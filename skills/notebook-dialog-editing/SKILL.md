---
name: notebook-dialog-editing
description: "Use CLI tools to inspect Python APIs and find, understand, view, and safely edit Jupyter notebooks and aidialog dialogs without a Python kernel. Trigger for .ipynb or dialog work using shell-accessible tools."
---

# Notebook and dialog editing

Use these commands instead of manipulating notebook JSON. Read each command's `--help` only when its use case arises; use `pyskills-doc` for the underlying Python contract when help is not enough.

## Before any notebook edit

**Always run `pyskills-doc nbdev.skill` before editing any notebook.** It defines the notebook-as-source workflow, the required full read, lesson-cell conventions, export rules, and finish checks. This applies to ordinary `.ipynb` files and especially to nbdev source notebooks.

## Choose by use case

- Python API discovery: `pyskills-doc module.symbol`; add `--all` for an elided module listing.
- Hierarchical Markdown/code/notebook reading: `exhash-open PATH`; use a displayed verified token to read one section, or consult `exhash-open --help` for search, paths, links, URLs, and addressed views.
- Search cell sources across notebooks: `rgapi-nbrg PATTERN ROOT`; read `rgapi-nbrg --help` for context, globs, limits, and matching options.
- Orient within one notebook/dialog: `aidialog-summary PATH`.
- Semantic message search: `aidialog-find PATH PATTERN`; it can filter types, errors, exports, headings, IDs, and context. Read `aidialog-find --help` for details.
- Read the complete narrative and outputs: `aidialog-view PATH --out --full-out`; pass a message ID for a targeted view. Multiple IDs are comma-separated.
- Get edit-ready cell lines: `lnhashview-cell PATH CELL_ID`; use its fresh `line|hash|` addresses with `exhash-cell`.
- Edit cell source safely: `exhash-cell PATH CELL_ID COMMAND...`; read `exhash-cell --help` and `pyskills-doc exhash.skill` for the command language. Re-view after every edit call before constructing another.
- Add, delete, or move messages: `aidialog-add`, `aidialog-del`, and `aidialog-move`. IDs are comma-separated; use `--dry-run` when previewing placement or removal. Read the command's help before first use.

For dialog semantics beyond CLI help, run `pyskills-doc aidialog.dlgskill`. For notebook search semantics, run `pyskills-doc rgapi.skill`.

If a structural operation is missing, extend the owning CLI rather than splicing raw `.ipynb` JSON.
