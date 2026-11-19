#!/usr/bin/env python3
"""Entry program for news-image-20261119.

Writes the front page (entry.png, drawn by draw_news.py) to /output.
Standard library only; deterministic; no network.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
MAX_BYTES = 1048576  # the competition's 1 MiB cap
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    src = os.path.join(HERE, "entry.png")
    with open(src, "rb") as fh:
        head = fh.read(len(PNG_MAGIC))
        if head != PNG_MAGIC:
            raise SystemExit("entry.png is not a PNG file")
    if os.path.getsize(src) > MAX_BYTES:
        raise SystemExit("entry.png is over the 1 MiB cap")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
