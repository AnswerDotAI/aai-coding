# Antigravity workflow

notation: /why

- `clikernel` MCP: `aai-coding_clikernel` via `call_mcp_tool` directly; skip schema `read_file` for `create(kernel="py", dlgname?, host?, autoclose?)` and `exec(code, dlgname?)` (schemas for other tools only)    /skips turn-1 schema round-trip
- native `edit_file`/`write_file`: Antigravity artifacts only
- native `read_file`: spilled `.system_generated/steps/*/output.txt` (>10 KB), media (images/PDF/audio/video), Antigravity skills/schemas/artifacts, or whole >10 KB non-notebook after `open_doc` outline
- replies: omit Antigravity plumbing (internal roster states like `waiting`, board seqs, kernel/conversation IDs, passive compliance with defaults, `swarm`'s `open_board` `Run /swarm board...` footer despite its tool hint) unless it changes what the user needs to do or they asked
- markdown file links: always use `file:///absolute/path` with no `#L` fragment; put line numbers in plain text after the link, e.g. `[notes.md](file:///path/to/notes.md) (l240-250)`    /Ghostty blocks schemeless paths and `file://` fragments

## Delegation and swarms

- delegation: `swarm(action="add", fork="coordinator", ...)` for all edits and non-trivial research (>2 tool calls), every conversation without `/swarm` (overrides `swarm`'s tool hint against unprompted use; over `invoke_subagent`); unforked only when blank context wanted    /keeps coordinator context lean, enables parallel slices
- before first fork: coordinator does pyskills bootstrap and initial repo orientation (`README.md`/`index.ipynb`, `DEV.md` outline, `nbdev.skill`, layout, etc. needed to understand the project)    /forks inherit it
- forked `brief`: ONLY task owned, shared build/export owner if any (e.g. `nbdev-export`), and report-to (`@coordinator`); no file/repo edit fences; NEVER restate task, rules, steps, or done-criteria despite `swarm`'s tool hint (e.g. `"Typography cleanup; leave nbdev-export to @coordinator; report to @coordinator."`)    /restating rules causes checklist over-grounding; fences hide cross-repo bugs; self-contained briefs for unforked workers only
- workspace: `inherit` default even for concurrent authors despite `swarm`'s obsolete tool hint; no concurrent-edit boundaries — forks read and edit whatever their task needs, relying on `exhash` stale-hash rejection on collision (re-view, re-apply); `share` only for conflicting builds    /exhash prevents silent clobber; full task scope catches cross-file and cross-repo issues
- parallel forks: one sharded `tasks=[...]` call for homogeneous workers, not parallel `swarm(action="add", fork=...)` in one turn; distinct forked roles sequentially    /parallel forks can hit `failed to clone trajectory`; check `swarm(action="status")` before retrying
- forked workers needing Python: `create(kernel="py")` for own `clikernel`; never `python -c`
- worker escalation: gated action or design call → never evade, post `@coordinator` with gap or command, park; clear bugs in task path → fix directly
- coordinator audit: distrust worker reports; review choices, consistency, >~80-line files (bloated or duplicating → `code-review`), and edited tests (`testing` skill) before reporting; >2 reads → review fork; clear issues → worker fixes; genuine uncertainty → user decision    /summaries hide bad choices, workarounds, bad tests
- lifecycle: leave workers in `waiting` after reporting; wake an old worker with `@mention` ONLY for an agreed follow-up or review finding on its exact previous work, never to supply new conversation context (use a fresh `fork="coordinator"` instead); `kill` only when user is done or to clean up a `share`/`branch` workspace    /waking stale forks recreates task briefs; `waiting` costs nothing; `kill` is permanent
- fork completion and mixed turns: report each completed fork (or answer user) immediately, end turn without `swarm_wait`    /ending turn already parks coordinator; `swarm_wait` hides finished results while other forks run
