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

`ws-setup` clones the chosen repo, creates its `.venv`, installs fastws into that environment, and runs its `ws-sync`. It isolates the new environment even if another workspace is active. It prints activation instructions but does not change shell startup files or configure the coding harness. A failed step leaves the new directory in place for inspection; do not delete it or retry setup over it blindly.

**Custom workspace without a base repo:** create the directory:

```bash
mkdir -p ~/coding-ws
cd ~/coding-ws
```

Create `repos.txt` from the repository names in the table below, one per line. Then create the environment and let fastws clone and install those projects:

```bash
uv venv --python 3.13
source .venv/bin/activate
uv pip install 'fastws-cli>=0.0.14'
ws-sync
```

The examples use `~/coding-ws`; any new directory works. `ws-sync` first pulls the workspace repo if it has an upstream, reads the combined repo lists, clones missing repos, and pulls project updates before installing packages. A failed root pull or clone stops the sync. It creates a missing `pyproject.toml` from `pyproject.tmpl` if available, otherwise generates a minimal one, and installs workspace projects editably. It is not just an install command. See [fastws's documentation](https://github.com/AnswerDotAI/fastws) for the full command reference.

For your own workspace Git repo, track `repos.txt` as your shared baseline and gitignore `repos-local.txt`, the root `pyproject.toml`, `pyrightconfig.json`, `uv.lock`, and `.cargo/`, along with project checkout directories. Keep optional starting defaults in `pyproject.tmpl`; changes to it do not overwrite existing generated configuration. An existing workspace that tracks generated files should back them up before pulling a change that untracks them, then restore its local copies.

For a custom workspace, use these repositories in `repos.txt`. The public workspace already supplies its shared list:

| Repo | Why it is included |
|---|---|
| `AnswerDotAI/fastws` | Workspace commands, kept up to date alongside the harness. The distribution name is `fastws-cli`. |
| `AnswerDotAI/aai-coding` | Skills, prompts, plugins, and the kernel startup file linked from this checkout, plus the `aai-hook` and `claudesub` CLIs. |
| `AnswerDotAI/exhash` | Hash-verified editing tools imported by startup and used by the notebook CLI workflow. |
| `AnswerDotAI/rgapi` | Search tools imported by startup, including the notebook search CLI. |
| `AnswerDotAI/safecmd` | Command approval tool used by the Claude setup; not an aai-coding package dependency. |
| `AnswerDotAI/slopometer` | Prose scoring tool used by the Claude hooks; not an aai-coding package dependency. |

Dependencies such as clikernel, pyskills, and aidialog install as packages and do not all need source checkouts. Keep personal extras in `repos-local.txt`: `ws-add` and automatic discovery write there, leaving the baseline alone. A clone of a workspace base receives shared `repos.txt` updates through Git. A custom workspace's own list receives no updates from that base.

### Check the environment

From the activated shell:

```bash
command -v python ws-sync aai-hook clikernel-mcp clikernel-hook pyskills-doc safecmd slopometer
command -v aidialog-summary exhash-cell lnhashview-cell exhash-open rgapi-nbrg
uv pip check
pyskills-doc aai_coding.coding_patterns
python aai-coding/kernel/startup.py
```

Run these from the workspace root. The commands should resolve inside `<venv>/bin`, package dependencies should be consistent, and the skill documentation should render. Running the startup script should import its tooling and print the bootstrap instructions. Verify the live kernel separately in step 7. Resolve missing dependencies or commands before installing hooks; another environment on PATH can hide an incomplete setup.

In each new shell, activate the workspace environment before launching the harness. Ask before adding `source <venv>/bin/activate` to the user's shell startup file; global auto-activation is convenient but not required. GUI-launched harnesses may not inherit the shell's PATH, so use absolute executable paths in configuration and ensure hook subprocesses can find the workspace tools too.

## Working through kernels

Claude Code and Codex use persistent kernels for Python, file inspection, searching, notebook work, and most edits. Discover tools through pyskills and use exhash for hash-verified edits. Use Bash for shell commands, builds, and Git. Native tools remain available where the installed skills call for them. Launch the normal `claude` or `codex` executable.

## 1. Kernel server

Outcome: a server named `clikernel` runs `<venv>/bin/clikernel-mcp` directly. Check for an existing registration before adding one.

For Claude Code, register a user-scope stdio server with that command and no arguments. For Codex, merge the following into `~/.codex/config.toml`, replacing `<venv>` with the absolute workspace environment path:

```toml
[mcp_servers.clikernel]
command = "<venv>/bin/clikernel-mcp"
args = ["--quiet"]
omit_tools_from = ["deferred"]

[mcp_servers.clikernel.tools.exec]
approval_mode = "approve"

[mcp_servers.clikernel.tools.list_kernels]
approval_mode = "approve"

[mcp_servers.clikernel.tools.delete_kernel]
approval_mode = "approve"

[mcp_servers.clikernel.tools.restart]
approval_mode = "approve"

[mcp_servers.clikernel.tools.use_kernel]
approval_mode = "approve"

[mcp_servers.clikernel.tools.create]
approval_mode = "approve"

[mcp_servers.clikernel.tools.interrupt]
approval_mode = "approve"
```

`--quiet` suppresses startup output and automatic rule notes. Ask before adding `env_vars = ["GITHUB_TOKEN"]` to the server block. It passes the user's GitHub token into local kernels for tools such as `ghapi`.

In the main conversation, create a Python kernel with `create(kernel="py")` before calling `exec(code=...)`. Reuse that agent's current kernel on later calls. `use_kernel` attaches to a known existing kernel. Startup runs in each newly created Python kernel.

Codex gives each fork its own MCP session and current-kernel selection. Each fork creates its own kernel. Claude needs the isolation hook in step 3; with it, a subagent's first `exec` creates a separate kernel with startup helpers but none of the parent's variables.

Check: deferred to step 7.

## 2. Kernel startup file

Outcome: `~/.config/clikernel/startup.py` is a symlink to `<this repo>/kernel/startup.py`.

Settle existing non-symlink files before changing the path. Replace an older startup symlink with this target. Do not overwrite a user's custom startup file without agreeing how to retain it.

Check: verify startup helpers in the live kernel in step 7. Codex's quiet configuration does not print the startup notice.

## 3. Hooks

Merge these into `~/.claude/settings.json` under `hooks`. Use `<venv>/bin/aai-hook` for each `aai-hook` command below. Existing unrelated hooks stay in place.

| Event | Matcher | Command |
|---|---|---|
| `PreToolUse` | `Write\|Edit\|NotebookEdit` | `aai-hook claude-block-native-edit` |
| `PreToolUse` | `Bash` | `aai-hook claude-bash-guard` |
| `PreToolUse` | `mcp__clikernel__.*` | `<venv>/bin/clikernel-hook` |
| `UserPromptSubmit` | omitted | `aai-hook claude-prompt-submit` |
| `SessionStart` | omitted | `aai-hook claude-session-start` |
| `SubagentStart` | omitted | `aai-hook claude-subagent-start` |
| `UserPromptSubmit`, `MessageDisplay`, `PostToolBatch` | omitted | `aai-hook claude-air` |
| `UserPromptSubmit`, `MessageDisplay` | omitted | `aai-hook claude-slop` |

For rows with several events, register the command under each event. Resolve executable paths to `<venv>/bin` rather than relying on a GUI-launched process's PATH.

`clikernel-hook` supplies subagent identity to clikernel. Register that command directly; its implementation belongs to clikernel. Codex already isolates its MCP sessions and needs no identity hook.

The prompt hook adds notices for questions, reading requests, and approvals. The startup hook supplies bootstrap and resume guidance. The subagent-start hook tells forks to ignore Claude's injected `<fork-boilerplate>` instructions.

The air hook nudges after 8 tool-call rounds without a substantive text response, then every 5 further rounds. The slop hook buffers displayed messages and scores the previous turn's final message at the next prompt. These hooks remain Claude-only. The default slop thresholds can be overridden in the command; Jeremy uses `SLOP_DENSITY=20 SLOP_WORST=12 aai-hook claude-slop` for `UserPromptSubmit`.

For Codex, merge this into `~/.codex/hooks.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "<venv>/bin/aai-hook codex-prompt-submit"
          }
        ]
      }
    ]
  }
}
```

Do not install `codex-orientation`. After changing Codex hooks, tell the user to expect its hook trust prompt on restart.

## 4. Permissions and environment (Claude Code)

In `settings.json`, set `env.BASH_DEFAULT_TIMEOUT_MS` to `"90000"`. Include `Grep`, `Glob`, and `NotebookEdit` in `permissions.deny`. Include `WebSearch`, `WebFetch`, and clikernel's `create`, `use_kernel`, `list_kernels`, `restart`, `interrupt`, and `delete_kernel` tools in `permissions.allow`, using names such as `mcp__clikernel__create`.

Leave native `Read` and Bash available. The edit hook blocks `Write`, `Edit`, and `NotebookEdit` in favour of kernel editing tools. The Bash hook rejects output-truncating pipes and merged stderr; it does not force shell commands through the kernel.

Recommend `disableBundledSkills = true` to avoid built-in skills that prescribe a different workflow. Discuss conflicting existing permissions before changing them. Preserve the user's other restrictions and preferences.

Check: `settings.json` still parses after merging the hooks and permissions.

## 5. Skills, safecmd, and prompts

Create these skill symlinks into this checkout:

| Harness | Link | Target under `<this repo>` |
|---|---|---|
| Claude Code | `~/.claude/skills/persistent-python` | `skills/persistent-python` |
| Claude Code | `~/.claude/skills/pyskills` | `skills/pyskills` |
| Claude Code | `~/.claude/skills/safecmd` | `plugins/safecmd` |
| Codex | `~/.codex/skills/clikernel` | `skills/clikernel` |
| Codex | `~/.codex/skills/notebook-dialog-editing` | `skills/notebook-dialog-editing` |

The Codex skills appear as `kernel-notebook-editing` and `cli-notebook-editing`. Use the CLI notebook workflow only when the user explicitly requests working without a kernel. Resolve existing files or directories at the link paths with the user. Do not edit the skills as part of setup.

The starter includes `safecmd` and `slopometer`. safecmd's allowlist lives at `~/.config/safecmd/config.ini`. slopometer's first score downloads a spaCy language model into `~/.cache/slopometer`; tell the user to expect that download. Without the executable, the prose hook skips scoring.

Put the shared rules from `prompts/core.md` in `~/.codex/AGENTS.md`. For an uncustomized setup, symlink the file to this checkout. Merge with an existing personal file instead of replacing it.

For Claude Code, append the shared rules with `--append-system-prompt-file <this repo>/prompts/core.md`. Jeremy's `ccd` alias also uses the replacement system prompt:

```bash
claude --system-prompt-file <this repo>/prompts/sysp.md --append-system-prompt-file <this repo>/prompts/core.md
```

Ask before installing the replacement prompt. It replaces Claude's default behavioural instructions, including the dynamic environment block and scratchpad path. Tool schemas remain available. The executable is still ordinary Claude Code.

Codex can use `model_instructions_file = "<this repo>/prompts/codex-sysp.md"` in `~/.codex/config.toml`. Explain this choice before setting it: the file replaces Codex's built-in instructions, and upstream prompt changes do not arrive until it is revised. `~/.codex/AGENTS.md` still loads alongside it.

## 6. Optional comforts

The user might find it useful to hear a quiet tone when the harness finishes or asks a question: Notification hooks running `afplay /System/Library/Sounds/Submarine.aiff` on matcher `permission_prompt` and `Pop.aiff` on `idle_prompt`. If they keep shell functions they want available inside harness command shells, `env.BASH_ENV` in settings.json (and `[shell_environment_policy.set]` in codex's config.toml) pointing at their aliases file does that.

Model choice, UI settings, sounds, and disabled optional features are personal preferences. Do not copy them from another user's configuration without asking.

## 7. Restart and verify

Ask the user to restart each configured harness. Accept Codex's hook trust prompt when hooks changed.

Start a fresh session from the workspace root or a Python project containing `pyproject.toml`. Startup uses that file to enable the documented helpers. Confirm the installed skills are available. Use clikernel's MCP tools to create a Python kernel and verify state across two execution calls:

```python
create(kernel="py")
exec(code="setup_check = 1")
exec(code="setup_check + 1")
```

The last call returns `2`. In the kernel, `list_pyskills()` should include the `aai_coding.*` rows and `doc('aai_coding.coding_patterns')` should render. Check the startup helpers even when quiet mode hides the startup notice.

Have one fork create and use its own kernel. It must have startup helpers without the parent's `setup_check` variable. Confirm the parent's current kernel and variable are unchanged. Close kernels created only for this check. When a check fails, report the failed step and fix its wiring before continuing.

## Using the workspace

Activate `<venv>/bin/activate` in your shell, then `cd` into a project checkout to work or launch the harness. Each checkout remains a separate Git repo, but the Python projects share one environment. Run project commands and tests there as usual; importing another workspace package uses its editable checkout.

- **Inspect:** `ws-status` shows uncommitted changes and unpushed commits across repos. Review these before updating; preserve local work and resolve any pull conflicts normally.
- **Update:** `ws-sync` pulls the workspace's baseline first, clones newly listed repos, pulls project updates, refreshes workspace metadata, and installs dependencies. It also upgrades dependencies at most once per day; `ws-sync --upgrade` forces that upgrade pass. Restart running harness sessions and kernels after updates so they pick up changed skills and imported code.
- **Add:** `ws-add owner/repo` clones a repo, records it in the workspace's gitignored `repos-local.txt`, and syncs. For a repo already cloned immediately inside the workspace, use `ws-add directory-name`. Adding a dependency's repo makes it editable too.
- **Remove:** `ws-remove owner/repo` handles personal repos, with safety checks and confirmation before deleting a checkout. It refuses shared baseline members. Removing a repo from the shared list never deletes anyone's checkout; existing root checkouts become local additions on sync.

With the workspace environment activated, `ws-sync` can find the workspace from other directories. Run the commands from the workspace root when in doubt. Keep personal instructions and settings separate from the shared prompts; updates should not require reapplying personal edits to this repo.
