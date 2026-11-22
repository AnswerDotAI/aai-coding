---
name: pyskills
description: TRIGGER — read at session start, right after compaction, and before ANY local file, code, notebook, search, edit, web, docs, prose, git/GitHub, debugging, data, browser, or tool task if the full baseline `doc()` outputs and `list_pyskills()` catalog are not currently visible in context. The tooling catalog lives in the kernel, not in this skill list.
---

# Pyskills

- bootstrap (before local file reads, searches, edits, notebook work, or Python execution): if the full uncompacted outputs of `doc(clik, pysk)`, `doc(edsk)`, `doc(dsk)`, `doc(exh)`, `doc(rgsk)`, `doc(acp)`, and `list_pyskills()` are not currently visible in context (a compaction summary mentioning them does not count), MUST run them first in one parallel batch of bare calls via `clikernel`, follow their instructions, and think hard about each tool's capabilities before acting
- each task: match it to `list_pyskills()` rows; `doc(<module>)` for every candidate (doubtful ones too) and `doc(fn)` for functions whose overview row ends in `…` before first use; prefer matching pyskill over ad hoc code or shell
