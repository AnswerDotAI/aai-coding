# Antigravity workflow

notation: /why

- `clikernel` MCP: `aai-coding_clikernel` via `call_mcp_tool` directly; skip schema `read_file` for `create(kernel="py", host?, autoclose?)` and `exec(code)` (schemas for other tools only)    /skips turn-1 schema round-trip
- native `edit_file`/`write_file`: Antigravity artifacts only
- native `read_file`: spilled `.system_generated/steps/*/output.txt` (>10 KB), media (images/PDF/audio/video), Antigravity skills/schemas/artifacts, or whole >10 KB non-notebook after `open_doc` outline
- replies: omit Antigravity plumbing (internal roster states like `waiting`, board seqs, kernel/conversation IDs, passive compliance with defaults, `swarm`'s `open_board` `Run /swarm board...` footer despite its tool hint) unless it changes what the user needs to do or they asked
- markdown file links: always use `file:///absolute/path` with no `#L` fragment; put line numbers in plain text after the link, e.g. `[notes.md](file:///path/to/notes.md) (l240-250)`    /Ghostty blocks schemeless paths and `file://` fragments
- swarms: MUST read `better_swarm` skill before edits or >2-call research, every conversation even without `/swarm`; obsoletes `native_swarm`, `swarm_monitor`, `swarm_narrator`, `swarm_pane`
