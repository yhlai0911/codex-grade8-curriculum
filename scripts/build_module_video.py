from __future__ import annotations

import argparse
import asyncio
import html
import json
import re
import shlex
import subprocess
import sys
import unicodedata
from dataclasses import dataclass, field
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
VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
VIDEO_FPS = 30
CLIP_PADDING = 0.8
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".m4v", ".webm"}


@dataclass
class Scene:
    index: int
    title: str
    kicker: str = ""
    takeaway: str = ""
    focus: list[str] = field(default_factory=list)
    bullets: list[str] = field(default_factory=list)
    voice_id: str = ""
    voice_title: str = ""
    narration: str = ""


@dataclass
class VideoProject:
    title: str
    scenes: list[Scene]


def parse_voice_header(line: str) -> dict[str, str]:
    tokens = shlex.split(line[len(VOICE_BLOCK_START) :].strip())
    attrs: dict[str, str] = {}
    for token in tokens:
        if "=" not in token:
            continue
        key, value = token.split("=", 1)
        attrs[key.strip()] = value.strip()
    return attrs


def split_focus_tags(value: str) -> list[str]:
    tags = re.split(r"[、,，/]+", value)
    return [tag.strip() for tag in tags if tag.strip()]


def display_width(text: str) -> int:
    width = 0
    for char in text:
        if unicodedata.east_asian_width(char) in {"W", "F"}:
            width += 2
        else:
            width += 1
    return width


def wrap_text(text: str, max_width: int) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []

    lines: list[str] = []
    current = ""
    current_width = 0

    for char in text:
        if char == "\n":
            if current.strip():
                lines.append(current.strip())
            current = ""
            current_width = 0
            continue

        char_width = 2 if unicodedata.east_asian_width(char) in {"W", "F"} else 1
        if current and current_width + char_width > max_width:
            lines.append(current.strip())
            current = char
            current_width = char_width
        else:
            current += char
            current_width += char_width

    if current.strip():
        lines.append(current.strip())

    return lines


def short_label(text: str, max_width: int = 10) -> str:
    cleaned = re.sub(r"^\d+\s*", "", text).strip()
    result = ""
    width = 0
    for char in cleaned:
        char_width = 2 if unicodedata.east_asian_width(char) in {"W", "F"} else 1
        if width + char_width > max_width:
            break
        result += char
        width += char_width
    return result or cleaned[:4]


def parse_video_markdown(markdown_text: str) -> VideoProject:
    title = ""
    scenes: list[Scene] = []
    current: Scene | None = None
    in_voice = False
    voice_attrs: dict[str, str] | None = None
    voice_lines: list[str] = []

    lines = markdown_text.splitlines()
    for line in lines:
        stripped = line.strip()

        if not title and stripped.startswith("# "):
            title = stripped[2:].strip()
            continue

        if stripped.startswith("## "):
            if current is not None:
                if not current.voice_id or not current.narration:
                    raise ValueError(f"場景缺少 voice 區塊：{current.title}")
                scenes.append(current)
            current = Scene(index=len(scenes) + 1, title=stripped[3:].strip())
            in_voice = False
            voice_attrs = None
            voice_lines = []
            continue

        if current is None:
            continue

        if stripped.startswith(VOICE_BLOCK_START):
            if in_voice:
                raise ValueError(f"偵測到未關閉的 voice 區塊：{current.title}")
            in_voice = True
            voice_attrs = parse_voice_header(stripped)
            voice_lines = []
            continue

        if stripped == VOICE_BLOCK_END and in_voice:
            current.voice_id = voice_attrs.get("id", f"scene-{current.index:02d}")
            current.voice_title = voice_attrs.get("title", current.title)
            current.narration = "\n".join(voice_lines).strip()
            in_voice = False
            voice_attrs = None
            voice_lines = []
            continue

        if in_voice:
            voice_lines.append(line)
            continue

        if stripped.startswith("kicker:"):
            current.kicker = stripped.partition(":")[2].strip()
            continue

        if stripped.startswith("takeaway:"):
            current.takeaway = stripped.partition(":")[2].strip()
            continue

        if stripped.startswith("focus:"):
            current.focus = split_focus_tags(stripped.partition(":")[2].strip())
            continue

        if stripped.startswith("- "):
            current.bullets.append(stripped[2:].strip())
            continue

    if in_voice:
        raise ValueError("最後一個 voice 區塊未關閉。")

    if current is not None:
        if not current.voice_id or not current.narration:
            raise ValueError(f"場景缺少 voice 區塊：{current.title}")
        scenes.append(current)

    if not title:
        raise ValueError("找不到影片標題。")
    if not scenes:
        raise ValueError("找不到任何場景。")

    return VideoProject(title=title, scenes=scenes)


