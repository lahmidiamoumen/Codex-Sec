# Claude-Red Codex skill guidance

These instructions apply when using skills under `.agents/skills/offensive-*`.
They do not constrain ordinary repository work.

- Treat a skill as methodology, not authorization. Before active testing,
  confirm written authorization, exact assets, accounts, permitted methods, and
  test window; ask when the target or impact limits are unclear.
- Prefer passive and low-impact checks. Stop after the minimum proof needed.
  Disruptive tests, credential capture, persistence, evasion, lateral movement,
  and data extraction require explicit authorization for that activity and
  target.
- Capture a baseline, make one controlled change per test, and independently
  verify any claimed effect. Stop if testing reaches real-user data, external
  recipients, privileged access, destructive state, or an unapproved system.
- Use test accounts and synthetic data where practical. Do not retain unrelated
  personal or sensitive data; redact secrets from evidence.
- Report the target, method, evidence, limitations, impact, and remediation.
  Separate confirmed observations from inference.
- Record cleanup steps and regression criteria so the owner can safely retest.
- Verify time-sensitive CVEs, firmware behavior, and tool options against
  primary sources before relying on them.
