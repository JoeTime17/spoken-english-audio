#!/usr/bin/env python3
"""Generate natural-speed and slow-shadowing neural-voice MP3s."""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path
import sys

try:
    import edge_tts
except ImportError:
    sys.exit(
        "edge-tts is required. Install it in a temporary virtual environment "
        "with: python3 -m pip install edge-tts"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate normal-speed and slow-shadowing MP3s from UTF-8 text."
    )
    parser.add_argument("input", type=Path, help="Speech-ready UTF-8 text file")
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory (default: the input file's directory)",
    )
    parser.add_argument(
        "--base-name",
        help="Output basename without suffix (default: input filename stem)",
    )
    parser.add_argument(
        "--voice",
        default="en-US-BrianMultilingualNeural",
        help="Edge TTS voice name",
    )
    parser.add_argument("--normal-rate", default="-4%")
    parser.add_argument("--slow-rate", default="-15%")
    parser.add_argument("--pitch", default="-2Hz")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace existing generated output files",
    )
    return parser.parse_args()


async def synthesize(
    text: str,
    output: Path,
    *,
    voice: str,
    rate: str,
    pitch: str,
) -> None:
    partial = output.with_suffix(output.suffix + ".part")
    if partial.exists():
        partial.unlink()
    try:
        speech = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate=rate,
            pitch=pitch,
        )
        await speech.save(str(partial))
        if not partial.exists() or partial.stat().st_size == 0:
            raise RuntimeError(f"Speech service returned an empty file for {output}")
        partial.replace(output)
    finally:
        if partial.exists():
            partial.unlink()


async def main() -> None:
    args = parse_args()
    input_path = args.input.resolve()
    if not input_path.is_file():
        raise FileNotFoundError(f"Input text file does not exist: {input_path}")

    text = input_path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError("Input text is empty")
    if "[[slnc" in text.lower() or "↗" in text or "↘" in text:
        raise ValueError(
            "Use the clean _spoken.txt file for audio. Remove practice markers and "
            "use punctuation and paragraphs for pauses."
        )

    output_dir = (args.output_dir or input_path.parent).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    base_name = args.base_name or input_path.stem
    normal_output = output_dir / f"{base_name}_normal.mp3"
    slow_output = output_dir / f"{base_name}_slow.mp3"

    existing = [path for path in (normal_output, slow_output) if path.exists()]
    if existing and not args.force:
        names = ", ".join(str(path) for path in existing)
        raise FileExistsError(f"Output already exists: {names}. Use --force to replace it.")

    await synthesize(
        text,
        normal_output,
        voice=args.voice,
        rate=args.normal_rate,
        pitch=args.pitch,
    )
    await synthesize(
        text,
        slow_output,
        voice=args.voice,
        rate=args.slow_rate,
        pitch=args.pitch,
    )

    print(f"normal={normal_output}")
    print(f"slow={slow_output}")


if __name__ == "__main__":
    asyncio.run(main())
