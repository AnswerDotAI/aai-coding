# Setting up the Answer.AI harness

This file is a runbook for an LLM session, not a script. It sets up our way of working without requiring an Answer.AI account or a copy of our workspace. If you are a person: start with step 0 to create a workspace and get this repo, then open Claude Code or codex in the workspace and say "follow aai-coding/SETUP.md". If you already have the checkout, you can ask a session to follow this file from there, including step 0.

If you are the session: first read `README.md` in this repo in full, since the steps below change your user's configuration and the README's design context is what lets you merge, recommend, and answer questions in an informed way. Then work through the steps in order, checking existing setup before making changes. Make no change beyond the stated outcomes without asking. Where the user's existing configuration overlaps, merge and never replace: show them each conflict and agree a resolution.

This runbook targets macOS; the workspace commands use Bash/Zsh syntax. Do not apply the macOS sound hooks on other systems. Before harness configuration, at least one harness (Claude Code or codex) must be installed and signed in. Ask which harnesses to set up and where the workspace should live. No particular workspace name is required. Below, `<workspace>` means its absolute path, `<venv>` means `<workspace>/.venv`, and `<this repo>` means `<workspace>/aai-coding`. Resolve those placeholders before writing configuration; neither `~` nor shell variables are a substitute for an absolute path in config files.

## 0. Create a fastws workspace

Outcome: a workspace with the starter repos cloned, its shared uv environment activated, and the harness packages installed. If the user already has a fastws workspace, reuse it: check its combined `repos.txt` and `repos-local.txt`, add missing harness repos to the local list rather than changing a shared baseline, keep its Python version unless a dependency requires a change, and skip creation commands for things that already exist. Do not duplicate or move an existing aai-coding checkout without agreeing its location first.

### Prerequisites

