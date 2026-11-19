#!/usr/bin/env python3
"""news-image-20261119 entrypoint.

Copies the pre-rendered front page into the grader's output directory.
Pure standard library, deterministic, no network access.
"""
import sys
from os import environ
from pathlib import Path

SOURCE_NAME = "entry.png"
PNG_SIGNATURE = bytes((0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A))
SIZE_LIMIT = 1024 * 1024


def die(message):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_front_page(path):
    blob = path.read_bytes()
    if blob[: len(PNG_SIGNATURE)] != PNG_SIGNATURE:
        die(f"{path} is not a PNG file")
    if len(blob) > SIZE_LIMIT:
        die(f"{path} is {len(blob)} bytes, over the 1 MiB cap")
    return blob


def run():
    folder = Path(__file__).resolve().parent
    blob = load_front_page(folder / SOURCE_NAME)
    out_dir = Path(environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / SOURCE_NAME).write_bytes(blob)


if __name__ == "__main__":
    run()