def render_text_elements(
    *,
    x: int,
    y: int,
    lines: list[str],
    font_size: int,
    line_gap: int,
    fill: str,
    font_family: str,
    font_weight: str = "400",
) -> list[str]:
    elements: list[str] = []
    for index, line in enumerate(lines):
        line_y = y + index * line_gap
        escaped = html.escape(line)
        elements.append(
            f'<text x="{x}" y="{line_y}" fill="{fill}" '
            f'font-family="{font_family}" font-size="{font_size}" '
            f'font-weight="{font_weight}">{escaped}</text>'
        )
    return elements


def render_focus_chips(scene: Scene) -> str:
    if not scene.focus:
        return ""

    chip_x = 1180
    chip_y = 640
    chip_gap = 18
    parts: list[str] = []
    for tag in scene.focus:
        width = max(140, display_width(tag) * 16 + 56)
        parts.append(
            f'<rect x="{chip_x}" y="{chip_y}" width="{width}" height="54" '
            'rx="27" fill="#ffffff" fill-opacity="0.38" stroke="#102a43" '
            'stroke-opacity="0.10" />'
        )
        parts.append(
            f'<text x="{chip_x + 28}" y="{chip_y + 35}" fill="#102a43" '
            'font-family="Heiti TC" font-size="28" font-weight="600">'
            f"{html.escape(tag)}</text>"
        )
        chip_x += width + chip_gap

    return "\n".join(parts)


def render_progress(project: VideoProject, current_index: int) -> str:
    total = len(project.scenes)
    start_x = 160
    end_x = 1760
    step = 0 if total == 1 else (end_x - start_x) / (total - 1)
    baseline_y = 930
    parts = [
        '<line x1="160" y1="930" x2="1760" y2="930" stroke="#ffffff" '
        'stroke-opacity="0.18" stroke-width="4" />'
    ]

    for scene in project.scenes:
        x = start_x + (scene.index - 1) * step
        active = scene.index == current_index
        circle_fill = "#fca311" if active else "#ffffff"
        circle_opacity = "1.0" if active else "0.24"
        text_fill = "#fca311" if active else "#f4f7fb"
        label_weight = "700" if active else "500"
        parts.append(
            f'<circle cx="{x:.1f}" cy="{baseline_y}" r="18" fill="{circle_fill}" '
            f'fill-opacity="{circle_opacity}" />'
        )
        parts.append(
            f'<text x="{x:.1f}" y="{baseline_y + 54}" text-anchor="middle" '
            f'fill="{text_fill}" font-family="Heiti TC" font-size="24" '
            f'font-weight="{label_weight}">{html.escape(short_label(scene.title))}</text>'
        )

    return "\n".join(parts)


def render_bullet_lines(scene: Scene) -> list[str]:
    lines: list[str] = []
    for bullet in scene.bullets:
        wrapped = wrap_text(bullet, max_width=32)
        if not wrapped:
            continue
        lines.append(f"• {wrapped[0]}")
        for extra in wrapped[1:]:
            lines.append(f"   {extra}")
    return lines


