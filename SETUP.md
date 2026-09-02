# Setting up the Answer.AI harness

This file is a runbook for an LLM session, not a script. If you are a person: open Claude Code, codex, or Grok Build, `cd` anywhere in the aai-ws workspace, and say "follow aai-coding/SETUP.md". If you are the session: first read `README.md` in this repo in full, since the steps below change your user's configuration and the README's design context is what lets you merge, recommend, and answer questions in an informed way. Then work through the steps in order. Each step states an outcome to reach, a check, and what to settle with the user first. Make no change beyond the stated outcomes without asking. Where the user's existing configuration overlaps, merge and never replace: show them each conflict and agree a resolution.

Assumptions: macOS, and at least one harness (Claude Code, codex, or Grok Build) installed and signed in. Claude Code and codex assume the aai-ws uv workspace is cloned and synced (this repo is a member, so its `aai-hook` CLI and pyskills are already installed). Grok Build is hybrid-only and can run from a standalone editable install of this repo plus `clikernel` in one venv; use that venv's `aai-hook` and `clikernel-mcp` when aai-ws is absent. Ask which harnesses to set up before starting, and use absolute paths for this repo and the venv throughout.

Codex has two supported modes. This choice applies only to codex; Claude Code remains kernel-centric; Grok Build is hybrid-only. Settle which codex mode the user wants before changing its configuration:

1. **Kernel-centric:** do file, shell, and Python work through clikernel, complete the llmdojo bootstrap, and discover tools through pyskills. This is the existing Answer.AI harness workflow and most closely matches the Claude Code setup.
2. **Hybrid:** use the harness's native file and shell tools normally (codex: `apply_patch` and Bash; Grok Build: `search_replace` and `run_terminal_command`), and use `clikernel-mcp --quiet` only for Python-specific work. This keeps persistent Python state and pyskills without replacing the native file and shell workflow. Grok Build has no kernel-centric mode: its `UserPromptSubmit` and `SessionStart` hooks are passive (stdout is ignored), and it has no `MessageDisplay` or `PostToolBatch` events, so the dojo bootstrap notices, air nudge, slopometer, and drop-sentinel cannot inject context.

## 1. Kernel server

Outcome: the clikernel MCP server is registered. Claude Code: a user-scope server named `clikernel` running `<venv>/bin/clikernel-mcp`. Kernel-centric codex: a `[mcp_servers.clikernel]` block in `~/.codex/config.toml` with `command` set to that binary, `startup_timeout_sec = 30`, `tool_timeout_sec = 3600`, and `approval_mode = "approve"` for its `execute`, `connect`, `restart`, and `interrupt` tools.

Hybrid codex: use the following exact working configuration, changing the `command` path if the workspace is elsewhere:

```toml
[mcp_servers.clikernel]
command = "/Users/jhoward/aai-ws/.venv/bin/clikernel-mcp"
args = ["--quiet"]
env_vars = ["GITHUB_TOKEN"]
omit_tools_from = ["deferred"]

[mcp_servers.clikernel.tools.execute]
approval_mode = "approve"

[mcp_servers.clikernel.tools.list_kernels]
approval_mode = "approve"

[mcp_servers.clikernel.tools.stop_kernel]
approval_mode = "approve"

[mcp_servers.clikernel.tools.restart]
approval_mode = "approve"

[mcp_servers.clikernel.tools.connect]
approval_mode = "approve"

[mcp_servers.clikernel.tools.interrupt]
approval_mode = "approve"
```

`--quiet` keeps automatic startup output out of ordinary execution replies. Optional, ask the user: `env_vars = ["GITHUB_TOKEN"]` passes their GitHub token into the kernel so sessions can act for them on GitHub (via `ghapi`); remove that line if they do not want it.

Hybrid Grok Build: a `[mcp_servers.clikernel]` block in `~/.grok/config.toml`. Grok has no per-tool `approval_mode` and uses `env` rather than `env_vars`. Merge; do not replace other `[mcp_servers.*]` blocks:

```toml
[mcp_servers.clikernel]
command = "/Users/jhoward/aai-ws/.venv/bin/clikernel-mcp"
args = ["--quiet"]
env = { PATH = "/Users/jhoward/aai-ws/.venv/bin:/usr/bin:/bin:/usr/sbin:/sbin", PYTHONPATH = "/Users/jhoward/aai-ws/aai-coding", GITHUB_TOKEN = "${GITHUB_TOKEN}" }
startup_timeout_sec = 30
tool_timeout_sec = 3600
```

Change `command` (and the `PATH` prefix) to the venv that has `clikernel`, `rustygate`, and this package installed. Grok does not put that venv on PATH when it spawns the server, and `clikernel-mcp` looks up `rustygate` by name. Set `PYTHONPATH` to this repo so the kernel process can import `aai_coding` and the pyskills entry points resolve. Drop `GITHUB_TOKEN` if they do not want the token in the kernel. `grok mcp add` also writes this shape; prefer editing `config.toml` so the merge is visible.

Check: deferred to step 7, where a kernel round trip must work.

Settle first: whether a server named `clikernel` already exists.

## 2. Kernel startup files

