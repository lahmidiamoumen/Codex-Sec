#!/usr/bin/env python3
"""Generate claude-skills.json manifest from Skills/ tree.

Reads YAML frontmatter from each SKILL.md and emits a compact JSON manifest
of all skills, grouped by category, for tooling that needs a machine-readable
index of the library.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "Skills"
OUT = ROOT / "claude-skills.json"
PROVENANCE_FIELDS = (
    "schema_version",
    "source_commit",
    "source_ref",
    "source_body_sha256",
)

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def parse_frontmatter(text: str) -> dict:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    block = m.group(1)
    out: dict[str, str] = {}
    current_key: str | None = None
    buf: list[str] = []
    for line in block.splitlines():
        if not line.strip():
            continue
        if ":" in line and not line.startswith(" "):
            if current_key is not None:
                out[current_key] = "\n".join(buf).strip().strip('"')
                buf = []
            key, _, val = line.partition(":")
            current_key = key.strip()
            val = val.strip()
            if val:
                buf.append(val)
        else:
            buf.append(line.strip())
    if current_key is not None:
        out[current_key] = "\n".join(buf).strip().strip('"')
    return out


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print(f"Error: {SKILLS_DIR} not found", file=sys.stderr)
        return 1

    existing_provenance: dict[tuple[str, str], dict] = {}
    if OUT.is_file():
        try:
            previous = json.loads(OUT.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"Error: {OUT} is not valid JSON: {exc}", file=sys.stderr)
            return 1
        for old_entry in previous.get("skills", []):
            if not isinstance(old_entry, dict):
                continue
            key = (old_entry.get("name", ""), old_entry.get("path", ""))
            provenance = {
                field: old_entry[field]
                for field in PROVENANCE_FIELDS
                if field in old_entry
            }
            if provenance:
                existing_provenance[key] = provenance

    manifest: dict = {
        "name": "claude-red",
        "version": "0.3.0",
        "license": "MIT",
        "homepage": "https://github.com/SnailSploit/claude-red",
        "source_repository": "https://github.com/SnailSploit/Claude-Red.git",
        "categories": {},
        "skills": [],
    }

    for category_dir in sorted(SKILLS_DIR.iterdir()):
        if not category_dir.is_dir():
            continue
        category = category_dir.name
        manifest["categories"][category] = []
        for skill_dir in sorted(category_dir.iterdir()):
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.is_file():
                continue
            fm = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
            entry = {
                "name": fm.get("name", skill_dir.name),
                "category": category,
                "path": str(skill_md.relative_to(ROOT)),
                "description": fm.get("description", ""),
            }
            entry.update(existing_provenance.get((entry["name"], entry["path"]), {}))
            manifest["categories"][category].append(entry["name"])
            manifest["skills"].append(entry)

    manifest["skill_count"] = len(manifest["skills"])
    manifest["category_count"] = len(manifest["categories"])

    OUT.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} with {manifest['skill_count']} skills across {manifest['category_count']} categories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
