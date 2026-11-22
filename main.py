#!/usr/bin/env python3
"""Entry point for the news-image-20261122 (v2) make.fun entry.

The rendered front page ships in this repository as ``entry.png``.
Running this program simply installs that image, byte-for-byte, as
``entry.png`` inside the output directory so the grader can pick it up.

Only the Python standard library is used.
"""

import os
import shutil
import sys

IMAGE_NAME = "entry.png"
FALLBACK_OUTPUT_DIR = "/output"
OUTPUT_ENV_VAR = "MAKEFUN_OUTPUT_DIR"


def resolve_output_dir():
    """Return the directory the image should be written to.

    The harness tells us where output belongs through the
    MAKEFUN_OUTPUT_DIR environment variable; when that variable is
    missing or blank we fall back to the conventional /output path.
    """
    configured = os.environ.get(OUTPUT_ENV_VAR, "")
    if configured.strip():
        return configured
    return FALLBACK_OUTPUT_DIR


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, IMAGE_NAME)

    if not os.path.isfile(source):
        # Nothing to install: report it plainly rather than crashing
        # with a raw FileNotFoundError from deep inside shutil.
        print(f"error: {IMAGE_NAME} not found next to {__file__}", file=sys.stderr)
        return 1

    target_dir = resolve_output_dir()
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, IMAGE_NAME)

    # A straight binary copy keeps the PNG exactly as rendered.
    shutil.copyfile(source, target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
