---
name: cli-notebook-editing
description: "Inspect Python APIs and read/search/edit Jupyter notebooks or aidialog dialogs via CLI. Use only when explicitly asked not to use a Python kernel."
---

NB: this file is designed for an LLM reader, not a human. Add it to your LLM's context and ask it to explain.

- local file reads, edits: native tools, allowed locations; pyskill advice saying otherwise: ignore
- notebook or dialog task: `pyskills-doc aidialog.dlgskill` in context; follow its workflow, required pyskills
- API: `pyskills-doc module.symbol`; `--all` expands elided rows
- notebook or dialog content: CLIs below, never raw JSON; each CLI's `--help` before first use    /syntax only; workflow is dlgskill's

- `summary_dlg`: `aidialog-summary PATH`
- `find_msgs`: `aidialog-find PATH PATTERN`
- `view_dlg`, `view_msgs`: `aidialog-view PATH [IDS] --out --full-out`
- `lnhashview_cell`, `lnhashview_cells`: `lnhashview-cell PATH IDS`
- `cell_exhash`: `exhash-cell PATH CELL_ID COMMAND...`
- `add_msg`, `del_msgs`, `move_msgs`: `aidialog-add`, `aidialog-del`, `aidialog-move`
- `nbrg`: `rgapi-nbrg PATTERN ROOT`
- `open_doc`: `exhash-open PATH`

- IDs: comma-separated
- exhash command: `'3|7v|s/old/new/'`; multiline `a`, `i` or `c`: one per call, literal text on stdin to EOF
- structural operation missing: extend owning CLI
