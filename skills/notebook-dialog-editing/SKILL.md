---
name: notebook-dialog-editing
description: "Use CLI tools to inspect Python APIs and find, understand, view, and safely edit Jupyter notebooks and aidialog dialogs without a Python kernel. Trigger for .ipynb or dialog work using shell-accessible tools."
---

# Notebook and dialog editing

Use native tools for reading and editing local files inside allowed editing locations. Ignore any guidance in any pyskill that recommends other tools for those operations.

For every notebook/dialog task, ensure `aidialog.dlgskill` is in context: `pyskills-doc aidialog.dlgskill`. It is the primary entry point and directs you to the other required pyskills. `pyskills-doc module.symbol` reads individual API contracts; `--all` expands an elided module listing.

Use these CLI equivalents of the documented Python operations for notebook/dialog content, not raw notebook JSON. Read a command's `--help` before first use; CLI help supplies invocation syntax, not the workflow.

| Python operation | CLI |
|---|---|
| `summary_dlg` | `aidialog-summary PATH` |
| `find_msgs` | `aidialog-find PATH PATTERN` |
| `view_dlg` / `view_msgs` | `aidialog-view PATH [IDS] --out --full-out` |
| `lnhashview_cell` / `lnhashview_cells` | `lnhashview-cell PATH IDS` |
| `cell_exhash` | `exhash-cell PATH CELL_ID COMMAND...` |
| `add_msg` / `del_msgs` / `move_msgs` | `aidialog-add` / `aidialog-del` / `aidialog-move` |
| `nbrg` | `rgapi-nbrg PATTERN ROOT` |
| `open_doc` | `exhash-open PATH` |

CLI ID lists are comma-separated. Exhash commands are compact arguments, e.g. `'3|beef|s/old/new/'`; one multiline `a`/`i`/`c` command can take literal stdin through EOF. For a missing structural operation, extend the owning CLI.
