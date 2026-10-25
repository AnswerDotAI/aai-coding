---
name: cli-notebook-editing
description: "Inspect Python APIs and read/search/edit Jupyter notebooks or aidialog dialogs via CLI. Use only when explicitly asked not to use a Python kernel."
---

- Local file reads/edits: native tools, within allowed locations; ignore conflicting pyskill tool recommendations.
- Every notebook/dialog task: keep `aidialog.dlgskill` documentation in context (`pyskills-doc aidialog.dlgskill`); follow its workflow/required pyskills. API contracts: `pyskills-doc module.symbol`; `--all` expands elided listings.
- Notebook/dialog content: CLI operations below, never raw JSON. Read each CLI's `--help` before first use (syntax, not workflow).

| Python | CLI |
|---|---|
| `summary_dlg` | `aidialog-summary PATH` |
| `find_msgs` | `aidialog-find PATH PATTERN` |
| `view_dlg` / `view_msgs` | `aidialog-view PATH [IDS] --out --full-out` |
| `lnhashview_cell` / `lnhashview_cells` | `lnhashview-cell PATH IDS` |
| `cell_exhash` | `exhash-cell PATH CELL_ID COMMAND...` |
| `add_msg` / `del_msgs` / `move_msgs` | `aidialog-add` / `aidialog-del` / `aidialog-move` |
| `nbrg` | `rgapi-nbrg PATTERN ROOT` |
| `open_doc` | `exhash-open PATH` |

IDs: comma-separated. Exhash: `'3|7v|s/old/new/'`; one multiline `a`/`i`/`c` command accepts literal stdin through EOF. Missing structural operation: extend the owning CLI.
