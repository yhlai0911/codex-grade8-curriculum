# 主持人素材

把真人主持人素材放在這裡，之後可直接用：

```bash
uv run python scripts/build_short_video.py \
  video/prerequisite_finance_short.md \
  --presenter-media assets/presenter/your-professor.mp4
```

或：

```bash
uv run python scripts/build_short_video.py \
  video/prerequisite_finance_short.md \
  --presenter-media assets/presenter/your-professor.png
```

建議素材：

- 直式或接近直式的人像照片
- 或 `5` 到 `10` 秒、上半身、正面、背景乾淨的人物短片
- 格式支援：`png`、`jpg`、`jpeg`、`webp`、`mp4`、`mov`

注意：

- 如果你要明確是「台灣人年輕教授」，請提供你自己指定且可用的人像素材。
- 不能只靠外觀判定國籍，所以沒有指定素材時，不能準確聲稱人物是台灣人。
