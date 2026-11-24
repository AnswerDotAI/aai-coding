---
name: better_swarm
description: "Antigravity swarm orchestration: read BEFORE any edits or non-trivial research (>2 tool calls). Obsoletes native_swarm, swarm_monitor, swarm_narrator, and swarm_pane."
---

notation: /why

- obsoletes: `native_swarm` (`/swarm`), `swarm_monitor`, `swarm_narrator`, `swarm_pane`; never read or spawn them (no `monitor` or `narrator` workers)
- roles: `main` = user-facing session (`swarm` tool roster name: `coordinator` → `fork="coordinator"`, `@coordinator`); workers = agents on shared board
- scope: edits, >2-call research, builds, tests, reviews — every conversation, even without `/swarm` (overrides `swarm` tool hint; over `invoke_subagent`); quick read-only user lookup: inline fine; post-compaction: re-read before new forks

Tool|Role
-|-
`swarm`|`status`, `models`, `add`, `model`, `kill`, `title`, `channel` (when offered)
`post_message`|assign, check in, coordinate (`@name`, `@all`, `@#channel`)
`read_board`|read posts (`since:N`, `seqs:[...]`, `channel`); `since:0` = full history
`swarm_wait`|free sleep until post after highest seen `since` (not board head); `mentions_only:false` wakes for any post

- board tools (`post_message`, `read_board`, `swarm_wait`): upfront or one turn after first `swarm(action="add")`

## main

- job: read, judge, decide, orchestrate; no inline technical work    /inline work starves orchestration, blocks user
- pre-fork: pyskills bootstrap + repo orientation (`README.md`/`index.ipynb`, `DEV.md` outline, `nbdev.skill`, layout, relevant skills)    /forks inherit it
- spawning: `swarm(action="add", fork="coordinator", ...)` default; unforked only for blank context; job names (`parser`, `verifier`, `docs`; lowercase; not `all`, `coordinator`, `coordinator-*`); `swarm(action="title", ...)` once scope clear
- parallel forks: one sharded `tasks=[...]` (or `n`) call (`<name>-1`..`<name>-<k>`; `@<name>`, `kill` address group); distinct forked roles sequentially; check `status` before retrying any `add(fork=...)` error    /`add(fork=...)` (solo or paired) can error (`failed to clone trajectory`, `executor has not processed the previous input yet`) while still spawning
- workspace: `inherit` default even for concurrent authors (overrides `swarm` tool hint); no edit fences — full task scope, `exhash` rejects stale hashes; one build/export owner per crate (`cargo develop`, `nbdev-export`); `share`/`branch` only for conflicting builds (land work before `kill`, which deletes workspace)
- briefs (public): forked = ONLY task owned, shared build/export owner if any, report-to (`@coordinator` or next peer); never restate task, rules, steps, done-criteria, or edit fences    /restating rules causes checklist over-grounding; fences hide cross-repo bugs; self-contained briefs for unforked only
- 3-min check-in (multi-fork): `schedule(DurationSeconds=180, ...)` (default `TimerCondition="never"`, not `"any"` /other traffic resets it); on ping: `status` + `read_board`, `@mention` slow or ≥3-min-silent `working` workers (`last_post_time`, or brief `time` on board) for what changing and why, launch unblocked work, read landed edits, re-arm while `working` remains; `manage_task` `kill` when none remain (fallback: `CronExpression="*/3 * * * *"`)
- live audit: distrust summaries; read landed edits as forks finish: bird's-eye view, boilerplate factored out, genuine reuse (no wrappers/shims), consistency, >~80-line files (`code-review` if bloated/duplicating), edited tests (`testing` skill); >2 reads → review fork; clear issues → author fixes; real uncertainty → user decision    /summaries hide workarounds, bloat, bad tests
- user reports: curated — outcome, surprises, deviations, risks, blockers, remaining work; omit performative test counts, timings, internal names, plumbing (`waiting`, seqs, IDs, `open_board`) unless action-changing or asked
- turns: short; report each completed fork (or answer user) immediately, end turn without `swarm_wait` (ending turn parks `main`); `swarm_wait` only on silent board/timer turns with nothing to report
- harness idle warning: ignore `Subagent <id> went idle without reporting anything back` for swarm workers    /workers report on board (`read_board`/`status`), not `send_message`

## workers

- inherited history: read-only context (`main` still owns prior plans); execute ONLY assigned brief; never repeat `main`'s work
- Python: `create(kernel="py")` for own `clikernel`; never `python -c`
- edits: full task scope, no fences; stale `exhash` → re-view, re-apply; respect named build/export owner
- escalation: clear bugs in task path → fix directly; gated action or design call → never evade, post `@coordinator` with exact gap or command, park
- board: concise check-in replies (what changing and why); peer handoffs tag next peer only (`@name` = wakeup doorbell, never CC); `@coordinator` on `[done]`, blocker, or decision; cite prior posts by `#seq`, never copy-paste; helpers via `swarm(action="add")` (adder owns integrating, modelling, killing them)

## board and channels

- addressing: `@name` (or `@<prefix>` for group) wakes `waiting`/`stopped` member; `@all` only for swarm-wide rules/interfaces (never status); unmentioned posts wait for next wakeup; `@name` crosses channels
- channels (when `swarm` offers `channel`, >~8 workers or independent areas): everyone sees `main` + subscribed channels; keep `main` quiet (cross-area only), area talk in `#area`; `@#channel` wakes whole area; ops: `create`, `subscribe`, `unsubscribe`, `list`, `archive`

## lifecycle, models, quota

- states: `waiting` (asleep, zero cost, wakes on `@name`), `working` (reads posts after turn), `stopped` (post-restart, `@name` revives), `killed` (permanent)
- reuse: leave finished workers `waiting`; wake with `@name` ONLY for agreed follow-up or review finding on its exact prior work, never to supply new context (fresh `fork="coordinator"` instead); `kill` only when user done, looping worker replaced, or cleaning up `share`/`branch` (also kill its helpers)
- models/quota: omit `model` to inherit `main`'s unless user asks; switch via `swarm(action="model", name, model)` only on user ask or quota/capacity error (target `waiting`; keeps conversation; never `kill`+`add`; state why); `swarm(action="models")` shows live quota; post-quota failures stay idle until switched or `@name` after recovery
