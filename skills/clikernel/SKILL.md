---
name: kernel-notebook-editing
description: "Use kernel tools to inspect Python APIs and find, understand, view, and safely edit Jupyter notebooks and aidialog dialogs."
---

notation: /why

- kernel MCP tools: main Python workbench; call `exec` directly; lifecycle tools only when it reports no kernel, or for explicit kernel management
- never stop or delete kernels as cleanup; exception: extra kernels you created for a diagnostic: `delete_kernel` when done    /session-created ones stop at session end; selected ones aren't yours
- state persists: keep imports, fixtures, results, timing helpers
- no writable-root limit: user-authorized work on paths outside shell's workspace too
- reusable logic: importable project functions, called from kernel for exploration, timings, comparisons, artifacts; no thin scripts to invoke them
- IMPORTANT: kernel ≠ Bash replacement, whatever a pyskill says
- kernel, inspectors or a library's parallel machinery fit task badly: stop, report    /don't hide it with shell or script workaround

## Bootstrap

- kernel this session creates: `~/.config/clikernel/startup.py` already ran: skill modules under short aliases, `doc`, `list_pyskills` loaded; no import cell; follow any banner; `restart` reruns startup only in these kernels
- before first kernel use in a context, and after compaction: read the startup docs in parallel (`doc(clik, pysk)`, `doc(edsk)`, `doc(dsk)`, `doc(exh)`, `doc(rgsk)`, `doc(acp)`, `list_pyskills()`), each a bare expression    /compaction drops docs; `--quiet` hides the banner; single-module calls stay under 10 KB
- kernel restart or reconnect, Codex or MCP restart, user saying so included: runtime state lost, context kept: no bootstrap; restore only imports, state task needs; ≠ compaction: check visible context
- inspector feedback: follow, don't bypass

## Editing

- exhash: text inside cells; edits where a patch would repeat much unchanged text
- `apply_patch`: short contiguous changes, clearer as old + new; local files only
- aidialog: structural cell operations, e.g. add, delete, move, run cells
- straightforward text changes: prefer these tools over ad hoc scripts
- remote files, in that host's kernel: `doc(edsk, exh)` first, then `lnhashview_file` → `file_exhash`; never copy locally or build shell substitutions
- remote Git, builds, shell: SSH

## Payload text

- text args over two words in kernel calls (patterns, replacements, message bodies, code): `r'''...'''`; text contains `'''`: `r"""..."""`    /no interpolation, no escaping; plain quotes silently concatenate around embedded quotes
- multiline: literal line breaks, never `\n`    /call shows the exact text received

```python
add_msg(r'''First line of the note.
Second line of the note.''', msg_type='note')
cell_exhash(r'''nbs/00_core.ipynb''', r'''54276565''',
    (r'''1|v2|''', 's', r'''kc\.execute\("'FOREIGN'"\)''', r'''foreign_id = kc.execute("'FOREIGN'")'''))
```

- `%%exhash` body: unquoted

## Hosts

- [rustygate](https://github.com/AnswerDotAI/rustygate): per-machine gateway that owns kernels; `clikernel`: stdio router that reaches other machines, containers by `host` name
- host: machine whose files and Python task needs; all execution, paths are that host's; identity matters → check hostname, cwd
- add a machine: rustygate README, "Running as a service"; then name it in `~/.config/clikernel/gateways.toml`
- own `[mcp_servers.<name>]` HTTP block instead: bypasses router; kernels come up bare: no startup.py, no conversation cwd or env
