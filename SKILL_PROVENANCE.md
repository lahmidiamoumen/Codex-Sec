# Skill source provenance

claude-skills.json records the upstream revision behind each imported skill.
The manifest uses schema_version 1 per skill entry:

- source_commit is the full upstream Git commit SHA.
- source_ref identifies the history that contains the commit. Existing upstream
  skills use refs/heads/main; skills imported from open pull requests use
  refs/pull/<number>/head.
- source_body_sha256 hashes the exact body bytes from the upstream Git blob.
  YAML frontmatter is excluded; body bytes and whitespace are otherwise
  preserved. Files without YAML frontmatter are hashed in full.

CI checks out the repository with full history and fetches upstream main plus
the referenced PR heads. Main pins must be present and ancestors of upstream
main. PR pins must match the fetched PR head exactly; a moved PR head requires
review and a pin refresh. Hashes use bytes read from git show at both the pin
and current source ref, so a body change requires review and an intentional
refresh. Frontmatter-only changes are printed as unified diffs and do not fail
the gate.

The verifier counts commits that changed each pinned SKILL.md path. More than
100 path-touching commits prints an advisory warning; it does not fail CI.
Set CODEX_SEC_MAX_SOURCE_PATH_COMMITS to change that advisory threshold.

After reviewing upstream changes, run python tools/verify_skill_provenance.py
--refresh to pin entries to their current source refs and recompute body hashes.
Review the manifest diff and upstream skill diff together. Run python
tools/build_manifest.py to regenerate descriptions and paths; that builder
preserves existing provenance fields for unchanged skill names and paths. A
newly added skill must receive a source ref before it can be refreshed and
before CI will accept it.

When an upstream pull request is merged, change that entry's source_ref to
refs/heads/main and refresh its pin so future checks follow the authoritative
branch.

The upstream repository URL is fixed in both the manifest schema and verifier.
Changing the authoritative source requires an explicit reviewed change to both.