Outcome: `~/.config/clikernel/startup.py` and `startup.txt` are symlinks into `<workspace>/llmdojo/claude/`.

Check: deferred to step 7; the startup notice printing is the check.

Settle first: existing non-symlink files at those paths.

## 3. Hooks

Outcome, Claude Code, in `~/.claude/settings.json` under `hooks`: PreToolUse matcher `Write|Edit|NotebookEdit` runs `aai-hook claude-block-native-edit`; PreToolUse matcher `Bash` runs `aai-hook claude-bash-guard`; UserPromptSubmit runs `aai-hook claude-prompt-submit`; SessionStart runs `aai-hook claude-session-start`; UserPromptSubmit, MessageDisplay, and PostToolBatch each also run `aai-hook claude-air` (the come-up-for-air nudge: after 8 tool-call rounds with no text response of 100+ chars, it injects a reminder to surface and reassess, repeating every 5 further rounds). The air nudge is Claude-only: codex has no message-level hook event, so it cannot observe the "text happened" reset condition - the codex-shaped substitute is a sentence in AGENTS.md; revisit if codex grows one. PostToolBatch and Stop also each run `aai-hook claude-drop-sentinel`, a Python port of podlayer/message-drop-sentinel (MIT): it detects the thinking-sandwich message-drop platform bug from the transcript scar (two adjacent thinking blocks) and tells the agent its text was probably eaten: restate it in the turn-final message, or say it now and end the turn if the user needs it immediately. Retire the sentinel entries when the upstream bug is fixed (re-test recipe and issue links in that repo's README). UserPromptSubmit and MessageDisplay also each run `aai-hook claude-slop`: MessageDisplay buffers each displayed assistant message, and at the next prompt the hook scores the previous turn's final message with the `slopometer` CLI, injecting the flagged patterns as context. A prompt that is a bare `;` means the user did not understand the previous reply, and the hook injects an instruction to restate it in plain English. Bare `aai-hook` resolves because the user's shell profile puts the workspace venv on PATH; if it does not, use the absolute venv path.

Outcome, kernel-centric codex, in `~/.codex/hooks.json`: PostCompact, SessionStart with matcher `compact`, and PreToolUse with matcher `mcp__clikernel__execute` each run `<venv>/bin/aai-hook codex-orientation`; UserPromptSubmit runs `<venv>/bin/aai-hook codex-prompt-submit`. Hybrid codex does not install `codex-orientation`, since it does not run the dojo; it may still install `codex-prompt-submit`. codex asks the user to trust hooks on the first start after any `hooks.json` change; tell them to expect that prompt.

Outcome, hybrid Grok Build, a new file `~/.grok/hooks/aai.json` (Grok merges every `*.json` in that directory; do not overwrite other hook files). UserPromptSubmit runs `<venv>/bin/aai-hook grok-prompt-submit`. Do not install `claude-air`, `claude-slop`, `claude-drop-sentinel`, `claude-session-start`, `claude-block-native-edit`, or `codex-orientation`: Grok cannot inject their stdout, and hybrid Grok does not run the dojo. `grok-prompt-submit` emits the same `hookSpecificOutput` JSON as `codex-prompt-submit` so a future Grok that honors Claude-shaped injection will pick it up; today's Grok treats UserPromptSubmit as passive, so the notices also live in `prompts/core.md` (step 5). Tell them to run `/hooks-trust` only if they later add project-scoped hooks; user-scope `~/.grok/hooks/` is already trusted.

Check: `aai-hook claude-prompt-submit` fed `{"prompt": "test?"}` on stdin prints the question notice.

Settle first: every hook the user already has; theirs stay alongside these unless they collide.

## 4. Permissions and environment (Claude Code)

Outcome, in `settings.json`: `permissions.deny` includes `Read`, `Edit`, `Write`, `Grep`, `Glob`, `NotebookEdit`, `Bash(cat *)`, and `Bash(python -c:*)`; `permissions.allow` includes `WebSearch`, `WebFetch`, and `mcp__clikernel__restart`; `env.BASH_DEFAULT_TIMEOUT_MS` is `"90000"`. These force work through the kernel tooling; the harness does not function as designed without them.

Recommended, ask the user: `disableBundledSkills` set to `true` in `settings.json`, turning off the built-in skills (`init`, `review`, `code-review`, `security-review`, `simplify`, `verify`, `run`, `dataviz`, `artifact-design`, `fewer-permission-prompts`, `update-config`, `keybindings-help`), which assume the native file tools this deny list removes.

Settle first: any existing rule that conflicts. In particular a broad `Bash` allow rule defeats both the bash guard and safecmd; surface that one explicitly.

Check: the file still parses as JSON after editing.

## 5. Skills, safecmd, and prompts

Outcome: symlinks from `~/.claude/skills/persistent-python` and `~/.claude/skills/pyskills` to `<this repo>/skills/<name>`. Kernel-centric codex gets the same two skill symlinks. Hybrid codex instead gets `~/.codex/skills/clikernel` pointing to `<this repo>/skills/clikernel` and `~/.codex/skills/notebook-dialog-editing` pointing to `<this repo>/skills/notebook-dialog-editing`; the latter teaches Codex to inspect and edit notebooks and aidialog dialogs safely through the shell CLIs without using a kernel. Hybrid Grok Build gets the same two skill directories under `~/.grok/skills/`. Remove the other mode's skill symlinks when switching, since they intentionally prescribe conflicting tool-use policies. Also link `~/.claude/skills/safecmd` to `<this repo>/plugins/safecmd` and `~/.codex/AGENTS.md` to `<this repo>/prompts/core.md`. Grok Build already has a personal `~/.grok/AGENTS.md` on most machines: do not replace it. Symlink `~/.grok/AGENT.md` to `<this repo>/prompts/core.md` instead; Grok loads every recognized rule filename in `~/.grok/`, and `AGENT.md` is a distinct name from `AGENTS.md` even on a case-insensitive disk.

safecmd auto-approves allowlisted Bash commands. The `safecmd` package is a workspace member, so it is already installed; its allowlist lives at `~/.config/safecmd/config.ini` and the defaults are fine to start.

Optional, Claude Code: the user might like `<this repo>/prompts/core.md` appended to the system prompt; a shell alias adding `--append-system-prompt-file <this repo>/prompts/core.md` to `claude` does it. The stronger option is the team's full behavioral prompt: symlink `~/.claude/sysp` to `<this repo>/prompts/sysp.md` and alias `claude` to `claude --system-prompt-file ~/.claude/sysp --append-system-prompt-file <this repo>/prompts/core.md`, which replaces Claude Code's default prompt entirely. Explain the trade to the user before wiring it: the default's tool schemas survive replacement, but its dynamic environment block and scratchpad path do not, and the behavioral text takes over from the default's guidance.

Optional, codex: the analogue of the full behavioral prompt is `model_instructions_file = "<this repo>/prompts/codex-sysp.md"` (absolute path) in `~/.codex/config.toml`, replacing codex's built-in instructions entirely; `~/.codex/AGENTS.md` (and so `core.md`) still loads on top, and no symlink is involved since the key points straight into the checkout. Explain the trade to the user before wiring it: the file is the team's edited reconstruction of the built-in instructions, so upstream changes to codex's own prompt stop arriving until the file is revised.

Optional, Grok Build: `grok --rules` (alias `--append-system-prompt`) appends text for one session; `--system-prompt-override` replaces the default prompt entirely. There is no team `grok-sysp.md`. Prefer the `~/.grok/AGENT.md` symlink. Do not ship a reconstructed Grok system prompt: Grok's default prompt is the product, and replacing it drops tool-use guidance the hybrid setup still needs.

Settle first: existing real directories where the symlinks go.

## 6. Optional comforts

The user might find it useful to hear a quiet tone when the harness finishes or asks a question: Notification hooks running `afplay /System/Library/Sounds/Submarine.aiff` on matcher `permission_prompt` and `Pop.aiff` on `idle_prompt`. If they keep shell functions they want available inside harness command shells, `env.BASH_ENV` in settings.json (and `[shell_environment_policy.set]` in codex's config.toml) pointing at their aliases file does that. Grok Build has no equivalent shell-env key; functions they need inside `run_terminal_command` belong in their login shell or in the MCP `env` map.

## 7. Restart and verify wiring

All three harnesses read configuration at startup: ask the user to restart each, accepting codex's hook trust prompt when hooks changed. Then verify a kernel round trip by running `1+1` through clikernel. In hybrid codex or Grok Build, the reply should contain just the result rather than the startup text. If `py` fails with connection refused, the venv is missing `ipykernel`/`ipymini`; install them into that same venv. On Grok, also run `grok inspect` and confirm `clikernel-workflow` and `notebook-dialog-editing` appear under Skills, `~/.grok/AGENT.md` under global rules, the `clikernel` MCP server under MCP, and `aai.json` under Hooks.

## 8. Acceptance

In a fresh Claude Code or kernel-centric codex session in any workspace Python project: the bootstrap notice fires; invoking `persistent-python` then running `dojo_start()` completes a clean round; `list_pyskills()` shows the `aai_coding.*` rows; `doc(aai_coding.coding_patterns)` renders.

In a fresh hybrid codex session: `clikernel-workflow` and `notebook-dialog-editing` appear in the available skills; ordinary local text edits use `apply_patch`; notebook and aidialog work can use the shell CLIs without starting a kernel; shell work uses Bash; and clikernel retains Python state across two execution calls. Inside clikernel, `list_pyskills()` shows the `aai_coding.*` rows and `doc(aai_coding.coding_patterns)` renders.

In a fresh hybrid Grok Build session: `clikernel-workflow` and `notebook-dialog-editing` appear in the available skills; ordinary local text edits use `search_replace`; notebook and aidialog work can use the shell CLIs without starting a kernel; shell work uses `run_terminal_command`; and clikernel retains Python state across two execution calls. Inside clikernel, `list_pyskills()` shows the `aai_coding.*` rows and `doc(aai_coding.coding_patterns)` renders. Native file tools stay allowed. When a check fails, fix that step's wiring before moving on, and tell the user what was wrong.
