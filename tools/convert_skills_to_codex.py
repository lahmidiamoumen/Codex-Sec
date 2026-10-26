#!/usr/bin/env python3
"""Convert the repository's Claude-style skills into Codex project skills."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import textwrap
from pathlib import Path

from enhance_codex_skills import enhance


ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOT = ROOT / "Skills"
TARGET_ROOT = ROOT / ".agents" / "skills"
MANIFEST = ROOT / "claude-skills.json"


def has_codex_frontmatter(content: str) -> bool:
    return bool(re.match(r"^---\s*\nname:\s*[^\n]+\ndescription:\s*", content))


def section(lines: list[str], title: str) -> list[str]:
    start = None
    for index, line in enumerate(lines):
        if re.match(rf"^##\s+{re.escape(title)}\s*$", line.strip(), re.IGNORECASE):
            start = index + 1
            break
    if start is None:
        return []

    end = len(lines)
    for index in range(start, len(lines)):
        if re.match(r"^##\s+", lines[index].strip()):
            end = index
            break
    return lines[start:end]


def metadata_value(lines: list[str], field: str) -> str:
    pattern = re.compile(rf"^-\s*\*\*{re.escape(field)}\*\*\s*:\s*(.+)$", re.IGNORECASE)
    for line in lines:
        match = pattern.match(line.strip())
        if match:
            return match.group(1).strip()
    return ""


def legacy_to_codex(content: str, source_path: Path) -> str:
    lines = content.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    metadata = section(lines, "Metadata")
    description_lines = section(lines, "Description")
    trigger_lines = section(lines, "Trigger Phrases")

    folder = metadata_value(metadata, "Folder") or source_path.parent.name
    name = re.sub(r"[^a-z0-9]+", "-", folder.lower()).strip("-")
    source = metadata_value(metadata, "Source")
    description = " ".join(line.strip() for line in description_lines if line.strip())
    if not description:
        description = f"Security research methodology for {name}."

    instruction_index = next(
        (
            index
            for index, line in enumerate(lines)
            if re.match(r"^##\s+Instructions for Claude\s*$", line.strip(), re.IGNORECASE)
        ),
        None,
    )
    if instruction_index is None:
        body = "\n".join(lines).strip()
    else:
        body = "\n".join(lines[instruction_index:]).strip()

    trigger_text = "\n".join(line.rstrip() for line in trigger_lines).strip()
    prefix = ["---", f"name: {name}", "description: >"]
    prefix.extend(f"  {line}" for line in textwrap.wrap(description, width=76))
    prefix.extend(["---", ""])
    if source:
        prefix.extend([f"## Source", f"{source}", ""])
    if trigger_text:
        prefix.extend(["## Trigger phrases", trigger_text, ""])
    prefix.append(body)
    return "\n".join(prefix).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", nargs="+", metavar="SKILL", help="Convert only the named skill folders")
    args = parser.parse_args()

    sources = sorted(SOURCE_ROOT.rglob("SKILL.md"))
    all_names = {source.parent.name for source in sources}
    selected = set(args.only) if args.only else None
    if selected is None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        expected = manifest.get("skill_count")
        if len(sources) != expected:
            raise SystemExit(f"Manifest expects {expected} skills under {SOURCE_ROOT}, found {len(sources)}")
    else:
        missing = selected - all_names
        if missing:
            raise SystemExit(f"Unknown source skills: {', '.join(sorted(missing))}")
        sources = [source for source in sources if source.parent.name in selected]

    TARGET_ROOT.mkdir(parents=True, exist_ok=True)
    converted = 0
    legacy = 0

    for source in sources:
        content = source.read_text(encoding="utf-8")
        target_dir = TARGET_ROOT / source.parent.name
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / "SKILL.md"

        if has_codex_frontmatter(content):
            target.write_text(content, encoding="utf-8", newline="\n")
        else:
            target.write_text(legacy_to_codex(content, source), encoding="utf-8", newline="\n")
            legacy += 1
        converted += 1

    print(f"Converted {converted} skills to {TARGET_ROOT}")
    print(f"Translated {legacy} legacy Claude-format skills")
    enhance(skill_names=selected)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
