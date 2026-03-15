from __future__ import annotations

import argparse
import asyncio
import json
import math
import re
import sys
from pathlib import Path

from build_module_video import (
    Scene,
    VideoProject,
    format_timestamp,
    parse_video_markdown,
    probe_duration,
    render_text_elements,
    require_command,
    run_command,
    short_label,
    synthesize_audio,
    wrap_text,
)


VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_FPS = 30
CLIP_PADDING = 0.35
TRANSITION_DURATION = 0.45
DEFAULT_VOICE = "zh-TW-HsiaoYuNeural"
DEFAULT_RATE = "+18%"
DEFAULT_PITCH = "+0Hz"
DEFAULT_VOLUME = "+0%"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".m4v", ".webm"}
TRANSITIONS = ["fadeblack", "smoothleft", "circleopen", "pixelize"]


def clean_title(title: str) -> str:
    return re.sub(r"^\d+\s*", "", title).strip()


def render_progress_bar(project: VideoProject, current_index: int) -> str:
    total = len(project.scenes)
    start_x = 120
    end_x = 960
    step = 0 if total == 1 else (end_x - start_x) / (total - 1)
    y = 1768
    parts = [
        f'<line x1="{start_x}" y1="{y}" x2="{end_x}" y2="{y}" stroke="#ffffff" stroke-opacity="0.18" stroke-width="4" />'
    ]
    for scene in project.scenes:
        x = start_x + (scene.index - 1) * step
        active = scene.index == current_index
        circle_fill = "#ffb703" if active else "#d9e2ec"
        circle_opacity = "1.0" if active else "0.24"
        text_fill = "#ffb703" if active else "#d9e2ec"
        weight = "700" if active else "500"
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y}" r="16" fill="{circle_fill}" fill-opacity="{circle_opacity}" />'
        )
        parts.append(
            f'<text x="{x:.1f}" y="{y + 50}" text-anchor="middle" fill="{text_fill}" '
            f'font-family="Heiti TC" font-size="22" font-weight="{weight}">{scene.index:02d}</text>'
        )
    return "\n".join(parts)


def render_focus_pills(scene: Scene) -> str:
    parts: list[str] = []
    x = 160
    y = 968
    for tag in scene.focus:
        width = max(170, len(tag) * 42 + 46)
        parts.append(
            f'<rect x="{x}" y="{y}" width="{width}" height="74" rx="37" '
            'fill="#fca311" fill-opacity="0.12" stroke="#fca311" stroke-opacity="0.22" />'
        )
        parts.append(
            f'<text x="{x + 30}" y="{y + 48}" fill="#ffb703" font-family="Heiti TC" '
            'font-size="34" font-weight="700">'
            f"{tag}</text>"
        )
        x += width + 20
    return "\n".join(parts)


def render_module_steps(scene: Scene) -> str:
    steps = ["時間價值", "NPV / IRR", "匯率基礎", "利率概念"]
    active_map = {
        1: 0,
        2: 1,
        3: 2,
        4: 3,
        5: 3,
    }
    active_index = active_map.get(scene.index, 0)
    start_y = 1328
    height = 80
    gap = 18
    parts: list[str] = []
    for index, step in enumerate(steps):
        y = start_y + index * (height + gap)
        active = index <= active_index
        fill = "#102a43" if active else "#d9e2ec"
        fill_opacity = "0.95" if active else "0.12"
        text_fill = "#f7f7f2" if active else "#9fb3c8"
        parts.append(
            f'<rect x="120" y="{y}" width="840" height="{height}" rx="28" '
            f'fill="{fill}" fill-opacity="{fill_opacity}" />'
        )
        parts.append(
            f'<text x="154" y="{y + 51}" fill="{text_fill}" font-family="Heiti TC" '
            f'font-size="32" font-weight="700">{index + 1}. {step}</text>'
        )
    return "\n".join(parts)


def build_bullet_lines(scene: Scene) -> list[str]:
    lines: list[str] = []
    for bullet in scene.bullets[:3]:
        wrapped = wrap_text(bullet, max_width=22)
        if not wrapped:
            continue
        lines.append(f"• {wrapped[0]}")
        for extra in wrapped[1:2]:
            lines.append(f"  {extra}")
    return lines


