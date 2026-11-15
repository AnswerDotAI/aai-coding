---
name: persistent-python
description: The persistent clikernel Python session — Jeremy's preferred single tool for nearly ALL Python work. TRIGGER — read and bootstrap as step zero of EVERY session where clikernel is available, before the first tool call other than a Skill load: even tasks that only read a file or search a directory, plus stateful inspection, editing code or notebooks, debugging, experiments, API probes, data transforms, pyskills discovery, notebook-style work, local tool orchestration. If it could go through Python, it goes here — never python -c, Bash heredocs, or ad hoc scripts.
---

# Persistent Python

NB: this file is designed for an LLM reader, not a human. Add it to your LLM's context and ask it to explain.

notation: /why

- `create(kernel="py")`: `py` (ipymini) only; never `python3` or another kernelspec
- startup banner in `create` reply: follow it; says project imports skipped, or missing: tell user before other work, then `exec` `$XDG_CONFIG_HOME/clikernel/startup.py` (default `~/.config/clikernel/startup.py`) whole    /single source of bootstrap imports; never retype from memory

## Environment specifics

- read and search in kernel, never Bash or harness reader: `open_doc` outline, then one section; `view_file` for a file or line range; `rg`; `lnhashview_*` when an edit may follow
- ALL edits (code, tests, config, prose, notebook cells): `exhash`, never harness edit tools; cell or message structure exhash lacks: `aidialog.dlgskill`; rare fallback, for a text edit exhash can't express: `fastcore.tools` file editors
- editing Claude Code's JSON settings: merge into existing keys, never replace; then check for duplicate keys with `json.loads(s, object_pairs_hook=<raiser>)`    /`json.loads` keeps last duplicate silently; codex also reads these files, and its stricter parser rejects them
- `permissions.deny`: bare tool name removes tool from system prompt; scoped rule (`Bash(rm *)`) blocks matching calls only
- Bash, `apply_patch`: don't disable just because clikernel is preferred; first establish sessions misuse them