def build_slide_svg(project: VideoProject, scene: Scene) -> str:
    title_lines = wrap_text(scene.title, max_width=18)
    kicker_lines = wrap_text(scene.kicker, max_width=34)
    takeaway_lines = wrap_text(scene.takeaway or scene.kicker, max_width=18)
    bullet_lines = render_bullet_lines(scene)
    scene_number = f"{scene.index:02d}"

    title_elements = render_text_elements(
        x=140,
        y=220,
        lines=title_lines,
        font_size=72,
        line_gap=92,
        fill="#f4f7fb",
        font_family="Songti TC",
        font_weight="700",
    )
    kicker_elements = render_text_elements(
        x=140,
        y=360,
        lines=kicker_lines,
        font_size=28,
        line_gap=40,
        fill="#fca311",
        font_family="Heiti TC",
        font_weight="500",
    )
    bullet_elements = render_text_elements(
        x=170,
        y=490,
        lines=bullet_lines,
        font_size=28,
        line_gap=42,
        fill="#f4f7fb",
        font_family="Heiti TC",
        font_weight="400",
    )
    takeaway_elements = render_text_elements(
        x=1180,
        y=430,
        lines=takeaway_lines,
        font_size=44,
        line_gap=62,
        fill="#102a43",
        font_family="Songti TC",
        font_weight="700",
    )

    focus_chips = render_focus_chips(scene)
    progress = render_progress(project, scene.index)
    voice_lines = wrap_text(scene.voice_title or scene.title, max_width=18)
    voice_elements = render_text_elements(
        x=1180,
        y=770,
        lines=voice_lines,
        font_size=28,
        line_gap=38,
        fill="#486581",
        font_family="Heiti TC",
        font_weight="500",
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{VIDEO_WIDTH}" height="{VIDEO_HEIGHT}" viewBox="0 0 {VIDEO_WIDTH} {VIDEO_HEIGHT}">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#09141f" />
      <stop offset="60%" stop-color="#102a43" />
      <stop offset="100%" stop-color="#16324f" />
    </linearGradient>
    <linearGradient id="card" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f7b267" />
      <stop offset="100%" stop-color="#ffd166" />
    </linearGradient>
  </defs>
  <rect width="{VIDEO_WIDTH}" height="{VIDEO_HEIGHT}" fill="url(#bg)" />
  <circle cx="1590" cy="150" r="200" fill="#fca311" fill-opacity="0.08" />
  <circle cx="1780" cy="300" r="90" fill="#ffd166" fill-opacity="0.18" />
  <path d="M40 850 C320 730, 520 960, 840 860 S1380 720, 1880 840" fill="none" stroke="#fca311" stroke-opacity="0.14" stroke-width="6" />
  <rect x="110" y="410" width="900" height="430" rx="34" fill="#ffffff" fill-opacity="0.08" stroke="#ffffff" stroke-opacity="0.10" />
  <rect x="1120" y="240" width="670" height="580" rx="38" fill="#ffe2b3" />
  <rect x="1120" y="240" width="670" height="580" rx="38" fill="#ffffff" fill-opacity="0.14" />
  <text x="140" y="110" fill="#d9e2ec" font-family="Heiti TC" font-size="24" font-weight="600">MODULE OVERVIEW</text>
  <text x="140" y="150" fill="#9fb3c8" font-family="Heiti TC" font-size="22">{html.escape(project.title)}</text>
  <circle cx="1650" cy="170" r="78" fill="#fca311" />
  <text x="1650" y="188" text-anchor="middle" fill="#102a43" font-family="Heiti TC" font-size="54" font-weight="700">{scene_number}</text>
  {chr(10).join(title_elements)}
  {chr(10).join(kicker_elements)}
  <text x="170" y="470" fill="#fca311" font-family="Heiti TC" font-size="28" font-weight="700">這一段你會看到</text>
  {chr(10).join(bullet_elements)}
  <text x="1180" y="320" fill="#243b53" font-family="Heiti TC" font-size="28" font-weight="700">本段重點</text>
  {chr(10).join(takeaway_elements)}
  {focus_chips}
  <text x="1180" y="730" fill="#243b53" font-family="Heiti TC" font-size="24" font-weight="700">對應旁白段落</text>
  {chr(10).join(voice_elements)}
  {progress}
</svg>
"""


def require_command(command: str) -> None:
    from shutil import which

    if not which(command):
        raise SystemExit(f"找不到 `{command}`，無法建立影片。")


def run_command(command: list[str]) -> None:
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode != 0:
        details = result.stderr.strip() or result.stdout.strip() or "未知錯誤"
        raise RuntimeError(details)


async def synthesize_audio(
    scene: Scene,
    *,
    output_path: Path,
    voice: str,
    rate: str,
    pitch: str,
    volume: str,
) -> None:
    communicator = edge_tts.Communicate(
        text=scene.narration,
        voice=voice,
        rate=rate,
        pitch=pitch,
        volume=volume,
    )
    await communicator.save(str(output_path))


def render_scene_image(scene_svg: str, svg_path: Path, png_path: Path) -> None:
    svg_path.write_text(scene_svg, encoding="utf-8")
    run_command(
        [
            "magick",
            "-density",
            "220",
            str(svg_path),
            "-resize",
            f"{VIDEO_WIDTH}x{VIDEO_HEIGHT}",
            str(png_path),
        ]
    )


def probe_duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        details = result.stderr.strip() or result.stdout.strip() or "未知錯誤"
        raise RuntimeError(f"無法讀取音檔時長：{details}")
    return float(result.stdout.strip())


def detect_media_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in IMAGE_EXTENSIONS:
        return "image"
    if suffix in VIDEO_EXTENSIONS:
        return "video"
    raise SystemExit(f"不支援的人像素材格式：{path.suffix}")


def render_clip(
    image_path: Path,
    audio_path: Path,
    clip_path: Path,
    duration: float,
    presenter_media: Path | None = None,
) -> None:
    fade_out_start = max(duration - 0.45, 0)
    video_filter = (
        f"fade=t=in:st=0:d=0.35,"
        f"fade=t=out:st={fade_out_start:.2f}:d=0.45,"
        "format=yuv420p"
    )
    command = [
        "ffmpeg",
        "-y",
        "-loop",
        "1",
        "-framerate",
        str(VIDEO_FPS),
        "-i",
        str(image_path),
        "-i",
        str(audio_path),
    ]
    if presenter_media is None:
        command.extend(
            [
                "-vf",
                video_filter,
                "-af",
                f"apad=pad_dur={CLIP_PADDING:.2f}",
                "-t",
                f"{duration:.2f}",
                "-c:v",
                "libx264",
                "-preset",
                "medium",
                "-crf",
                "20",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                str(clip_path),
            ]
        )
        run_command(command)
        return

    presenter_type = detect_media_type(presenter_media)
    if presenter_type == "image":
        command.extend(["-loop", "1", "-i", str(presenter_media)])
    else:
        command.extend(["-stream_loop", "-1", "-i", str(presenter_media)])

    presenter_x = "W-w-84"
    presenter_y = "H-h-76+16*sin(t*1.1)"
    filter_complex = (
        f"[0:v]{video_filter}[bg];"
        "[2:v]scale=480:-2,format=rgba,"
        "eq=contrast=1.03:saturation=1.03,"
        "colorchannelmixer=aa=0.98[presenter];"
        "[presenter]split[presenter_main][presenter_shadow];"
        "[presenter_shadow]boxblur=22:3,colorchannelmixer=aa=0.24[shadow];"
        f"[bg][shadow]overlay=x={presenter_x}+22:y={presenter_y}+26:shortest=1[bg_shadow];"
        f"[bg_shadow][presenter_main]overlay=x={presenter_x}:y={presenter_y}:shortest=1[outv]"
    )
    command.extend(
        [
            "-filter_complex",
            filter_complex,
            "-map",
            "[outv]",
            "-map",
            "1:a",
            "-af",
            f"apad=pad_dur={CLIP_PADDING:.2f}",
            "-t",
            f"{duration:.2f}",
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "20",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            str(clip_path),
        ]
    )
    run_command(command)


def concat_clips(clips: list[Path], output_path: Path) -> None:
    concat_file = output_path.with_suffix(".concat.txt")
    lines = [f"file '{clip.resolve()}'" for clip in clips]
    concat_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    run_command(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c",
            "copy",
            "-movflags",
            "+faststart",
            str(output_path),
        ]
    )


def format_timestamp(seconds: float) -> str:
    millis = int(round(seconds * 1000))
    hours, remainder = divmod(millis, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, ms = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def build_srt(project: VideoProject, durations: list[float]) -> str:
    parts: list[str] = []
    cursor = 0.0
    for scene, duration in zip(project.scenes, durations, strict=True):
        start = cursor
        end = cursor + duration
        cue_text = wrap_text(scene.narration, max_width=34)
        parts.append(str(scene.index))
        parts.append(f"{format_timestamp(start)} --> {format_timestamp(end)}")
        parts.extend(cue_text)
        parts.append("")
        cursor = end
    return "\n".join(parts).strip() + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="把模組導覽 Markdown 轉成旁白投影片影片。"
    )
    parser.add_argument("markdown", type=Path, help="影片來源 Markdown")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("build/finance_module_video"),
        help="輸出資料夾",
    )
    parser.add_argument("--voice", default=DEFAULT_VOICE, help="Edge TTS 語音名稱")
    parser.add_argument("--rate", default=DEFAULT_RATE, help="語速，例如 -5%")
    parser.add_argument("--pitch", default=DEFAULT_PITCH, help="音高，例如 +0Hz")
    parser.add_argument("--volume", default=DEFAULT_VOLUME, help="音量，例如 +0%")
    parser.add_argument(
        "--presenter-media",
        type=Path,
        default=None,
        help="真人主持人照片或短片路徑，可用 png/jpg/webp/mp4/mov",
    )
    return parser


async def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.markdown.exists():
        raise SystemExit(f"找不到來源稿：{args.markdown}")
    if args.presenter_media is not None and not args.presenter_media.exists():
        raise SystemExit(f"找不到人像素材：{args.presenter_media}")

    require_command("magick")
    require_command("ffmpeg")
    require_command("ffprobe")

    markdown_text = args.markdown.read_text(encoding="utf-8")
    project = parse_video_markdown(markdown_text)

    output_dir = args.output_dir
    slides_dir = output_dir / "slides"
    audio_dir = output_dir / "audio"
    clips_dir = output_dir / "clips"
    for path in (slides_dir, audio_dir, clips_dir):
        path.mkdir(parents=True, exist_ok=True)

    clip_paths: list[Path] = []
    clip_durations: list[float] = []
    manifest: list[dict[str, object]] = []

    for scene in project.scenes:
        stem = f"{scene.index:02d}-{scene.voice_id}"
        svg_path = slides_dir / f"{stem}.svg"
        png_path = slides_dir / f"{stem}.png"
        audio_path = audio_dir / f"{stem}.mp3"
        clip_path = clips_dir / f"{stem}.mp4"

        slide_svg = build_slide_svg(project, scene)
        render_scene_image(slide_svg, svg_path, png_path)
        await synthesize_audio(
            scene,
            output_path=audio_path,
            voice=args.voice,
            rate=args.rate,
            pitch=args.pitch,
            volume=args.volume,
        )
        duration = probe_duration(audio_path) + CLIP_PADDING
        render_clip(
            png_path,
            audio_path,
            clip_path,
            duration,
            presenter_media=args.presenter_media,
        )

        clip_paths.append(clip_path)
        clip_durations.append(duration)
        manifest.append(
            {
                "index": scene.index,
                "title": scene.title,
                "voice_id": scene.voice_id,
                "audio": str(audio_path),
                "slide": str(png_path),
                "clip": str(clip_path),
                "duration_seconds": round(duration, 3),
            }
        )

    video_path = output_dir / f"{args.markdown.stem}.mp4"
    concat_clips(clip_paths, video_path)

    srt_path = output_dir / f"{args.markdown.stem}.srt"
    srt_path.write_text(build_srt(project, clip_durations), encoding="utf-8")

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "source_markdown": str(args.markdown),
                "voice": args.voice,
                "rate": args.rate,
                "pitch": args.pitch,
                "volume": args.volume,
                "presenter_media": str(args.presenter_media) if args.presenter_media else None,
                "video": str(video_path),
                "subtitle": str(srt_path),
                "scenes": manifest,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"已輸出影片：{video_path}")
    print(f"已輸出字幕：{srt_path}")
    print(f"已輸出素材清單：{manifest_path}")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
