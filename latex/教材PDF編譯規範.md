# 教材 PDF 編譯規範

## 來源稿規則

- 正式教材與正式讀書計畫一律以 `.tex` 為排版來源稿。
- `.md` 僅保留給內容整理、語音區塊維護與必要時轉寫使用。
- 可朗讀段落若在 Markdown 中維護，使用 `:::voice ... :::` 區塊標記。

## 編譯工具

- 正式編譯：`latexmk + xelatex`
- 轉寫流程：`pandoc + xelatex`
- 預設備援引擎：`lualatex`

## 版面規格

- 紙張：`A4`
- 字級：`12pt`
- 邊界：上 `24mm`、下 `26mm`、左 `24mm`、右 `24mm`
- 中文字型：`Songti TC`
- 等寬字型：`Menlo`
- 正式產物：`.tex`、`.pdf`
- 轉寫流程產物：`.print.md`、`.tex`、`.pdf`

## 專案命令

```bash
uv run python scripts/compile_tex_pdf.py 教材/惠文國二下數學_PBL自學語音教材.tex
uv run python scripts/compile_tex_pdf.py 教材/惠文國二下數學_段考對齊讀書計畫.tex
uv run python scripts/build_textbook_pdf.py 教材/惠文國二下數學_PBL自學語音教材.md
uv run python scripts/build_textbook_pdf.py 教材/惠文國二下數學_PBL自學語音教材.md --engine lualatex
```

## 產出路徑

- 預設輸出到 `build/`
- 會保留中間檔，方便校稿與追查排版問題
