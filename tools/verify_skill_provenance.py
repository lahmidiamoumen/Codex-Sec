#!/usr/bin/env python3
"""Verify upstream commit pins and SKILL.md body hashes in the manifest."""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "claude-skills.json"
EXPECTED_SOURCE = "https://github.com/SnailSploit/Claude-Red.git"
TRACKING_REMOTE = "upstream-claude-red"
SCHEMA_VERSION = 1
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
REF_RE = re.compile(r"^refs/(?:heads/main|pull/([1-9][0-9]*)/head)$")
FRONTMATTER_RE = re.compile(rb"\A---\r?\n.*?\r?\n---(?:\r?\n|\Z)", re.DOTALL)


def git(*args: str, check: bool = True, text: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
    )


def tracking_ref(source_ref: str) -> str:
    if source_ref == "refs/heads/main":
        return f"refs/remotes/{TRACKING_REMOTE}/main"
    match = REF_RE.fullmatch(source_ref)
    if match and match.group(1):
        return f"refs/remotes/{TRACKING_REMOTE}/pr/{match.group(1)}"
    raise ValueError(f"unsupported source_ref: {source_ref}")


def fetch_source_refs(entries: list[dict]) -> None:
    source_refs: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("manifest contains a non-object skill entry")
        source_ref = entry.get("source_ref")
        if not isinstance(source_ref, str) or not REF_RE.fullmatch(source_ref):
            raise ValueError(f"unsupported source_ref: {source_ref}")
        source_refs.add(source_ref)
    if "refs/heads/main" not in source_refs:
        raise ValueError("manifest does not pin the upstream main branch")

    remote_url = git("remote", "get-url", TRACKING_REMOTE, check=False)
    if remote_url.returncode != 0:
        git("remote", "add", TRACKING_REMOTE, EXPECTED_SOURCE)
    elif remote_url.stdout.strip() != EXPECTED_SOURCE:
        raise ValueError(f"{TRACKING_REMOTE} points to an unexpected repository")

    pr_fetch_refspec = (
        f"+refs/pull/*/head:refs/remotes/{TRACKING_REMOTE}/pr/*"
    )
    configured = git(
        "config",
        "--get-all",
        f"remote.{TRACKING_REMOTE}.fetch",
        check=False,
    )
    if pr_fetch_refspec not in configured.stdout.splitlines():
        git(
            "config",
            "--add",
            f"remote.{TRACKING_REMOTE}.fetch",
            pr_fetch_refspec,
        )

    refspecs = [
        f"+refs/heads/main:refs/remotes/{TRACKING_REMOTE}/main"
    ]
    for source_ref in sorted(source_refs):
        if source_ref == "refs/heads/main":
            continue
        match = REF_RE.fullmatch(source_ref)
        if not match or not match.group(1):
            raise ValueError(f"unsupported source_ref: {source_ref}")
        number = match.group(1)
        refspecs.append(
            f"+refs/pull/{number}/head:refs/remotes/{TRACKING_REMOTE}/pr/{number}"
        )

    shallow = git("rev-parse", "--is-shallow-repository").stdout.strip() == "true"
    fetch_args = ["git", "fetch", "--no-tags"]
    if shallow:
        fetch_args.append("--unshallow")
    subprocess.run(
        [*fetch_args, TRACKING_REMOTE, *refspecs],
        cwd=ROOT,
        check=True,
    )
    if git("rev-parse", "--is-shallow-repository").stdout.strip() != "false":
        raise ValueError("source fetch left a shallow repository; full history is required")


def read_skill_at(commit: str, path: str) -> bytes:
    return git("show", f"{commit}:{path}", text=False).stdout


def body_sha256(blob: bytes) -> str:
    frontmatter = FRONTMATTER_RE.match(blob)
    body = blob[frontmatter.end() :] if frontmatter else blob
    return hashlib.sha256(body).hexdigest()


def frontmatter_bytes(blob: bytes) -> bytes:
    match = FRONTMATTER_RE.match(blob)
    return blob[: match.end()] if match else b""