def build_slide_svg(project: VideoProject, scene: Scene) -> str:
    title_lines = wrap_text(clean_title(scene.title), max_width=14)
    kicker_lines = wrap_text(scene.kicker, max_width=22)
    takeaway_lines = wrap_text(scene.takeaway, max_width=14)
    bullet_lines = build_bullet_lines(scene)

    title_elements = render_text_elements(
        x=120,
        y=258,
        lines=title_lines,
        font_size=74,
        line_gap=96,
        fill="#f7f7f2",
        font_family="Songti TC",
        font_weight="700",
    )
    kicker_elements = render_text_elements(
        x=120,
        y=470,
        lines=kicker_lines,
        font_size=34,
        line_gap=46,
        fill="#ffb703",
        font_family="Heiti TC",
        font_weight="700",
    )
    takeaway_elements = render_text_elements(
        x=120,
        y=740,
        lines=takeaway_lines,
        font_size=54,
        line_gap=74,
        fill="#102a43",
        font_family="Songti TC",
        font_weight="700",
    )
    bullet_elements = render_text_elements(
        x=150,
        y=1140,
        lines=bullet_lines,
        font_size=32,
        line_gap=46,
        fill="#d9e2ec",
        font_family="Heiti TC",
        font_weight="500",
    )
    progress = render_progress_bar(project, scene.index)
    focus_pills = render_focus_pills(scene)
    module_steps = render_module_steps(scene)

    angle_y = 700 + scene.index * 10
    circle_x = 930 - scene.index * 12
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{VIDEO_WIDTH}" height="{VIDEO_HEIGHT}" viewBox="0 0 {VIDEO_WIDTH} {VIDEO_HEIGHT}">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#04111c" />
      <stop offset="55%" stop-color="#0b2239" />
      <stop offset="100%" stop-color="#133b5c" />
    </linearGradient>
    <linearGradient id="card" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffe2b3" />
      <stop offset="100%" stop-color="#ffd089" />
    </linearGradient>
  </defs>
  <rect width="{VIDEO_WIDTH}" height="{VIDEO_HEIGHT}" fill="url(#bg)" />
  <circle cx="{circle_x}" cy="250" r="190" fill="#fca311" fill-opacity="0.10" />
  <circle cx="1020" cy="470" r="84" fill="#ffd166" fill-opacity="0.16" />
  <path d="M-40 {angle_y} C220 {angle_y - 90}, 520 {angle_y + 60}, 1120 {angle_y - 40}" fill="none" stroke="#fca311" stroke-opacity="0.18" stroke-width="6" />
  <rect x="96" y="642" width="888" height="294" rx="48" fill="#f8deb0" />
  <rect x="96" y="1046" width="888" height="212" rx="42" fill="#081824" fill-opacity="0.88" stroke="#ffffff" stroke-opacity="0.08" />
  <text x="120" y="108" fill="#d9e2ec" font-family="Heiti TC" font-size="28" font-weight="700">MODULE 1 SHORT</text>
  <text x="120" y="146" fill="#9fb3c8" font-family="Heiti TC" font-size="24">財管基礎與匯率入門</text>
  <circle cx="918" cy="146" r="88" fill="#ffb703" />
  <text x="918" y="172" text-anchor="middle" fill="#102a43" font-family="Heiti TC" font-size="62" font-weight="700">{scene.index:02d}</text>
  {chr(10).join(title_elements)}
  {chr(10).join(kicker_elements)}
  <text x="120" y="718" fill="#243b53" font-family="Heiti TC" font-size="30" font-weight="700">一句話抓重點</text>
  {chr(10).join(takeaway_elements)}
  {focus_pills}
  <text x="120" y="1092" fill="#ffb703" font-family="Heiti TC" font-size="30" font-weight="700">這一段你要記住</text>
  {chr(10).join(bullet_elements)}
  <text x="120" y="1302" fill="#9fb3c8" font-family="Heiti TC" font-size="26">正式模組四步走</text>
  {module_steps}
  {progress}
