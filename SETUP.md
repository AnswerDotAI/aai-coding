# Setting up the Answer.AI harness

This file is a runbook for an LLM session, not a script. If you are a person: open Claude Code or codex, `cd` anywhere in the aai-ws workspace, and say "follow aai-coding/SETUP.md". If you are the session: first read `README.md` in this repo in full, since the steps below change your user's configuration and the README's design context is what lets you merge, recommend, and answer questions in an informed way. Then work through the steps in order. Each step states an outcome to reach, a check, and what to settle with the user first. Make no change beyond the stated outcomes without asking. Where the user's existing configuration overlaps, merge and never replace: show them each conflict and agree a resolution.

Assumptions: macOS, the aai-ws uv workspace cloned and synced (this repo is a member, so its `aai-hook` CLI and pyskills are already installed), and at least one harness (Claude Code or codex) installed and signed in. Ask which harnesses to set up before starting, and use absolute paths for this repo and the workspace venv throughout.

## 1. Kernel server

Outcome: the clikernel MCP server is registered. Claude Code: a user-scope server named `clikernel` running `<venv>/bin/clikernel-mcp`. codex: a `[mcp_servers.clikernel]` block in `~/.codex/config.toml` with `command` set to that binary, `startup_timeout_sec = 30`, `tool_timeout_sec = 3600`, and `approval_mode = "approve"` for its `execute`, `connect`, `restart`, and `interrupt` tools. Optional, ask the user: `env_vars = ["GITHUB_TOKEN"]` on the server block passes their GitHub token into the kernel so sessions can act for them on GitHub (via `ghapi`); add it only if they want that and are happy to share the token.

Check: deferred to step 7, where a kernel round trip must work.

Settle first: whether a server named `clikernel` already exists.

## 2. Kernel startup files

Outcome: `~/.config/clikernel/startup.py` and `startup.txt` are symlinks into `<workspace>/llmdojo/claude/`.

Check: deferred to step 7; the startup notice printing is the check.

Settle first: existing non-symlink files at those paths.

## 3. Hooks

