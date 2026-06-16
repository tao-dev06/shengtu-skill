#!/usr/bin/env python3
"""Generate an image with JOJO Code and save it locally."""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


BASE_URL = "https://api2.jojocode.com/v1"
DEFAULT_MODEL = "gpt-image-2"
DEFAULT_SIZE = "1024x1024"
NO_PROXY_OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def load_local_env() -> None:
    """Load JOJO_API_KEY from nearby private .env.local files if present."""
    candidates = [
        Path(__file__).resolve().parents[1] / ".env.local",
        Path.cwd() / ".env.local",
    ]
    for env_path in candidates:
        if not env_path.exists():
            continue
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip().lstrip("\ufeff")
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def request_json(url: str, api_key: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    last_error: Exception | None = None
    for attempt in range(1, 4):
        try:
            with NO_PROXY_OPENER.open(request, timeout=180) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"API request failed with HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            last_error = exc
            if attempt < 3:
                time.sleep(attempt)

    reason = getattr(last_error, "reason", last_error)
    raise RuntimeError(f"API request failed: {reason}") from last_error


def download_bytes(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"Accept": "image/*,*/*"})
    try:
        with NO_PROXY_OPENER.open(request, timeout=180) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Image download failed with HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Image download failed: {exc.reason}") from exc


def extract_image_bytes(response_json: dict) -> bytes:
    data = response_json.get("data")
    if not isinstance(data, list) or not data:
        raise RuntimeError("API response did not include image data.")

    first = data[0]
    if not isinstance(first, dict):
        raise RuntimeError("API response image item was not an object.")

    b64_json = first.get("b64_json")
    if isinstance(b64_json, str) and b64_json:
        return base64.b64decode(b64_json)

    image_url = first.get("url")
    if isinstance(image_url, str) and image_url:
        return download_bytes(image_url)

    raise RuntimeError("API response did not include b64_json or url.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate an image with JOJO Code and save it locally.",
    )
    parser.add_argument("--prompt", required=True, help="Image description.")
    parser.add_argument("--size", default=DEFAULT_SIZE, help="Image size, such as 1024x1024.")
    parser.add_argument("--output", required=True, help="Output image filename or path.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Image model name.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    load_local_env()

    api_key = os.environ.get("JOJO_API_KEY")
    if not api_key:
        print(
            "Missing JOJO_API_KEY. Set it in the environment or in private .env.local.",
            file=sys.stderr,
        )
        return 2

    endpoint = f"{BASE_URL}/images/generations"
    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "size": args.size,
        "n": 1,
    }

    try:
        response_json = request_json(endpoint, api_key, payload)
        image_bytes = extract_image_bytes(response_json)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    output_path = Path(args.output).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(image_bytes)

    resolved = output_path.resolve()
    print(f"Saved image: {resolved}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
