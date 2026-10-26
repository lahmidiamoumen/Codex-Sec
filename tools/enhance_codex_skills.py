#!/usr/bin/env python3
"""Apply Codex-focused cleanup to the project's migrated security skills."""

from __future__ import annotations

import argparse
import json
import re
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = ROOT / ".agents" / "skills"
SOURCE_ROOT = ROOT / "Skills"
README = ROOT / "README.md"
MANIFEST = ROOT / "claude-skills.json"
ENHANCEMENTS = ROOT / "claude-skills-enhancements.json"
LONG_SKILL_LINE_LIMIT = 1000

USING_SKILL = """## Using this skill

Use this methodology selectively; it is a reference, not a mandatory sequence.
Confirm the target and test type are in scope before active testing. Prefer a
minimum-impact proof, stop once the finding is established, and report evidence,
limitations, impact, and remediation with sensitive data redacted.
"""

LONG_REFERENCE_NOTE = """## Detailed methodology

The full methodology is in [references/methodology.md](references/methodology.md).
Use its headings to locate only the material relevant to the task, and verify
time-sensitive tool behavior and vulnerability details against primary sources.
"""

NETEXEC_DESCRIPTION = (
    "NetExec (nxc) methodology for authorized network security assessments. Use "
    "when reviewing scoped SMB, LDAP, WinRM, RDP, or related service exposure and "
    "authentication controls."
)


def read_readme_descriptions() -> dict[str, str]:
    descriptions: dict[str, str] = {}
    row = re.compile(r"^\|\s*\[`([^`]+)`\]\([^)]*\)\s*\|\s*(.*?)\s*\|$")
    for line in README.read_text(encoding="utf-8").splitlines():
        match = row.match(line)
        if match:
            descriptions[match.group(1)] = re.sub(r"\s+", " ", match.group(2)).strip()
    descriptions["offensive-netexec"] = NETEXEC_DESCRIPTION
    return descriptions


def read_enhancements() -> dict[str, dict[str, str]]:
    data = json.loads(ENHANCEMENTS.read_text(encoding="utf-8"))
    return {
        item["name"]: item["enhanced_content"]
        for item in data.get("skills", [])
        if item.get("name") and item.get("enhanced_content")
    }


def replace_assessment_notes(
    content: str, enhancement: dict[str, str], path: Path
) -> tuple[str, bool]:
    title = "## Codex assessment notes"
    fields = (
        ("Purpose", "purpose"),
        ("Safe validation", "safe_validation"),
        ("Defender acceptance", "defender_acceptance"),
        ("Interpretation check", "interpretation_check"),
    )
    lines = [title, ""]
    for label, key in fields:
        value = enhancement.get(key, "").strip()
        if value:
            lines.extend([f"**{label}:** {value}", ""])
    block = "\n".join(lines).rstrip() + "\n"

    existing = re.search(r"(?m)^## Codex assessment notes\s*$", content)
    if existing:
        next_heading = re.search(r"(?m)^##\s+", content[existing.end() :])
        end = existing.end() + next_heading.start() if next_heading else len(content)
        suffix = content[end:].lstrip("\n")
        updated = content[: existing.start()].rstrip() + "\n\n" + block
        if suffix:
            updated += "\n" + suffix
        return updated, updated != content

    updated = content.rstrip() + "\n\n" + block
    return updated, updated != content


def replace_description(content: str, description: str, path: Path) -> tuple[str, bool]:
    frontmatter = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", content, re.DOTALL)
    if not frontmatter:
        raise ValueError(f"Missing YAML frontmatter: {path}")

    lines = frontmatter.group(1).splitlines()
    start = next((i for i, line in enumerate(lines) if line.startswith("description:")), None)
    if start is None:
        raise ValueError(f"Missing description field: {path}")

    end = start + 1
    while end < len(lines) and (lines[end].startswith(" ") or lines[end].startswith("\t")):
        end += 1

    replacement = ["description: >"]
    replacement.extend(
        "  " + line
        for line in textwrap.wrap(description, width=76, break_long_words=False, break_on_hyphens=False)
    )
    changed = lines[start:end] != replacement
    if not changed:
        return content, False

    lines[start:end] = replacement
    updated_frontmatter = "---\n" + "\n".join(lines) + "\n---\n"
    return updated_frontmatter + content[frontmatter.end() :], True