Outcome, Claude Code, in `~/.claude/settings.json` under `hooks`: PreToolUse matcher `Write|Edit|NotebookEdit` runs `aai-hook claude-block-native-edit`; PreToolUse matcher `Bash` runs `aai-hook claude-bash-guard`; UserPromptSubmit runs `aai-hook claude-prompt-submit`; SessionStart runs `aai-hook claude-session-start`; UserPromptSubmit, MessageDisplay, and PostToolBatch each also run `aai-hook claude-air` (the come-up-for-air nudge: after 8 tool-call rounds with no text response of 100+ chars, it injects a reminder to surface and reassess, repeating every 5 further rounds). The air nudge is Claude-only: codex has no message-level hook event, so it cannot observe the "text happened" reset condition - the codex-shaped substitute is a sentence in AGENTS.md; revisit if codex grows one. PostToolBatch and Stop also each run `aai-hook claude-drop-sentinel`, a Python port of podlayer/message-drop-sentinel (MIT): it detects the thinking-sandwich message-drop platform bug from the transcript scar (two adjacent thinking blocks) and tells the agent its text was probably eaten: restate it in the turn-final message, or say it now and end the turn if the user needs it immediately. Retire the sentinel entries when the upstream bug is fixed (re-test recipe and issue links in that repo's README). UserPromptSubmit and MessageDisplay also each run `aai-hook claude-slop`: MessageDisplay buffers each displayed assistant message, and at the next prompt the hook scores the previous turn's final message with the `slopometer` CLI, injecting the flagged patterns as context. A prompt that is a bare `;` means the user did not understand the previous reply, and the hook injects an instruction to restate it in plain English. Bare `aai-hook` resolves because the user's shell profile puts the workspace venv on PATH; if it does not, use the absolute venv path.

Desktop app: the desktop currently has no launch flags, so it cannot replace the system prompt or open on a prepared session the way `claudedojo` launches `claude`. The hooks detect it (`CLAUDE_CODE_ENTRYPOINT` = `claude-desktop`): SessionStart prints `prompts/core.md` instead of the bootstrap gate, and native Write and Edit stay usable. NotebookEdit stays blocked everywhere: its writer saves non-ASCII as JSON escapes and churns every notebook it touches. The bash guard also runs in both frontends. Revisit if the desktop gains launch options.

Outcome, codex, in `~/.codex/hooks.json`: PostCompact, SessionStart with matcher `compact`, and PreToolUse with matcher `mcp__clikernel__execute` each run `<venv>/bin/aai-hook codex-orientation`; UserPromptSubmit runs `<venv>/bin/aai-hook codex-prompt-submit`. codex asks the user to trust hooks on the first start after any `hooks.json` change; tell them to expect that prompt.

Check: `aai-hook claude-prompt-submit` fed `{"prompt": "test?"}` on stdin prints the question notice.

Settle first: every hook the user already has; theirs stay alongside these unless they collide.

## 4. Permissions and environment (Claude Code)

Outcome, in `settings.json`: `permissions.deny` includes `Read`, `Edit`, `Write`, `Grep`, `Glob`, `NotebookEdit`, `Bash(cat *)`, and `Bash(python -c:*)`; `permissions.allow` includes `WebSearch`, `WebFetch`, and `mcp__clikernel__restart`; `env.BASH_DEFAULT_TIMEOUT_MS` is `"90000"`. These force work through the kernel tooling; the harness does not function as designed without them.

Recommended, ask the user: `disableBundledSkills` set to `true` in `settings.json`, turning off the built-in skills (`init`, `review`, `code-review`, `security-review`, `simplify`, `verify`, `run`, `dataviz`, `artifact-design`, `fewer-permission-prompts`, `update-config`, `keybindings-help`), which assume the native file tools this deny list removes.

Settle first: any existing rule that conflicts. In particular a broad `Bash` allow rule defeats both the bash guard and safecmd; surface that one explicitly. Also whether the user works in the desktop app: settings cannot branch by frontend, so this deny list would remove native tools from desktop sessions too. Such users skip the deny list here and carry these rules in `~/.config/claudedojo/config.toml` instead (step 5), where they apply only to `claudedojo` launches.

Check: the file still parses as JSON after editing.

## 5. Skills, safecmd, and prompts

Outcome: symlinks from `~/.claude/skills/persistent-python`, `~/.claude/skills/pyskills`, and the same two names in `~/.codex/skills`, to `<this repo>/skills/<name>`; `~/.claude/skills/safecmd` to `<this repo>/plugins/safecmd`; `~/.codex/AGENTS.md` to `<this repo>/prompts/core.md`.

safecmd auto-approves allowlisted Bash commands. The `safecmd` package is a workspace member, so it is already installed; its allowlist lives at `~/.config/safecmd/config.ini` and the defaults are fine to start.

Optional, Claude Code: the user might like `<this repo>/prompts/core.md` appended to the system prompt; a shell alias adding `--append-system-prompt-file <this repo>/prompts/core.md` to `claude` does it. The stronger option is the team's full behavioral prompt: symlink `~/.claude/sysp` to `<this repo>/prompts/sysp.md` and alias `claude` to `claude --system-prompt-file ~/.claude/sysp --append-system-prompt-file <this repo>/prompts/core.md`, which replaces Claude Code's default prompt entirely. Explain the trade to the user before wiring it: the default's tool schemas survive replacement, but its dynamic environment block and scratchpad path do not, and the behavioral text takes over from the default's guidance.

Optional, codex: the analogue of the full behavioral prompt is `model_instructions_file = "<this repo>/prompts/codex-sysp.md"` (absolute path) in `~/.codex/config.toml`, replacing codex's built-in instructions entirely; `~/.codex/AGENTS.md` (and so `core.md`) still loads on top, and no symlink is involved since the key points straight into the checkout. Explain the trade to the user before wiring it: the file is the team's edited reconstruction of the built-in instructions, so upstream changes to codex's own prompt stop arriving until the file is revised.

Settle first: existing real directories where the symlinks go.

## 6. Optional comforts

The user might find it useful to hear a quiet tone when the harness finishes or asks a question: Notification hooks running `afplay /System/Library/Sounds/Submarine.aiff` on matcher `permission_prompt` and `Pop.aiff` on `idle_prompt`. If they keep shell functions they want available inside harness command shells, `env.BASH_ENV` in settings.json (and `[shell_environment_policy.set]` in codex's config.toml) pointing at their aliases file does that.

## 7. Restart and verify wiring

Both harnesses read configuration at startup: ask the user to restart each, accepting codex's hook trust prompt. Then verify a kernel round trip (run `1+1` through the clikernel execute tool) and that the session-start notice appeared.

## 8. Acceptance

In a fresh Claude Code session in any workspace Python project: the bootstrap notice fires; invoking `persistent-python` then running `dojo_start()` completes a clean round; `list_pyskills()` shows the `aai_coding.*` rows; `doc(aai_coding.coding_patterns)` renders. When a check fails, fix that step's wiring before moving on, and tell the user what was wrong.
