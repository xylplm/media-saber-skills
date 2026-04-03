#!/usr/bin/env python3
"""Publish built skill zip packages to ClawHub via HTTP upload API.

Required env vars:
- CLAWHUB_UPLOAD_URL
- CLAWHUB_TOKEN

Optional env vars:
- CLAWHUB_TOKEN_HEADER (default: Authorization)
- CLAWHUB_TOKEN_PREFIX (default: Bearer)
- CLAWHUB_FILE_FIELD (default: file)
- CLAWHUB_TIMEOUT_SECONDS (default: 60)
"""

from __future__ import annotations

import json
import mimetypes
import os
import sys
import uuid
from pathlib import Path
from urllib import request

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


def env(name: str, default: str | None = None, required: bool = False) -> str:
    value = os.getenv(name, default)
    if required and not value:
        raise RuntimeError(f"Missing required env: {name}")
    return value or ""


def build_multipart(file_field: str, file_path: Path) -> tuple[bytes, str]:
    boundary = f"----clawhub-boundary-{uuid.uuid4().hex}"
    content_type = f"multipart/form-data; boundary={boundary}"

    mime_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
    file_bytes = file_path.read_bytes()

    lines = []
    lines.append(f"--{boundary}\r\n".encode("utf-8"))
    lines.append(
        (
            f'Content-Disposition: form-data; name="{file_field}"; '
            f'filename="{file_path.name}"\r\n'
        ).encode("utf-8")
    )
    lines.append(f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8"))
    lines.append(file_bytes)
    lines.append(b"\r\n")
    lines.append(f"--{boundary}--\r\n".encode("utf-8"))

    return b"".join(lines), content_type


def publish_one(upload_url: str, token_header: str, token_value: str, file_field: str, timeout_s: int, zip_file: Path) -> None:
    body, content_type = build_multipart(file_field, zip_file)

    req = request.Request(upload_url, data=body, method="POST")
    req.add_header("Content-Type", content_type)
    req.add_header("Accept", "application/json")
    req.add_header(token_header, token_value)

    with request.urlopen(req, timeout=timeout_s) as resp:  # noqa: S310
        raw = resp.read().decode("utf-8", errors="replace")
        print(f"Published: {zip_file.name} -> HTTP {resp.status}")
        if raw.strip():
            try:
                parsed = json.loads(raw)
                print(json.dumps(parsed, ensure_ascii=False))
            except Exception:  # noqa: BLE001
                print(raw)


def main() -> int:
    upload_url = env("CLAWHUB_UPLOAD_URL", required=True)
    token = env("CLAWHUB_TOKEN", required=True)
    token_header = env("CLAWHUB_TOKEN_HEADER", "Authorization")
    token_prefix = env("CLAWHUB_TOKEN_PREFIX", "Bearer")
    file_field = env("CLAWHUB_FILE_FIELD", "file")
    timeout_s = int(env("CLAWHUB_TIMEOUT_SECONDS", "60"))

    if token_prefix:
        token_value = f"{token_prefix} {token}".strip()
    else:
        token_value = token

    zips = sorted(DIST.glob("*.zip"))
    if not zips:
        print("No zip files found under dist/. Run build first.")
        return 1

    for zip_file in zips:
        publish_one(upload_url, token_header, token_value, file_field, timeout_s, zip_file)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(f"Publish failed: {exc}")
        raise
