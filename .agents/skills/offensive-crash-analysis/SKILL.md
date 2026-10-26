---
name: offensive-crash-analysis
description: >
  Crash triage — exploitability assessment, root-cause analysis
---

## Source
https://github.com/SnailSploit/offensive-checklist/blob/main/4-crash-analysis.md

## Trigger phrases
Use this skill when the conversation involves any of:
`crash analysis, crash triage, WinDbg, GDB, ASAN, MSAN, exploitability, stack trace, register dump, segfault, null deref, access violation, week 4`

## Using this skill

Use this methodology selectively; it is a reference, not a mandatory sequence.
Confirm the target and test type are in scope before active testing. Prefer a
minimum-impact proof, stop once the finding is established, and report evidence,
limitations, impact, and remediation with sensitive data redacted.

## Detailed methodology

The full methodology is in [references/methodology.md](references/methodology.md).
Use its headings to locate only the material relevant to the task, and verify
time-sensitive tool behavior and vulnerability details against primary sources.
