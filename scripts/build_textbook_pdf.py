from __future__ import annotations

import argparse
import shlex
import subprocess
import sys
from pathlib import Path


VOICE_BLOCK_START = ":::voice"
VOICE_BLOCK_END = ":::"


def parse_voice_header(line: str) -> dict[str, str]:
    tokens = shlex.split(line[len(VOICE_BLOCK_START) :].strip())
    attrs: dict[str, str] = {}
    for token in tokens:
        if "=" not in token:
            continue
        key, value = token.split("=", 1)
        attrs[key.strip()] = value.strip()
    return attrs


def render_voice_block(attrs: dict[str, str], body_lines: list[str]) -> list[str]:
    section_id = attrs.get("id", "voice")
    title = attrs.get("title", section_id)
    rendered: list[str] = [
        "",
        f"> [語音解說] {title}",
        ">",
        f"> 音檔代號：`{section_id}`",
    ]

    if body_lines and any(line.strip() for line in body_lines):
        rendered.append(">")
        for line in body_lines:
            if line.strip():
                rendered.append(f"> {line.rstrip()}")
            else:
                rendered.append(">")

    rendered.append("")
    return rendered


def normalize_markdown(markdown_text: str) -> tuple[str | None, str]:
    lines = markdown_text.splitlines()
    normalized: list[str] = []
    current_attrs: dict[str, str] | None = None
    current_body: list[str] = []
    title: str | None = None
    in_fence = False
    fence_marker = ""

    for index, original_line in enumerate(lines):
        line = original_line
        stripped = line.strip()

        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = ""
            if current_attrs is not None:
                current_body.append(line)
            else:
                normalized.append(line)
            continue

        if not in_fence and title is None and stripped.startswith("# "):
            title = stripped[2:].strip()
            continue

        if stripped.startswith(VOICE_BLOCK_START):
            if current_attrs is not None:
                raise ValueError("偵測到未關閉的 voice 區塊。")
            current_attrs = parse_voice_header(stripped)
            current_body = []
            continue

        if stripped == VOICE_BLOCK_END and current_attrs is not None:
            normalized.extend(render_voice_block(current_attrs, current_body))
            current_attrs = None
            current_body = []
            continue

        if current_attrs is not None:
            current_body.append(line)
            continue

        if not in_fence and stripped == "---":
            normalized.extend(["", r"\newpage", ""])
            continue

        if not in_fence and line.startswith("##"):
            hashes, _, rest = line.partition(" ")
            if len(hashes) >= 2 and rest:
                line = f"{hashes[1:]} {rest}"

        normalized.append(line)

    if current_attrs is not None:
        raise ValueError("最後一個 voice 區塊未關閉。")

    return title, "\n".join(normalized).strip() + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="將教材 Markdown 轉成 LaTeX 與 PDF。"
    )
    parser.add_argument("markdown", type=Path, help="教材 Markdown 路徑")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("build"),
        help="輸出資料夾，會產生 .md、.tex、.pdf",
    )
    parser.add_argument(
        "--engine",
        choices=["xelatex", "lualatex"],
        default="xelatex",
        help="LaTeX 編譯引擎，預設為 xelatex",
    )
    return parser


def run_command(command: list[str]) -> None:
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode != 0:
        stderr = result.stderr.strip()
        stdout = result.stdout.strip()
        details = stderr or stdout or "未知錯誤"
        raise RuntimeError(details)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.markdown.exists():
        raise SystemExit(f"找不到教材檔案：{args.markdown}")

    if not shutil_which("pandoc"):
        raise SystemExit("找不到 pandoc，無法建立 LaTeX/PDF。")

    if not shutil_which(args.engine):
        raise SystemExit(f"找不到 {args.engine}，無法編譯 PDF。")

    repo_root = Path(__file__).resolve().parent.parent
    latex_dir = repo_root / "latex"
    metadata_file = latex_dir / "metadata.yaml"
    header_file = latex_dir / "preamble.tex"
    if not metadata_file.exists():
        raise SystemExit(f"找不到 PDF 設定檔：{metadata_file}")
    if not header_file.exists():
        raise SystemExit(f"找不到 LaTeX 前置檔：{header_file}")

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    input_text = args.markdown.read_text(encoding="utf-8")
    title, normalized_text = normalize_markdown(input_text)

    base_name = args.markdown.stem
    normalized_md = output_dir / f"{base_name}.print.md"
    tex_output = output_dir / f"{base_name}.tex"
    pdf_output = output_dir / f"{base_name}.pdf"

    normalized_md.write_text(normalized_text, encoding="utf-8")

    resource_path = f"{args.markdown.parent}:{repo_root}"
    common_args = [
        "pandoc",
        str(normalized_md),
        "--standalone",
        "--from",
        "markdown+pipe_tables+yaml_metadata_block+tex_math_dollars+raw_tex",
        "--resource-path",
        resource_path,
        "--metadata-file",
        str(metadata_file),
        "--include-in-header",
        str(header_file),
    ]
    if title:
        common_args.extend(["--metadata", f"title={title}"])

    tex_command = common_args + ["--to", "latex", "-o", str(tex_output)]
    pdf_command = common_args + [
        "--pdf-engine",
        args.engine,
        "-o",
        str(pdf_output),
    ]

    try:
        run_command(tex_command)
        run_command(pdf_command)
    except RuntimeError as exc:
        raise SystemExit(f"LaTeX/PDF 建置失敗：{exc}") from exc

    print(f"已輸出 Markdown：{normalized_md}")
    print(f"已輸出 LaTeX：{tex_output}")
    print(f"已輸出 PDF：{pdf_output}")
    return 0


def shutil_which(command: str) -> str | None:
    from shutil import which

    return which(command)


if __name__ == "__main__":
    sys.exit(main())