</svg>
"""


def render_clip(
    scene_index: int,
    image_path: Path,
    audio_path: Path,
    clip_path: Path,
    duration: float,
    presenter_media: Path | None = None,
) -> None:
    fade_out_start = max(duration - 0.28, 0)
    total_frames = max(math.ceil(duration * VIDEO_FPS), 1)
    anchor_variants = [
        ("0.08", "0.10"),
        ("0.20", "0.14"),
        ("0.10", "0.20"),
        ("0.18", "0.08"),
    ]
    anchor_x, anchor_y = anchor_variants[(scene_index - 1) % len(anchor_variants)]
    video_filter = (
        f"zoompan=z='min(zoom+0.0007,1.06)':"
        f"x='(iw-iw/zoom)*{anchor_x}':y='(ih-ih/zoom)*{anchor_y}':"
        f"d={total_frames}:s={VIDEO_WIDTH}x{VIDEO_HEIGHT}:fps={VIDEO_FPS},"
        "eq=contrast=1.05:saturation=1.08:brightness=0.01,"
        "drawbox=x='mod(t*420,iw+180)-180':y=0:w=180:h=ih:color=white@0.035:t=fill,"
        "vignette=angle=PI/5,"
        f"fade=t=in:st=0:d=0.2,fade=t=out:st={fade_out_start:.2f}:d=0.28,"
        "format=yuv420p"
    )
    command = [
        "ffmpeg",
        "-y",
        "-loop",
        "1",
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

    presenter_x = "W-w-72"
    presenter_y = "294+18*sin(t*1.4)"
    filter_complex = (
        f"[0:v]{video_filter}[bg];"
        "[2:v]scale=360:-2,format=rgba,"
        "eq=contrast=1.04:saturation=1.03,"
        "colorchannelmixer=aa=0.98[presenter];"
        "[presenter]split[presenter_main][presenter_shadow];"
        "[presenter_shadow]boxblur=18:2,colorchannelmixer=aa=0.26[shadow];"
        f"[bg][shadow]overlay=x={presenter_x}+18:y={presenter_y}+24:shortest=1[bg_shadow];"
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


def detect_media_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in IMAGE_EXTENSIONS:
        return "image"
    if suffix in VIDEO_EXTENSIONS:
        return "video"
    raise SystemExit(f"不支援的人像素材格式：{path.suffix}")


def concat_clips(clips: list[Path], output_path: Path) -> None:
    raise NotImplementedError("請改用 compose_clips_with_transitions。")


def compose_clips_with_transitions(
    clips: list[Path], durations: list[float], output_path: Path
) -> None:
    if len(clips) != len(durations):
        raise ValueError("clips 與 durations 長度不一致。")

    if len(clips) == 1:
        run_command(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(clips[0]),
                "-c",
                "copy",
                "-movflags",
                "+faststart",
                str(output_path),
            ]
        )
        return

    command = ["ffmpeg", "-y"]
    for clip in clips:
        command.extend(["-i", str(clip)])

    filters: list[str] = []
    current_video = "[0:v]"
    current_audio = "[0:a]"
    timeline_length = durations[0]

    for index in range(1, len(clips)):
        transition = TRANSITIONS[(index - 1) % len(TRANSITIONS)]
        next_video = f"[v{index}]"
        next_audio = f"[a{index}]"
        offset = max(timeline_length - TRANSITION_DURATION, 0)
        filters.append(
            f"{current_video}[{index}:v]xfade=transition={transition}:"
            f"duration={TRANSITION_DURATION:.2f}:offset={offset:.2f}{next_video}"
        )
        filters.append(
            f"{current_audio}[{index}:a]acrossfade=d={TRANSITION_DURATION:.2f}:"
            f"c1=tri:c2=tri{next_audio}"
        )
        timeline_length = timeline_length + durations[index] - TRANSITION_DURATION
        current_video = next_video
        current_audio = next_audio

    command.extend(
        [
            "-filter_complex",
            ";".join(filters),
            "-map",
            current_video,
            "-map",
            current_audio,
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            str(output_path),
        ]
    )
    run_command(command)


def build_srt(project: VideoProject, durations: list[float]) -> str:
    parts: list[str] = []
    cursor = 0.0
    for scene, duration in zip(project.scenes, durations, strict=True):
        start = cursor
        end = cursor + duration
        cue_text = wrap_text(scene.narration, max_width=16)
        parts.append(str(scene.index))
        parts.append(f"{format_timestamp(start)} --> {format_timestamp(end)}")
        parts.extend(cue_text)
        parts.append("")
        cursor = end
    return "\n".join(parts).strip() + "\n"


def render_scene_image(svg_text: str, svg_path: Path, png_path: Path) -> None:
    svg_path.write_text(svg_text, encoding="utf-8")
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="把模組導覽稿轉成直式短影音。"
    )
    parser.add_argument("markdown", type=Path, help="短影音來源 Markdown")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("build/finance_module_short"),
        help="輸出資料夾",
    )
    parser.add_argument("--voice", default=DEFAULT_VOICE, help="Edge TTS 語音名稱")
    parser.add_argument("--rate", default=DEFAULT_RATE, help="語速，例如 +18%")
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

    project = parse_video_markdown(args.markdown.read_text(encoding="utf-8"))
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

        render_scene_image(build_slide_svg(project, scene), svg_path, png_path)
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
            scene.index,
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
    compose_clips_with_transitions(clip_paths, clip_durations, video_path)

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

    print(f"已輸出短影音：{video_path}")
    print(f"已輸出字幕：{srt_path}")
    print(f"已輸出素材清單：{manifest_path}")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
