# Antigravity workflow

notation: /why

- `clikernel` MCP: `aai-coding_clikernel` via `call_mcp_tool` directly; skip schema `read_file` for `create(kernel="py", dlgname?, host?, autoclose?)` and `exec(code, dlgname?)` (schemas for other tools only)    /skips turn-1 schema round-trip
- native `edit_file`/`write_file`: Antigravity artifacts only
- native `read_file`: spilled `.system_generated/steps/*/output.txt` (>10 KB), media (images/PDF/audio/video), Antigravity skills/schemas/artifacts, or whole >10 KB non-notebook after `open_doc` outline
- replies: omit Antigravity plumbing (internal roster states like `waiting`, board seqs, kernel/conversation IDs, passive compliance with defaults, `swarm`'s `open_board` `Run /swarm board...` footer despite its tool hint) unless it changes what the user needs to do or they asked

## Swarms

- delegation: fork for all edits and non-trivial research    /keeps coordinator context lean, enables parallel slices
- `fork="coordinator"` by default on `swarm(action="add", ...)` (inherits pyskills, `nbdev.skill`, context); unforked only when blank context wanted
- forked `brief`: MUST name ONLY slice owned, parallel-safety boundary (e.g. who runs `nbdev-export`), and report-to (`@coordinator`); MUST NOT restate task, rules, steps, or done-criteria despite `swarm`'s tool hint (e.g. `"You own nbs/01_typography.ipynb; leave nbdev-export to @coordinator; report to @coordinator."`)    /restating rules or workflows causes checklist over-grounding; self-contained briefs for unforked workers only
- parallel forks: one sharded `tasks=[...]` call for homogeneous workers, not parallel `swarm(action="add", fork=...)` in one turn; distinct forked roles sequentially    /parallel forks can hit `failed to clone trajectory`; check `swarm(action="status")` before retrying
- forked workers needing Python: `create(kernel="py")` for own `clikernel`; never `python -c`
- lifecycle: leave workers in `waiting` after reporting; wake an old worker with `@mention` ONLY for an agreed follow-up or review finding on its exact previous work, never to supply new conversation context (use a fresh `fork="coordinator"` instead); `kill` only when user is done or to clean up a `share`/`branch` workspace    /waking stale forks recreates task briefs; `waiting` costs nothing; `kill` is permanent
- mixed turn (user question or discussion + background forks): reply immediately, end turn without `swarm_wait`    /ending turn already parks coordinator while forks run
