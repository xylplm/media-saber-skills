#!/usr/bin/env python3
"""One-click SkillHub packager for media-saber skills.

Usage:
  python build_skill.py
  python build_skill.py --skill media-saber-mcp
  python build_skill.py --version 1.0.1
  python build_skill.py --skill media-saber-mcp --version 1.0.1
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Iterable, List
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"

DEFAULT_IGNORE = {
    ".git",
    ".github",
    "__pycache__",
    ".DS_Store",
}


def sha256_of_file(file_path: Path) -> str:
    h = hashlib.sha256()
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def list_skill_dirs(skill_name: str | None) -> List[Path]:
    candidates = [
        p for p in ROOT.iterdir()
        if p.is_dir() and p.name not in DEFAULT_IGNORE and p.name != "dist"
    ]
    if skill_name:
        candidates = [p for p in candidates if p.name == skill_name]
    valid = [p for p in candidates if (p / "SKILL.md").exists() and (p / "skill.json").exists()]
    return sorted(valid, key=lambda x: x.name)


def iter_files(base: Path) -> Iterable[Path]:
    for path in base.rglob("*"):
        if not path.is_file():
            continue
        if any(part in DEFAULT_IGNORE for part in path.parts):
            continue
        yield path


def patch_skill_version(skill_json_path: Path, version: str | None) -> str:
    with skill_json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    current_version = str(data.get("version", "1.0.0"))
    if version and version != current_version:
        data["version"] = version
        with skill_json_path.open("w", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, indent=2, ensure_ascii=True)
            f.write("\n")
        return version
    return current_version


def build_one_skill(skill_dir: Path, version_override: str | None) -> Path:
    skill_json = skill_dir / "skill.json"
    version = patch_skill_version(skill_json, version_override)

    DIST.mkdir(parents=True, exist_ok=True)
    archive_name = f"{skill_dir.name}-{version}.zip"
    out_file = DIST / archive_name

    with ZipFile(out_file, "w", compression=ZIP_DEFLATED) as zf:
        for file_path in iter_files(skill_dir):
            rel = file_path.relative_to(skill_dir)
            zf.write(file_path, arcname=str(rel).replace(os.sep, "/"))

    return out_file


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build SkillHub zip package(s).")
    parser.add_argument("--skill", help="Skill directory name under media-saber-skills")
    parser.add_argument("--version", help="Override version in skill.json before packaging")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    skills = list_skill_dirs(args.skill)
    if not skills:
        print("No valid skill found. Need both SKILL.md and skill.json.")
        return 1

    print(f"Found {len(skills)} skill(s): {', '.join(s.name for s in skills)}")
    outputs = []
    for skill_dir in skills:
        out_file = build_one_skill(skill_dir, args.version)
        digest = sha256_of_file(out_file)
        outputs.append((out_file, digest))

    print("\nBuild completed:")
    for out_file, digest in outputs:
        print(f"- {out_file}")
        print(f"  sha256: {digest}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