- Git and [uv](https://docs.astral.sh/uv/getting-started/installation/) installed. Check `git --version` and `uv --version`.
- GitHub SSH access: fastws clones `owner/repo` entries using `git@github.com:owner/repo.git`. Check `git ls-remote git@github.com:AnswerDotAI/aai-coding.git HEAD`; fix authentication before cloning. The starter repos are public and require no Answer.AI organization membership.
- Rust (`rustc --version`, `cargo --version`) and native build tools (Xcode Command Line Tools on macOS). The starter builds exhash and rgapi from source. Ask before installing missing toolchains.
- Network access for cloning and installing packages.

### Create, clone, and sync

Use fastws-cli 0.0.14 or later for `ws-setup`. Shared/local repo lists and cloning during sync are also supported. Run the commands in the same shell, choosing the appropriate starting point below.

**Public workspace:** bootstrap the public Answer.AI baseline. The destination must not already exist.

```bash
uvx --from 'fastws-cli>=0.0.14' ws-setup AnswerDotAI/aai-ws ~/coding-ws
cd ~/coding-ws
source .venv/bin/activate
```

**Answer.AI team workspace:** use `AnswerDotAI/private-ws` instead of `AnswerDotAI/aai-ws` in that command. It contains the larger team baseline and requires private-repo access. A user's fork or another team's workspace repo can be substituted too. Existing team workspaces should follow the [migration instructions](https://github.com/AnswerDotAI/private-ws#migrating-an-existing-workspace), not create a second workspace.

`ws-setup` clones the chosen repo, creates its `.venv`, installs fastws into that environment, and runs its `ws-sync`. It isolates the new environment even if another workspace is active. It prints activation instructions but does not change shell startup files or configure the coding harness. A failed step leaves the new directory in place for inspection; do not delete it or retry setup over it blindly.

**Custom workspace without a base repo:** clone aai-coding to obtain the copyable starter list, then let fastws clone the remaining repos:

```bash
mkdir -p ~/coding-ws
cd ~/coding-ws
git clone git@github.com:AnswerDotAI/aai-coding.git
cp aai-coding/repos.txt repos.txt
uv venv --python 3.13
source .venv/bin/activate
uv pip install 'fastws-cli>=0.0.14'
ws-sync
```

The examples use `~/coding-ws`; any new directory works. `ws-sync` first pulls the workspace repo if it has an upstream, reads the combined repo lists, clones missing repos, and pulls project updates before installing packages. A failed root pull or clone stops the sync. It creates a missing `pyproject.toml` from `pyproject.tmpl` if available, otherwise generates a minimal one, and installs workspace projects editably. It is not just an install command. See [fastws's documentation](https://github.com/AnswerDotAI/fastws) for the full command reference.

For your own workspace Git repo, track `repos.txt` as your shared baseline and gitignore `repos-local.txt`, the root `pyproject.toml`, `pyrightconfig.json`, `uv.lock`, and `.cargo/`, along with project checkout directories. Keep optional starting defaults in `pyproject.tmpl`; changes to it do not overwrite existing generated configuration. An existing workspace that tracks generated files should back them up before pulling a change that untracks them, then restore its local copies.

The starter list is deliberately small:

| Repo | Why it is included |
|---|---|
| `AnswerDotAI/fastws` | Workspace commands, kept up to date alongside the harness. The distribution name is `fastws-cli`. |
| `AnswerDotAI/aai-coding` | Skills, prompts, and plugins linked from this checkout, plus the `aai-hook` CLI. |
| `AnswerDotAI/llmdojo` | Kernel startup files linked in step 2, and the kernel-centric bootstrap. |
| `AnswerDotAI/ipykernel-helper` | Startup helpers, plus the IPython and ipykernel dependencies needed to run Python kernels. |
| `AnswerDotAI/exhash` | Hash-verified editing tools imported by startup and used by the notebook CLI workflow. |
| `AnswerDotAI/rgapi` | Search tools imported by startup, including the notebook search CLI. |
| `AnswerDotAI/safecmd` | Command approval tool used by the Claude setup; not an aai-coding package dependency. |
| `AnswerDotAI/slopometer` | Prose scoring tool used by the Claude hooks; not an aai-coding package dependency. |

This is a starter for the documented setup, not a strict minimum for each harness mode. Dependencies such as clikernel, pyskills, and aidialog are installed through package dependencies rather than all needing source checkouts. Keep personal extras in `repos-local.txt`: `ws-add` and automatic discovery write there, leaving the baseline alone. A clone of either workspace base receives baseline updates through Git. A starter list copied into a custom workspace is independent and does not receive those updates automatically.

### Check the environment

From the activated shell:

```bash
command -v python ws-sync aai-hook clikernel-mcp pyskills-doc safecmd slopometer
command -v aidialog-summary exhash-cell lnhashview-cell exhash-open rgapi-nbrg
uv pip check
pyskills-doc aai_coding.coding_patterns
python llmdojo/claude/startup.py
```

Run these from the workspace root. The commands should resolve inside `<venv>/bin`, package dependencies should be consistent, and the skill documentation should render. Running the startup script should import its tooling and print the bootstrap instructions; it does not run the dojo or replace the live kernel checks in steps 7–8. Resolve missing dependencies or commands before installing hooks: another environment on PATH can otherwise hide an incomplete setup.

In each new shell, activate the workspace environment before launching the harness. Ask before adding `source <venv>/bin/activate` to the user's shell startup file; global auto-activation is convenient but not required. GUI-launched harnesses may not inherit the shell's PATH, so use absolute executable paths in configuration and ensure hook subprocesses can find the workspace tools too.

## Choose a harness mode

Codex has two supported modes. This choice applies only to codex; Claude Code remains kernel-centric. Settle which codex mode the user wants before changing its configuration:

1. **Kernel-centric:** do file, shell, and Python work through clikernel, complete the llmdojo bootstrap, and discover tools through pyskills. This is the existing Answer.AI harness workflow and most closely matches the Claude Code setup.
2. **Hybrid:** use codex's `apply_patch` and Bash tools normally, and use `clikernel-mcp --quiet` only for Python-specific work. This keeps persistent Python state and pyskills without replacing codex's native file and shell workflow.

## 1. Kernel server

Outcome: the clikernel MCP server is registered. Claude Code: a user-scope server named `clikernel` running `<this repo>/scripts/clikernel-mcp-shim`, which execs `<venv>/bin/clikernel-mcp`, adding `--quiet` when `CLAUDE_CODE_ENTRYPOINT` is `claude-desktop`: desktop kernels skip the startup notice, since desktop sessions take their instructions from the hooks (step 3). Kernel-centric codex: a `[mcp_servers.clikernel]` block in `~/.codex/config.toml` with `command` set to that binary, `startup_timeout_sec = 30`, `tool_timeout_sec = 3600`, and `approval_mode = "approve"` for its `execute`, `connect`, `restart`, and `interrupt` tools.

Hybrid codex: use the following configuration, replacing `<venv>` with the absolute workspace environment path:

```toml
[mcp_servers.clikernel]
command = "<venv>/bin/clikernel-mcp"
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

Check: deferred to step 7, where a kernel round trip must work.

Settle first: whether a server named `clikernel` already exists.

## 2. Kernel startup files

Outcome: `~/.config/clikernel/startup.py` and `startup.txt` are symlinks into `<workspace>/llmdojo/claude/`.

Check: deferred to step 7; the startup notice printing is the check.

Settle first: existing non-symlink files at those paths.

## 3. Hooks

Send a bare `;` to request a plain-English restatement of the previous reply. When response annotations are present, include `;` in the main prompt to rewrite the selected text and answer any accompanying question. The hooks read the request after `## My request:` without parsing the selections.

Outcome, Claude Code, in `~/.claude/settings.json` under `hooks`: PreToolUse matcher `Write|Edit|NotebookEdit` runs `aai-hook claude-block-native-edit`; PreToolUse matcher `Bash` runs `aai-hook claude-bash-guard`; UserPromptSubmit runs `aai-hook claude-prompt-submit`; SessionStart runs `aai-hook claude-session-start`; UserPromptSubmit, MessageDisplay, and PostToolBatch each also run `aai-hook claude-air` (the come-up-for-air nudge: after 8 tool-call rounds with no text response of 100+ chars, it injects a reminder to surface and reassess, repeating every 5 further rounds). The air nudge is Claude-only: codex has no message-level hook event, so it cannot observe the "text happened" reset condition - the codex-shaped substitute is a sentence in AGENTS.md; revisit if codex grows one. PostToolBatch and Stop also each run `aai-hook claude-drop-sentinel`, a Python port of podlayer/message-drop-sentinel (MIT): it detects the thinking-sandwich message-drop platform bug from the transcript scar (two adjacent thinking blocks) and tells the agent its text was probably eaten: restate it in the turn-final message, or say it now and end the turn if the user needs it immediately. Retire the sentinel entries when the upstream bug is fixed (re-test recipe and issue links in that repo's README). UserPromptSubmit and MessageDisplay also each run `aai-hook claude-slop`: MessageDisplay buffers each displayed assistant message, and at the next prompt the hook scores the previous turn's final message with the `slopometer` CLI, injecting the flagged patterns as context. A bare `;` means the user did not understand the previous reply, so the hook asks the agent to restate it in plain English. A bare `'` asks the agent to say whether its closing caveat was a real issue or empty hedging. Bare `aai-hook` resolves because the user's shell profile puts the workspace venv on PATH; if it does not, use the absolute venv path.

Desktop app: it has no launch flags, so no sysp replacement and no `claudedojo` launch. Hooks detect it (`CLAUDE_CODE_ENTRYPOINT` = `claude-desktop`): SessionStart prints `prompts/core.md` on startup, resume, and compaction. Desktop sessions receive no dojo instructions. Native Write and Edit stay usable. NotebookEdit stays blocked everywhere: its writer saves non-ASCII as JSON escapes, churning whole notebooks. The bash guard runs in both frontends. Revisit if the desktop gains launch options.

Outcome, kernel-centric codex, in `~/.codex/hooks.json`: PostCompact, SessionStart with matcher `compact`, and PreToolUse with matcher `mcp__clikernel__execute` each run `<venv>/bin/aai-hook codex-orientation`; UserPromptSubmit runs `<venv>/bin/aai-hook codex-prompt-submit`; Stop and UserPromptSubmit each run `<venv>/bin/aai-hook codex-slop`. Hybrid codex does not install `codex-orientation`, since it does not run the dojo; it may still install `codex-prompt-submit` and `codex-slop`. The Stop hook stores `last_assistant_message`. On the next prompt, `codex-slop` scores that text and handles bare `;`. The `codex-prompt-submit` hook handles `'` independently of scoring. codex asks the user to trust hooks on the first start after any `hooks.json` change; tell them to expect that prompt.

Check: `aai-hook claude-prompt-submit` fed `{"prompt": "test?"}` on stdin prints the question notice.

Settle first: every hook the user already has; theirs stay alongside these unless they collide.

## 4. Permissions and environment (Claude Code)

Outcome, in `settings.json`: `permissions.deny` includes `Read`, `Edit`, `Write`, `Grep`, `Glob`, `NotebookEdit`, `Bash(cat *)`, and `Bash(python -c:*)`; `permissions.allow` includes `WebSearch`, `WebFetch`, and `mcp__clikernel__restart`; `env.BASH_DEFAULT_TIMEOUT_MS` is `"90000"`. These force work through the kernel tooling; the harness does not function as designed without them.

Recommended, ask the user: `disableBundledSkills` set to `true` in `settings.json`, turning off the built-in skills (`init`, `review`, `code-review`, `security-review`, `simplify`, `verify`, `run`, `dataviz`, `artifact-design`, `fewer-permission-prompts`, `update-config`, `keybindings-help`), which assume the native file tools this deny list removes.

Settle first: any existing rule that conflicts. In particular a broad `Bash` allow rule defeats both the bash guard and safecmd; surface that one explicitly. Also whether the user works in the desktop app: settings cannot branch by frontend, and this deny list would strip desktop sessions too. Such users carry these rules in `~/.config/claudedojo/config.toml` instead (step 5).

Check: the file still parses as JSON after editing.

## 5. Skills, safecmd, and prompts

Outcome: symlinks from `~/.claude/skills/persistent-python` and `~/.claude/skills/pyskills` to `<this repo>/skills/<name>`. Kernel-centric codex gets the same two skill symlinks. Hybrid codex instead gets `~/.codex/skills/clikernel` pointing to `<this repo>/skills/clikernel` and `~/.codex/skills/notebook-dialog-editing` pointing to `<this repo>/skills/notebook-dialog-editing`; the latter teaches Codex to inspect and edit notebooks and aidialog dialogs safely through the shell CLIs without using a kernel. Remove the other mode's codex skill symlinks when switching, since they intentionally prescribe conflicting tool-use policies. Also link `~/.claude/skills/safecmd` to `<this repo>/plugins/safecmd` and `~/.codex/AGENTS.md` to `<this repo>/prompts/core.md`.

safecmd auto-approves allowlisted Bash commands. The starter workspace installs the `safecmd` package; its allowlist lives at `~/.config/safecmd/config.ini` and the defaults are fine to start. The starter also installs `slopometer` for the prose-scoring hook. Its first score downloads a spaCy language model into `~/.cache/slopometer`; tell the user to expect that download. Without the executable, the prose hook silently skips scoring, so check it explicitly rather than assuming the hook registration proves it works.

Optional, Claude Code: `claudedojo` launches `claude` on a session opening with the worked dojo round, adding the `claude_args` list from `~/.config/claudedojo/config.toml` (each `~`-expanded). That file carries the whole CLI launch: no shell alias, no `--settings` file:

    claude_args = [
      "--system-prompt-file", "~/.claude/sysp",
      "--append-system-prompt-file", "<this repo>/prompts/core.md",
      "--allowedTools", "WebSearch", "WebFetch", "mcp__clikernel__restart",
      "--disallowedTools", "Read", "Edit", "Write", "Grep", "Glob", "NotebookEdit", "Bash(cat *)", "Bash(python -c:*)",
    ]

`--system-prompt-file` replaces Claude Code's default prompt with sysp.md (symlink `~/.claude/sysp` to `<this repo>/prompts/sysp.md`). Explain the trade before wiring it: the default's tool schemas survive replacement, but its dynamic environment block and scratchpad path do not.

Optional, codex: the analogue of the full behavioral prompt is `model_instructions_file = "<this repo>/prompts/codex-sysp.md"` (absolute path) in `~/.codex/config.toml`, replacing codex's built-in instructions entirely; `~/.codex/AGENTS.md` (and so `core.md`) still loads on top, and no symlink is involved since the key points straight into the checkout. Explain the trade to the user before wiring it: the file is the team's edited reconstruction of the built-in instructions, so upstream changes to codex's own prompt stop arriving until the file is revised.

Settle first: existing real directories where the symlinks go.

## 6. Optional comforts

The user might find it useful to hear a quiet tone when the harness finishes or asks a question: Notification hooks running `afplay /System/Library/Sounds/Submarine.aiff` on matcher `permission_prompt` and `Pop.aiff` on `idle_prompt`. If they keep shell functions they want available inside harness command shells, `env.BASH_ENV` in settings.json (and `[shell_environment_policy.set]` in codex's config.toml) pointing at their aliases file does that.

## 7. Restart and verify wiring

Both harnesses read configuration at startup: ask the user to restart each, accepting codex's hook trust prompt when hooks changed. Then verify a kernel round trip by running `1+1` through clikernel. In the hybrid codex mode, the reply should contain just the result rather than the startup text.

## 8. Acceptance

In a fresh Claude Code or kernel-centric codex session in any workspace Python project: the bootstrap notice fires; invoking `persistent-python` then running `dojo_start()` completes a clean round; `list_pyskills()` shows the `aai_coding.*` rows; `doc(aai_coding.coding_patterns)` renders.

In a fresh hybrid codex session: `clikernel-workflow` and `notebook-dialog-editing` appear in the available skills; ordinary local text edits use `apply_patch`; notebook and aidialog work can use the shell CLIs without starting a kernel; shell work uses Bash; and clikernel retains Python state across two execution calls. Inside clikernel, `list_pyskills()` shows the `aai_coding.*` rows and `doc(aai_coding.coding_patterns)` renders. When a check fails, fix that step's wiring before moving on, and tell the user what was wrong.

## Using the workspace

Activate `<venv>/bin/activate` in your shell, then `cd` into a project checkout to work or launch the harness. Each checkout remains a separate Git repo, but the Python projects share one environment. Run project commands and tests there as usual; importing another workspace package uses its editable checkout.

- **Inspect:** `ws-status` shows uncommitted changes and unpushed commits across repos. Review these before updating; preserve local work and resolve any pull conflicts normally.
- **Update:** `ws-sync` pulls the workspace's baseline first, clones newly listed repos, pulls project updates, refreshes workspace metadata, and installs dependencies. It also upgrades dependencies at most once per day; `ws-sync --upgrade` forces that upgrade pass. Restart running harness sessions and kernels after updates so they pick up changed skills and imported code.
- **Add:** `ws-add owner/repo` clones a repo, records it in the workspace's gitignored `repos-local.txt`, and syncs. For a repo already cloned immediately inside the workspace, use `ws-add directory-name`. Adding a dependency's repo makes it editable too.
- **Remove:** `ws-remove owner/repo` handles personal repos, with safety checks and confirmation before deleting a checkout. It refuses shared baseline members. Removing a repo from the shared list never deletes anyone's checkout; existing root checkouts become local additions on sync.

With the workspace environment activated, `ws-sync` can find the workspace from other directories. Run the commands from the workspace root when in doubt. Keep personal instructions and settings separate from the shared prompts; updates should not require reapplying personal edits to this repo.
