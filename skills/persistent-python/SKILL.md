---
name: persistent-python
description: The persistent clikernel Python session — Jeremy's preferred single tool for nearly ALL Python work. TRIGGER — read and bootstrap as step zero of EVERY session where clikernel is available, before the first tool call other than a Skill load: even tasks that only read a file or search a directory, plus stateful inspection, editing code or notebooks, debugging, experiments, API probes, data transforms, pyskills discovery, notebook-style work, local tool orchestration. If it could go through Python, it goes here — never python -c, Bash heredocs, or ad hoc scripts.
---

# Persistent Python

ALWAYS use the `clikernel` MCP server for ALL Python work: writing code, editing code or notebooks, running or debugging anything, inspecting objects or packages, probing APIs, and transforming data. It is the workbench for every task in this environment. If the work could go through Python, it goes through clikernel. Do not fall back to `python -c`, shell heredocs, or ad hoc scripts.

For Python, `py` (ipymini) is required. Start the kernel with `create(kernel="py")`. Never request `python3` (ipykernel) or another Python kernelspec. Check the clikernel MCP server instructions already in your context before the first call.

Run code with `exec(code=...)` in the selected persistent kernel. Imports, variables, monkeypatches, and cached objects carry across calls. `exec` never creates or switches kernels.

The `create` reply opens with the startup banner: what is imported, and which cells to run next. Follow it. If the banner reports that project imports were skipped, or no banner appears, report that to the user before other work, then run the code in `$XDG_CONFIG_HOME/clikernel/startup.py` (default `~/.config/clikernel/startup.py`) as one `exec` call. That file is the single source of truth for bootstrap imports; never retype them from memory.

This skill does not repeat what the server instructions and startup docs cover: the tools, notebook magics, output format, interaction rules, reload gotchas, and pyskills workflow. `list_pyskills()` shows the available tooling. Prefer a relevant pyskill over ad hoc code.

## Environment specifics

The following apply specifically to this environment:

- After a kernel restart or compaction, read `doc(f)` again for any tooling function whose docs are no longer in your context.
- Read and search through clikernel tools, never Bash or the harness's file reader. For an overview, start with exhash's `open_doc` outline, then open one section. To view a file or a line range, use `view_file` from `fastcore.editskill`. Search with `rgapi`. Switch to `lnhashview_*` once an edit is plausible.
- Use `exhash` for ALL edits: code, tests, config, prose and notebook cells. Never use the harness's built-in file-edit tools. `aidialog.dlgskill` covers the structural cell and message operations that exhash doesn't. `fastcore.tools` file editors are the rare fallback where exhash can't express a text edit.
- Claude Code settings are plain JSON: `~/.claude/settings.json` (user-global), `.claude/settings.json` (project, committed), `.claude/settings.local.json` (project, personal); later files override earlier. Edit them with the normal kernel tooling (`lnhashview_file` + `%%exhash`). Merge into existing keys rather than replacing them. Then check for duplicate keys with `json.loads(s, object_pairs_hook=<raiser>)`. Plain `json.loads` silently keeps the last duplicate, but the stricter serde parsers that also read these files (codex) reject the file outright. A BARE tool name in `permissions.deny` removes that tool from the system prompt entirely, while a scoped rule (`Bash(rm *)`) only blocks matching calls. Hooks go under `"hooks"`, keyed by event (PreToolUse, SessionStart, UserPromptSubmit, ...). `skillOverrides` hides bundled skills: `"off"`, or `"user-invocable-only"` to keep the slash command usable by the user. Settings load at startup, so changes take effect from the next session.
- Codex settings are TOML: `~/.codex/config.toml` is user-global, while trusted `.codex/config.toml` files apply from the project root down to the current directory, with the closest project file winning. CLI overrides have higher precedence. Hooks can live in `hooks.json` or inline `[hooks]` tables at user and project config layers; matching hooks from every active layer are merged. `PreToolUse` can inspect, deny, or rewrite Bash, `apply_patch`, MCP, and most other local tool calls. `[[skills.config]]` entries enable or disable skills by path, while `mcp_servers.<id>.enabled_tools` and `disabled_tools` control which MCP tools are exposed. Do not disable Bash or `apply_patch` merely because clikernel is preferred; first establish that sessions misuse them. Config changes take effect after restarting Codex.
