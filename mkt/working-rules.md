# Working rules — how marketing files updates

> Ordered by owner 2026-09-22 22:24 UTC after repeated edit slips on the big files.

1. **Updates go in NEW small files, never appended to giant files.** `mkt/TASKS.md` and `mkt/MARKETING_LOG.md` stay as-is; new work gets its own file (one topic per file).
2. New files live where they belong: research in `mkt/research/`, dev notes in `mkt req/`, standing rules here.
3. The agent verifies with `git diff` before every commit. No exceptions.
