#!/usr/bin/env python3
"""Validate skill package structure for CI."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def find_skill_dirs() -> list[Path]:
    out = []
    for p in ROOT.iterdir():
        if not p.is_dir() or p.name in {".github", "scripts", "dist", "__pycache__"}:
            continue
        if (p / "SKILL.md").exists() and (p / "skill.json").exists():
            out.append(p)
    return sorted(out, key=lambda x: x.name)


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_json_file = skill_dir / "skill.json"
    try:
        data = json.loads(skill_json_file.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return [f"{skill_dir.name}: skill.json is invalid JSON: {exc}"]

    required_keys = ["id", "name", "version", "entry", "files"]
    for key in required_keys:
        if key not in data:
            errors.append(f"{skill_dir.name}: missing key '{key}' in skill.json")

    entry = data.get("entry")
    if isinstance(entry, str):
        entry_file = skill_dir / entry
        if not entry_file.exists():
            errors.append(f"{skill_dir.name}: entry file not found: {entry}")

    files = data.get("files")
    if isinstance(files, list):
        for rel in files:
            if not isinstance(rel, str):
                errors.append(f"{skill_dir.name}: files item is not string: {rel}")
                continue
            if not (skill_dir / rel).exists():
                errors.append(f"{skill_dir.name}: declared file not found: {rel}")

    return errors


def main() -> int:
    skills = find_skill_dirs()
    if not skills:
        print("No valid skill directories found.")
        return 1

    all_errors: list[str] = []
    for skill in skills:
        all_errors.extend(validate_skill(skill))

    if all_errors:
        print("Validation failed:")
        for err in all_errors:
            print(f"- {err}")
        return 1

    print("Validation passed.")
    print("Skills:", ", ".join(s.name for s in skills))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
