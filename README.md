# 惠文國二下數學 PBL 自學教材

這個工作區包含一份為臺中市立惠文高中國二學生設計的自學型數學 PBL 教材。現在正式排版來源稿以 `.tex` 為主；`.md` 保留作內容草稿與 Edge TTS 轉語音使用。

## 檔案

- `教材/惠文國二下數學_PBL自學語音教材.tex`：正式教材來源稿
- `教材/惠文國二下數學_PBL自學語音教材.md`：內容草稿 / TTS 來源稿
- `教材/惠文國二下數學_段考對齊讀書計畫.tex`：段考對齊讀書計畫來源稿
- `scripts/generate_edge_tts.py`：將 `voice` 區塊轉成 MP3
- `scripts/compile_tex_pdf.py`：直接將 `.tex` 編譯成 PDF
- `scripts/build_textbook_pdf.py`：將教材 Markdown 轉成 LaTeX 與 PDF
- `video/finance_module_overview.md`：模組導覽影片來源稿
- `scripts/build_module_video.py`：將模組導覽稿轉成旁白投影片影片
- `video/prerequisite_finance_short.md`：Module 1 直式短影音來源稿
- `scripts/build_short_video.py`：將短影音稿轉成 9:16 `mp4`
- `assets/presenter/README.md`：真人主持人素材放置方式
- `latex/教材PDF編譯規範.md`：LaTeX / PDF 輸出規範

## 快速開始

```bash
uv sync
uv run python scripts/compile_tex_pdf.py 教材/惠文國二下數學_PBL自學語音教材.tex
```

若要輸出語音：

```bash
uv run python scripts/generate_edge_tts.py 教材/惠文國二下數學_PBL自學語音教材.md
```

預設輸出資料夾為 `audio/`，預設語音為 `zh-TW-YunJheNeural`。

若要輸出模組導覽影片：

```bash
uv run python scripts/build_module_video.py video/finance_module_overview.md
```

預設會輸出到 `build/finance_module_video/`，並保留：

- `slides/*.svg`
- `slides/*.png`
- `audio/*.mp3`
- `clips/*.mp4`
- `finance_module_overview.mp4`
- `finance_module_overview.srt`
- `manifest.json`

若要輸出直式短影音：

```bash
uv run python scripts/build_short_video.py video/prerequisite_finance_short.md
```

預設會輸出到 `build/finance_module_short/`，並保留：

- `slides/*.svg`
- `slides/*.png`
- `audio/*.mp3`
- `clips/*.mp4`
- `prerequisite_finance_short.mp4`
- `prerequisite_finance_short.srt`
- `manifest.json`

若你要把 Markdown 草稿重新轉成 LaTeX / PDF：

```bash
uv run python scripts/build_textbook_pdf.py 教材/惠文國二下數學_PBL自學語音教材.md
```

預設會輸出到 `build/`，並保留：

- `.print.md`
- `.tex`
- `.pdf`

## 常用指令

```bash
uv run python scripts/generate_edge_tts.py 教材/惠文國二下數學_PBL自學語音教材.md --output-dir 語音
uv run python scripts/generate_edge_tts.py 教材/惠文國二下數學_PBL自學語音教材.md --only 00-orientation 01-sequence-opening
uv run python scripts/generate_edge_tts.py 教材/惠文國二下數學_PBL自學語音教材.md --voice zh-TW-HsiaoYuNeural --rate=-5%
uv run python scripts/generate_edge_tts.py 教材/惠文國二下數學_PBL自學語音教材.md --list
uv run python scripts/compile_tex_pdf.py 教材/惠文國二下數學_PBL自學語音教材.tex
uv run python scripts/compile_tex_pdf.py 教材/惠文國二下數學_段考對齊讀書計畫.tex
uv run python scripts/build_textbook_pdf.py 教材/惠文國二下數學_PBL自學語音教材.md
uv run python scripts/build_textbook_pdf.py 教材/惠文國二下數學_PBL自學語音教材.md --engine lualatex
uv run python scripts/build_module_video.py video/finance_module_overview.md
uv run python scripts/build_module_video.py video/finance_module_overview.md --voice zh-TW-HsiaoYuNeural --rate=-6%
uv run python scripts/build_short_video.py video/prerequisite_finance_short.md
uv run python scripts/build_short_video.py video/prerequisite_finance_short.md --voice zh-TW-YunJheNeural --rate=+20%
uv run python scripts/build_short_video.py video/prerequisite_finance_short.md --presenter-media assets/presenter/your-professor.mp4
```

## `voice` 區塊格式

```md
:::voice id=sample-opening title="示範開場"
這一段文字會被轉成音檔。
建議每段控制在 250 到 350 字內，方便學生分段聽。
:::
```

腳本會輸出：

- `sample-opening.mp3`
- `manifest.json`

## LaTeX / PDF 規格

- 正式排版來源稿是 `.tex`
- 正式 PDF 編譯流程是 `latexmk + xelatex`
- `.md` 只用於內容整理、TTS 與必要時轉寫成 `.tex`
- 數學符號與方程式請用 LaTeX 數學模式書寫：行內公式用 `$...$`，獨立公式用 `$$...$$`
- 預設中文字型是 `Songti TC`
- 預設等寬字型是 `Menlo`
- 詳細規範請看 `latex/教材PDF編譯規範.md`
