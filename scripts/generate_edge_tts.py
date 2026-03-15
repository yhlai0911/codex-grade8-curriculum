from __future__ import annotations

import argparse
import asyncio
import json
import re
import shlex
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    import edge_tts
except ImportError as exc:  # pragma: no cover - dependency check
    raise SystemExit(
        "找不到 edge_tts。請先執行 `uv sync` 或 `uv add edge-tts`。"
    ) from exc


VOICE_BLOCK_START = ":::voice"
VOICE_BLOCK_END = ":::"
DEFAULT_VOICE = "zh-TW-YunJheNeural"
DEFAULT_RATE = "+0%"
DEFAULT_PITCH = "+0Hz"
DEFAULT_VOLUME = "+0%"
DEFAULT_MAX_CHARS = 320


@dataclass
class VoiceSection:
    section_id: str
    title: str
    body: str


def parse_voice_header(line: str) -> dict[str, str]:
    tokens = shlex.split(line[len(VOICE_BLOCK_START) :].strip())
    attrs: dict[str, str] = {}
    for token in tokens:
        if "=" not in token:
            continue
        key, value = token.split("=", 1)
        attrs[key.strip()] = value.strip()
    return attrs


def extract_voice_sections(markdown_text: str) -> list[VoiceSection]:
    sections: list[VoiceSection] = []
    lines = markdown_text.splitlines()
    current_attrs: dict[str, str] | None = None
    current_body: list[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith(VOICE_BLOCK_START):
            if current_attrs is not None:
                raise ValueError("偵測到未關閉的 voice 區塊。")
            current_attrs = parse_voice_header(stripped)
            current_body = []
            continue

        if stripped == VOICE_BLOCK_END and current_attrs is not None:
            section_id = current_attrs.get("id")
            if not section_id:
                raise ValueError("voice 區塊缺少 id。")
            title = current_attrs.get("title", section_id)
            body = clean_markdown_text("\n".join(current_body))
            if body:
                sections.append(
                    VoiceSection(section_id=section_id, title=title, body=body)
                )
            current_attrs = None
            current_body = []
            continue

        if current_attrs is not None:
            current_body.append(line)

    if current_attrs is not None:
        raise ValueError("最後一個 voice 區塊未關閉。")

    return sections


def clean_markdown_text(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[*_>#-]{1,3}\s*", "", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()


def split_text(text: str, max_chars: int) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= max_chars:
        return [text]

    sentences = re.split(r"(?<=[。！？])", text)
    chunks: list[str] = []
    current = ""

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        if len(sentence) > max_chars:
            if current:
                chunks.append(current.strip())
                current = ""
            for index in range(0, len(sentence), max_chars):
                chunks.append(sentence[index : index + max_chars].strip())
            continue

        if len(current) + len(sentence) + 1 <= max_chars:
            current = f"{current} {sentence}".strip()
        else:
            if current:
                chunks.append(current.strip())
            current = sentence

    if current:
        chunks.append(current.strip())

    return chunks


async def synthesize_chunk(
    text: str,
    output_path: Path,
    voice: str,
    rate: str,
    pitch: str,
    volume: str,
) -> None:
    communicator = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        pitch=pitch,
        volume=volume,
    )
    await communicator.save(str(output_path))


async def render_sections(
    sections: list[VoiceSection],
    output_dir: Path,
    voice: str,
    rate: str,
    pitch: str,
    volume: str,
    max_chars: int,
) -> list[dict[str, object]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest: list[dict[str, object]] = []

    for section in sections:
        chunks = split_text(section.body, max_chars=max_chars)
        files: list[str] = []
        for index, chunk in enumerate(chunks, start=1):
            suffix = "" if len(chunks) == 1 else f"_{index:02d}"
            filename = f"{section.section_id}{suffix}.mp3"
            output_path = output_dir / filename
            await synthesize_chunk(
                text=chunk,
                output_path=output_path,
                voice=voice,
                rate=rate,
                pitch=pitch,
                volume=volume,
            )
            files.append(filename)

        manifest.append(
            {
                "id": section.section_id,
                "title": section.title,
                "files": files,
                "chars": len(section.body),
            }
        )

    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="把教材 Markdown 內的 voice 區塊轉成 Edge TTS 音檔。"
    )
    parser.add_argument("markdown", type=Path, help="教材 Markdown 路徑")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("audio"),
        help="音檔輸出資料夾",
    )
    parser.add_argument(
        "--voice",
        default=DEFAULT_VOICE,
        help="Edge TTS 語音名稱，例如 zh-TW-YunJheNeural",
    )
    parser.add_argument("--rate", default=DEFAULT_RATE, help="語速，例如 -5%")
    parser.add_argument("--pitch", default=DEFAULT_PITCH, help="音高，例如 +0Hz")
    parser.add_argument(
        "--volume", default=DEFAULT_VOLUME, help="音量，例如 +0%"
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=DEFAULT_MAX_CHARS,
        help="單一音檔最大字數，超過會自動切段",
    )
    parser.add_argument(
        "--only",
        nargs="*",
        default=None,
        help="只輸出指定的 voice id",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="只列出 voice 區塊，不產生音檔",
    )
    return parser


async def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.markdown.exists():
        raise SystemExit(f"找不到教材檔案：{args.markdown}")

    markdown_text = args.markdown.read_text(encoding="utf-8")
    sections = extract_voice_sections(markdown_text)
    if args.only:
        target_ids = set(args.only)
        sections = [section for section in sections if section.section_id in target_ids]

    if not sections:
        raise SystemExit("沒有可輸出的 voice 區塊。")

    if args.list:
        for section in sections:
            print(f"{section.section_id}\t{section.title}\t{len(section.body)}")
        return 0

    manifest = await render_sections(
        sections=sections,
        output_dir=args.output_dir,
        voice=args.voice,
        rate=args.rate,
        pitch=args.pitch,
        volume=args.volume,
        max_chars=args.max_chars,
    )

    manifest_path = args.output_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "source_markdown": str(args.markdown),
                "voice": args.voice,
                "rate": args.rate,
                "pitch": args.pitch,
                "volume": args.volume,
                "sections": manifest,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"已輸出 {len(manifest)} 個 voice 區塊到 {args.output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
