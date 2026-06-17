#!/usr/bin/env python3
"""Generate or edit images with the OpenAI Images API using gpt-image-2."""

from __future__ import annotations

import argparse
import base64
import json
import os
from pathlib import Path
import re
import sys
from typing import Any


MODEL = "gpt-image-2"
DEFAULT_SIZE = "auto"
DEFAULT_QUALITY = "medium"
DEFAULT_FORMAT = "png"
MIN_PIXELS = 655_360
MAX_PIXELS = 8_294_400
MAX_EDGE = 3840
MAX_RATIO = 3.0
QUALITIES = {"low", "medium", "high", "auto"}
FORMATS = {"png", "jpeg", "jpg", "webp"}


def die(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_prompt(prompt: str | None, prompt_file: str | None) -> str:
    if prompt and prompt_file:
        die("Use --prompt or --prompt-file, not both.")
    if prompt_file:
        return Path(prompt_file).read_text(encoding="utf-8").strip()
    if prompt:
        return prompt.strip()
    die("Missing prompt. Use --prompt or --prompt-file.")


def normalize_format(value: str) -> str:
    value = value.lower()
    if value not in FORMATS:
        die("output-format must be png, jpeg, jpg, or webp.")
    return "jpeg" if value == "jpg" else value


def validate_size(size: str) -> None:
    if size == "auto":
        return
    match = re.fullmatch(r"([1-9][0-9]*)x([1-9][0-9]*)", size)
    if not match:
        die("size must be auto or WIDTHxHEIGHT, for example 1024x1024.")
    width, height = int(match.group(1)), int(match.group(2))
    max_edge = max(width, height)
    min_edge = min(width, height)
    pixels = width * height
    if max_edge > MAX_EDGE:
        die("gpt-image-2 maximum edge length is 3840px.")
    if width % 16 or height % 16:
        die("gpt-image-2 width and height must be multiples of 16px.")
    if max_edge / min_edge > MAX_RATIO:
        die("gpt-image-2 long-to-short ratio must not exceed 3:1.")
    if pixels < MIN_PIXELS or pixels > MAX_PIXELS:
        die("gpt-image-2 total pixels must be between 655360 and 8294400.")


def output_paths(out: str, fmt: str, count: int) -> list[Path]:
    path = Path(out)
    if path.suffix == "":
        path = path.with_suffix(f".{fmt}")
    path.parent.mkdir(parents=True, exist_ok=True)
    if count == 1:
        return [path]
    return [path.with_name(f"{path.stem}-{i}{path.suffix}") for i in range(1, count + 1)]


def payload_from_args(args: argparse.Namespace) -> dict[str, Any]:
    prompt = read_prompt(args.prompt, args.prompt_file)
    fmt = normalize_format(args.output_format)
    validate_size(args.size)
    if args.quality not in QUALITIES:
        die("quality must be low, medium, high, or auto.")
    if args.n < 1 or args.n > 10:
        die("n must be between 1 and 10.")
    payload: dict[str, Any] = {
        "model": MODEL,
        "prompt": prompt,
        "size": args.size,
        "quality": args.quality,
        "n": args.n,
        "output_format": fmt,
    }
    if args.moderation:
        payload["moderation"] = args.moderation
    if args.output_compression is not None:
        if not 0 <= args.output_compression <= 100:
            die("output-compression must be between 0 and 100.")
        payload["output_compression"] = args.output_compression
    return payload


def ensure_api_key() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        die("OPENAI_API_KEY is not set.")


def write_images(response: Any, paths: list[Path]) -> None:
    items = getattr(response, "data", None)
    if not items:
        die("API response did not include image data.")
    for item, path in zip(items, paths):
        b64 = getattr(item, "b64_json", None)
        if not b64 and isinstance(item, dict):
            b64 = item.get("b64_json")
        if not b64:
            die("Image response item did not include b64_json.")
        path.write_bytes(base64.b64decode(b64))
        print(path)


def dry_run(payload: dict[str, Any], paths: list[Path], mode: str, images: list[str] | None = None) -> None:
    preview = {"mode": mode, "payload": payload, "outputs": [str(path) for path in paths]}
    if images:
        preview["images"] = images
    print(json.dumps(preview, indent=2, ensure_ascii=False))


def generate(args: argparse.Namespace) -> None:
    payload = payload_from_args(args)
    fmt = payload["output_format"]
    paths = output_paths(args.out, fmt, args.n)
    if args.dry_run:
        dry_run(payload, paths, "generate")
        return
    ensure_api_key()
    try:
        from openai import OpenAI
    except ImportError:
        die("Missing Python package: openai. Install with `uv pip install openai`.")
    response = OpenAI().images.generate(**payload)
    write_images(response, paths)


def edit(args: argparse.Namespace) -> None:
    payload = payload_from_args(args)
    image_paths = [Path(path) for path in args.image]
    for path in image_paths:
        if not path.exists():
            die(f"Image not found: {path}")
    fmt = payload["output_format"]
    paths = output_paths(args.out, fmt, args.n)
    if args.dry_run:
        dry_run(payload, paths, "edit", [str(path) for path in image_paths])
        return
    ensure_api_key()
    try:
        from openai import OpenAI
    except ImportError:
        die("Missing Python package: openai. Install with `uv pip install openai`.")
    with contextlib_exit_stack(image_paths) as files:
        response = OpenAI().images.edit(image=files, **payload)
    write_images(response, paths)


class contextlib_exit_stack:
    def __init__(self, paths: list[Path]) -> None:
        self.paths = paths
        self.files: list[Any] = []

    def __enter__(self) -> list[Any]:
        self.files = [path.open("rb") for path in self.paths]
        return self.files

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        for file in self.files:
            file.close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate or edit images with gpt-image-2.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_common(sub: argparse.ArgumentParser) -> None:
        sub.add_argument("--prompt")
        sub.add_argument("--prompt-file")
        sub.add_argument("--size", default=DEFAULT_SIZE)
        sub.add_argument("--quality", default=DEFAULT_QUALITY)
        sub.add_argument("--n", type=int, default=1)
        sub.add_argument("--output-format", default=DEFAULT_FORMAT)
        sub.add_argument("--output-compression", type=int)
        sub.add_argument("--moderation", choices=["auto", "low"])
        sub.add_argument("--out", default="output/imagegen/output.png")
        sub.add_argument("--dry-run", action="store_true")

    generate_parser = subparsers.add_parser("generate")
    add_common(generate_parser)
    generate_parser.set_defaults(func=generate)

    edit_parser = subparsers.add_parser("edit")
    add_common(edit_parser)
    edit_parser.add_argument("--image", action="append", required=True)
    edit_parser.set_defaults(func=edit)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