def report_frontmatter_diff(
    name: str,
    source_commit: str,
    source_ref: str,
    pinned_blob: bytes,
    current_blob: bytes,
) -> None:
    pinned = frontmatter_bytes(pinned_blob)
    current = frontmatter_bytes(current_blob)
    if pinned == current:
        return

    print(
        f"WARNING: {name}: upstream frontmatter changed since the pin "
        "(advisory; body hash excludes frontmatter)."
    )
    old_lines = pinned.decode("utf-8", errors="replace").splitlines(keepends=True)
    new_lines = current.decode("utf-8", errors="replace").splitlines(keepends=True)
    diff = difflib.unified_diff(
        old_lines,
        new_lines,
        fromfile=f"{name}@{source_commit[:12]}",
        tofile=f"{name}@{source_ref}",
    )
    for line in diff:
        print(line, end="")


def validate_entry(entry: dict, max_path_commits: int) -> list[str]:
    errors: list[str] = []
    name = entry.get("name", "<unnamed>")
    commit = entry.get("source_commit", "")
    source_ref = entry.get("source_ref", "")
    expected_hash = entry.get("source_body_sha256", "")
    path = entry.get("path", "")

    if entry.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"{name}: schema_version must be {SCHEMA_VERSION}")
    if not isinstance(commit, str) or not COMMIT_RE.fullmatch(commit):
        errors.append(f"{name}: source_commit must be a full lowercase SHA-1")
        return errors
    if not isinstance(expected_hash, str) or not HASH_RE.fullmatch(expected_hash):
        errors.append(f"{name}: source_body_sha256 must be a lowercase SHA-256")
        return errors
    if not isinstance(path, str):
        errors.append(f"{name}: path must be a string")
        return errors
    if not isinstance(source_ref, str) or not REF_RE.fullmatch(source_ref):
        errors.append(f"{name}: source_ref is invalid or unsupported")
        return errors

    pure_path = PurePosixPath(path)
    if (
        pure_path.is_absolute()
        or ".." in pure_path.parts
        or not path.startswith("Skills/")
        or pure_path.name != "SKILL.md"
    ):
        errors.append(f"{name}: source path must stay inside Skills/")
        return errors

    try:
        remote_ref = tracking_ref(source_ref)
        git("cat-file", "-e", f"{commit}^{{commit}}")
        if source_ref.startswith("refs/pull/"):
            current_commit = git("rev-parse", f"{remote_ref}^{{commit}}").stdout.strip()
            if current_commit != commit:
                errors.append(
                    f"{name}: pinned commit is not the current PR head; "
                    "review and refresh the pin"
                )
                return errors
        else:
            ancestry = git(
                "merge-base",
                "--is-ancestor",
                commit,
                remote_ref,
                check=False,
            )
            if ancestry.returncode != 0:
                errors.append(f"{name}: pinned commit is not an ancestor of {source_ref}")
                return errors

            path_commits_result = git(
                "rev-list",
                "--count",
                f"{commit}..{remote_ref}",
                "--",
                path,
            )
            path_commits = int(path_commits_result.stdout.strip())
            if path_commits > max_path_commits:
                print(
                    f"WARNING: {name}: source path changed in {path_commits} commits "
                    f"since its pin (advisory threshold: {max_path_commits})."
                )

        pinned_blob = read_skill_at(commit, path)
        current_blob = read_skill_at(remote_ref, path)
        report_frontmatter_diff(name, commit, source_ref, pinned_blob, current_blob)

        pinned_hash = body_sha256(pinned_blob)
        if pinned_hash != expected_hash:
            errors.append(f"{name}: body hash does not match source_commit")

        current_hash = body_sha256(current_blob)
        if current_hash != expected_hash:
            errors.append(
                f"{name}: upstream SKILL.md body changed since pin; review and refresh it"
            )
    except (subprocess.CalledProcessError, ValueError) as exc:
        detail = (
            exc.stderr.strip()
            if isinstance(exc, subprocess.CalledProcessError) and exc.stderr
            else str(exc)
        )
        errors.append(f"{name}: provenance check failed: {detail}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--max-path-commits",
        type=int,
        default=int(os.environ.get("CODEX_SEC_MAX_SOURCE_PATH_COMMITS", "100")),
        help="advisory threshold for commits changing a pinned source path (default: 100)",
    )
    parser.add_argument(
        "--no-fetch",
        action="store_true",
        help="use already-fetched upstream-claude-red refs",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="pin each entry to its current source ref and write the manifest",
    )
    args = parser.parse_args()
    if args.max_path_commits < 0:
        parser.error("--max-path-commits must be zero or greater")

    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        if not isinstance(manifest, dict):
            raise ValueError("manifest root must be an object")
        if manifest.get("source_repository") != EXPECTED_SOURCE:
            raise ValueError("source_repository does not match the approved upstream")
        entries = manifest.get("skills")
        if not isinstance(entries, list) or not entries:
            raise ValueError("manifest skills must be a non-empty array")
        if manifest.get("skill_count") != len(entries):
            raise ValueError("skill_count does not match the skills array")
        categories = manifest.get("categories")
        if not isinstance(categories, dict):
            raise ValueError("categories must be an object")
        if manifest.get("category_count") != len(categories):
            raise ValueError("category_count does not match categories")

        category_members: dict[str, str] = {}
        for category, names_in_category in categories.items():
            if not isinstance(names_in_category, list):
                raise ValueError(f"category {category} must contain a name array")
            for skill_name in names_in_category:
                if not isinstance(skill_name, str) or skill_name in category_members:
                    raise ValueError(
                        f"invalid or duplicate skill in category index: {skill_name}"
                    )
                category_members[skill_name] = category
        for entry in entries:
            if not isinstance(entry, dict):
                raise ValueError("manifest contains a non-object skill entry")
            if category_members.get(entry.get("name")) != entry.get("category"):
                raise ValueError(
                    f"{entry.get('name', '<unnamed>')}: category index does not match entry"
                )

        if not args.no_fetch:
            fetch_source_refs(entries)

        if args.refresh:
            for entry in entries:
                if not isinstance(entry, dict):
                    raise ValueError("manifest contains a non-object skill entry")
                name = entry.get("name", "<unnamed>")
                path = entry.get("path")
                source_ref = entry.get("source_ref")
                if not isinstance(path, str) or not isinstance(source_ref, str):
                    raise ValueError(f"{name}: path and source_ref are required to refresh")
                remote_ref = tracking_ref(source_ref)
                commit = git("rev-parse", f"{remote_ref}^{{commit}}").stdout.strip()
                if not COMMIT_RE.fullmatch(commit):
                    raise ValueError(f"{name}: could not resolve source commit")
                entry["schema_version"] = SCHEMA_VERSION
                entry["source_commit"] = commit
                entry["source_body_sha256"] = body_sha256(read_skill_at(commit, path))
            MANIFEST.write_text(
                json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            print(
                f"Refreshed provenance pins for {len(entries)} skills. "
                "Review the manifest and upstream skill diffs before committing."
            )
            return 0

        errors: list[str] = []
        names: set[str] = set()
        for entry in entries:
            if not isinstance(entry, dict):
                errors.append("manifest contains a non-object skill entry")
                continue
            name = entry.get("name")
            if not isinstance(name, str) or not name:
                errors.append("skill name must be a non-empty string")
                continue
            if name in names:
                errors.append(f"duplicate skill name: {name}")
            names.add(name)
            errors.extend(validate_entry(entry, args.max_path_commits))

        if errors:
            print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
            return 1
        main_pins = sum(entry["source_ref"] == "refs/heads/main" for entry in entries)
        pr_pins = len(entries) - main_pins
        print(
            f"Verified {main_pins} main pins (ancestry and body hash) and "
            f"{pr_pins} PR pins (exact head and body hash). "
            f"Path-touch threshold {args.max_path_commits} is advisory."
        )
        return 0
    except (OSError, json.JSONDecodeError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
