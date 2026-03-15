from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from shutil import which


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="直接將教材 .tex 來源稿編譯成 PDF。"
    )
    parser.add_argument("tex", type=Path, help="LaTeX 來源稿路徑")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("build"),
        help="PDF 輸出資料夾",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.tex.exists():
        raise SystemExit(f"找不到 tex 檔案：{args.tex}")

    if which("latexmk") is None:
        raise SystemExit("找不到 latexmk，無法直接編譯 tex。")

    args.output_dir.mkdir(parents=True, exist_ok=True)

    command = [
        "latexmk",
        "-xelatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        f"-outdir={args.output_dir}",
        str(args.tex),
    ]

    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode != 0:
        stderr = result.stderr.strip()
        stdout = result.stdout.strip()
        details = stderr or stdout or "未知錯誤"
        raise SystemExit(f"tex 編譯失敗：{details}")

    pdf_path = args.output_dir / f"{args.tex.stem}.pdf"
    print(f"已輸出 PDF：{pdf_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