def replace_claude_block(content: str, path: Path) -> tuple[str, bool]:
    start = re.search(r"(?m)^## Instructions for Claude\s*$", content)
    if not start:
        return content, False
    end = re.search(r"(?m)^## Full Methodology\s*$", content[start.end() :])
    if not end:
        raise ValueError(f"Claude instructions without Full Methodology section: {path}")

    methodology_start = start.end() + end.start()
    updated = content[: start.start()] + USING_SKILL + "\n" + content[methodology_start:]
    return updated, True


def split_long_methodology(content: str, path: Path) -> tuple[str, bool, str | None]:
    line_count = len(content.splitlines())
    if line_count <= LONG_SKILL_LINE_LIMIT:
        return content, False, None

    marker = re.search(r"(?m)^## Full Methodology\s*$", content)
    if not marker:
        raise ValueError(f"Long skill has no Full Methodology section: {path}")

    reference_content = content[marker.start() :].rstrip() + "\n"
    reference_path = path.parent / "references" / "methodology.md"
    if reference_path.exists():
        existing = reference_path.read_text(encoding="utf-8")
        if existing != reference_content:
            raise FileExistsError(f"Refusing to overwrite existing reference: {reference_path}")

    main_content = content[: marker.start()].rstrip() + "\n\n" + LONG_REFERENCE_NOTE
    return main_content, True, reference_content


def enhance(dry_run: bool = False, skill_names: set[str] | None = None) -> int:
    skills = sorted(SKILLS_ROOT.glob("*/SKILL.md"))
    if skill_names is None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        expected = manifest.get("skill_count")
        if len(skills) != expected:
            raise SystemExit(f"Manifest expects {expected} skills, found {len(skills)} under {SKILLS_ROOT}")
    else:
        available = {path.parent.name for path in skills}
        missing = skill_names - available
        if missing:
            raise SystemExit(f"Missing selected Codex skills: {', '.join(sorted(missing))}")
        skills = [path for path in skills if path.parent.name in skill_names]

    descriptions = read_readme_descriptions()
    enhancements = read_enhancements()
    counts = {"descriptions": 0, "claude_blocks": 0, "split": 0, "assessment_notes": 0}
    updates: list[tuple[Path, str, Path | None, str | None]] = []

    for path in skills:
        name = path.parent.name
        if name not in descriptions:
            raise SystemExit(f"No concise description available for {name}")

        original = path.read_text(encoding="utf-8")
        updated, desc_changed = replace_description(original, descriptions[name], path)
        updated, claude_changed = replace_claude_block(updated, path)
        notes_changed = False
        if name in enhancements:
            updated, notes_changed = replace_assessment_notes(updated, enhancements[name], path)
        updated, split, reference_content = split_long_methodology(updated, path)

        counts["descriptions"] += int(desc_changed)
        counts["claude_blocks"] += int(claude_changed)
        counts["split"] += int(split)
        counts["assessment_notes"] += int(notes_changed)

        reference_path = path.parent / "references" / "methodology.md" if split else None
        if updated != original:
            updates.append((path, updated, reference_path, reference_content if split else None))

    print(f"Skills selected: {len(skills)}")
    print(f"Descriptions refreshed from README: {counts['descriptions']}")
    print(f"Claude-only instruction blocks rewritten: {counts['claude_blocks']}")
    print(f"Long methodologies moved to references: {counts['split']}")
    print(f"Codex assessment-note sections updated: {counts['assessment_notes']}")
    if dry_run:
        print("Dry run only; no skill files changed.")
        return 0

    for path, updated, reference_path, reference_content in updates:
        if reference_path is not None and reference_content is not None:
            reference_path.parent.mkdir(parents=True, exist_ok=True)
            reference_path.write_text(reference_content, encoding="utf-8", newline="\n")
        path.write_text(updated, encoding="utf-8", newline="\n")

    print(f"Updated {len(updates)} skill entrypoints under {SKILLS_ROOT}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Report planned changes without writing files")
    parser.add_argument("--only", nargs="+", metavar="SKILL", help="Enhance only the named skill folders")
    args = parser.parse_args()
    return enhance(dry_run=args.dry_run, skill_names=set(args.only) if args.only else None)


if __name__ == "__main__":
    raise SystemExit(main())
