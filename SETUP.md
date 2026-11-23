# Setting up the Answer.AI harness

NB: this file is designed for an LLM reader, not a human. Add it to your LLM's context and ask it to explain.

notation: /why; `<workspace>`: workspace's absolute path; `<venv>`: `<workspace>/.venv`; `<this repo>`: `<workspace>/aai-coding`

- runbook, not script; no Answer.AI account needed
- person: step 0, then Claude Code, Codex, or Antigravity in workspace: "follow aai-coding/SETUP.md"; from an existing aai-coding checkout, session can do step 0 too
- session first: this repo's `README.md`, in full    /explains design: needed to merge settings, recommend, answer questions
- steps in order; check existing setup first; nothing beyond a step's outcome without asking
- user's config overlaps, or something already at a path: merge, never replace; agree each conflict with user
- macOS; Bash or Zsh
- ask: which harnesses (≥1, each installed and signed in before configuring); workspace location
- config files: absolute paths, never `~`, variables or bare command names    /GUI-launched harness, hook subprocesses may not inherit shell's PATH
- result: Python, files, search, notebooks, most edits through clikernel kernels (skills explain); native tools where skills call for them; Bash: shell, builds, Git; each harness launched as usual

## 0. Create a fastws workspace

Outcome: `AnswerDotAI/aai-ws` cloned with its repos; its uv environment active; harness packages installed.

- existing aai-ws clone: skip creation; `ws-sync` in it; keep its Python unless a dependency needs another
- aai-coding checked out elsewhere: agree with user before duplicating or moving
- need: Git, uv, Rust + native build tools (macOS: Xcode CLT); missing: ask before installing    /setup builds exhash, rgapi from source
- GitHub SSH must work: `git ls-remote git@github.com:AnswerDotAI/aai-coding.git HEAD`    /fastws clones over SSH; repos public: no org membership needed

one shell; destination must not exist:

```bash
uvx --from 'fastws-cli>=0.0.14' ws-setup AnswerDotAI/aai-ws ~/coding-ws
cd ~/coding-ws
source .venv/bin/activate
```

- `ws-setup`: runs `ws-sync` too; touches no shell startup file or harness config; fails: leave directory for inspection, don't delete it or rerun over it blindly
- fastws commands: [fastws docs](https://github.com/AnswerDotAI/fastws)

check, activated shell, workspace root:

```bash
command -v python ws-sync aai-hook clikernel-mcp clikernel-hook pyskills-doc safecmd slopometer
command -v aidialog-summary exhash-cell lnhashview-cell exhash-open rgapi-nbrg
uv pip check
pyskills-doc aai_coding.coding_patterns
python aai-coding/kernel/startup.py
```

- expect: every command in `<venv>/bin`; startup script prints bootstrap instructions; fix any failure before hooks    /another environment on PATH can hide incomplete setup
- each new shell: activate `<venv>` before launching a harness; activation in shell startup file: optional, ask first

## 1. Kernel server

Outcome: MCP server `clikernel` runs `<venv>/bin/clikernel-mcp`.

- Claude Code: user-scope stdio server, no arguments
- Codex, `~/.codex/config.toml`:

```toml
[mcp_servers.clikernel]
command = "<venv>/bin/clikernel-mcp"
args = ["--quiet"]
omit_tools_from = ["deferred"]
tools.exec.approval_mode = "approve"
tools.list_kernels.approval_mode = "approve"
tools.delete_kernel.approval_mode = "approve"
tools.restart.approval_mode = "approve"
tools.use_kernel.approval_mode = "approve"
tools.create.approval_mode = "approve"
tools.interrupt.approval_mode = "approve"
```

- `--quiet`: no startup output, automatic rule notes
- `env_vars = ["GITHUB_TOKEN"]` in that block: ask first    /passes user's GitHub token into kernels, e.g. for `ghapi`
- Antigravity: global plugin at `~/.gemini/config/plugins/aai-coding/` (`plugin.json` with `{"name": "aai-coding"}`, plus `mcp_config.json`):

```json
{
  "mcpServers": {
    "clikernel": {
      "command": "<venv>/bin/clikernel-mcp",
      "args": ["--maxout", "10000"]
    }
  }
}
```

- omit `--quiet` on Antigravity    /lets `create(kernel="py")` print the `startup.py` parallel `doc()` banner
- `--maxout 10000` on Antigravity    /stays under its 10,240-byte MCP spill and 78-byte timestamp header
- Antigravity names plugin servers `<plugin>_<server>` (`aai-coding_clikernel`), starts them with `cwd` = plugin dir, and shares one `clikernel-mcp` process across all conversations and subagents
- isolation: Claude subagents and all Antigravity conversations/subagents need `clikernel-hook` (step 3); Codex isolates its MCP sessions without it

## 2. Kernel startup file

Outcome: `~/.config/clikernel/startup.py` symlinks to `<this repo>/kernel/startup.py`; an older symlink there is replaced.

## 3. Hooks

Claude Code, `hooks` in `~/.claude/settings.json`; `aai-hook` = `<venv>/bin/aai-hook`; what each does: `aai_coding/harness.py` docstrings:

Event|Matcher|Command
-|-|-
`PreToolUse`|`Write\|Edit\|NotebookEdit`|`aai-hook claude-block-native-edit`
`PreToolUse`|`Bash`|`aai-hook claude-bash-guard`
`PreToolUse`|`mcp__clikernel__.*`|`<venv>/bin/clikernel-hook`
`UserPromptSubmit`|none|`aai-hook claude-prompt-submit`
`SessionStart`|none|`aai-hook claude-session-start`
`SubagentStart`|none|`aai-hook claude-subagent-start`
`UserPromptSubmit`, `MessageDisplay`, `PostToolBatch`|none|`aai-hook claude-air`
`UserPromptSubmit`, `MessageDisplay`|none|`aai-hook claude-slop`

- row with several events: register the command under each
- `clikernel-hook`: register directly    /implementation belongs to clikernel
- `claude-slop`: score thresholds overridable in command; Jeremy, on `UserPromptSubmit`: `SLOP_DENSITY=20 SLOP_WORST=12 aai-hook claude-slop`
- Codex, `~/.codex/hooks.json`:

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
    ],
    "SessionStart": [
      {
        "matcher": "^compact$",
        "hooks": [
          {
            "type": "command",
            "command": "<venv>/bin/aai-hook codex-orientation"
          }
        ]
      }
    ]
  }
}
```

- Antigravity, `~/.gemini/config/plugins/aai-coding/hooks.json` (plugin root; reloads next turn):

```json
{
  "clikernel-isolate": {
    "PreToolUse": [
      {
        "matcher": "call_mcp_tool",
        "hooks": [{"type": "command", "command": "<venv>/bin/clikernel-hook"}]
      }
    ]
  },
  "aai-coding": {
    "PreToolUse": [{"matcher": "swarm", "hooks": [{"type": "command", "command": "<venv>/bin/aai-hook agy-swarm-guard"}]}],
    "PostToolUse": [{"matcher": "call_mcp_tool", "hooks": [{"type": "command", "command": "<venv>/bin/aai-hook agy-kernel-warn"}]}],
    "SessionStart": [{"type": "command", "command": "<venv>/bin/aai-hook agy-session-start"}],
    "PreInvocation": [{"type": "command", "command": "<venv>/bin/aai-hook agy-prompt-submit"}],
    "PostInvocation": [{"type": "command", "command": "<venv>/bin/aai-hook agy-kernel-warn"}]
  }
}
```

- `clikernel-hook` on Antigravity: injects `agent` = `conversationId` and returns `decision: "allow"` for `clikernel` or `*_clikernel`; returns `decision: "ask"` for other MCP servers

## 4. Permissions and environment (Claude Code)

`~/.claude/settings.json`:

- `env.BASH_DEFAULT_TIMEOUT_MS`: `"90000"`
- `permissions.deny`: add `Grep` `Glob` `NotebookEdit`; leave `Read`, Bash available
- `permissions.allow`: add `WebSearch` `WebFetch`, and `mcp__clikernel__` + `create` `use_kernel` `list_kernels` `restart` `interrupt` `delete_kernel`
- `disableBundledSkills = true`: recommend    /built-in skills prescribe a different workflow
- after merging: file still parses

## 5. Skills, safecmd, prompts

skill symlinks; setup edits no skill:

- `~/.claude/skills/{persistent-python,pyskills}` → `<this repo>/skills/<same name>`
- `~/.claude/skills/safecmd` → `<this repo>/plugins/safecmd`
- `~/.codex/skills/{clikernel,notebook-dialog-editing,pyskills}` → `<this repo>/skills/<same name>`; listed as `kernel-notebook-editing`, `cli-notebook-editing`, `pyskills`
- `~/.gemini/config/plugins/aai-coding/skills/{kernel-notebook-editing,cli-notebook-editing}` → `<this repo>/skills/{clikernel,notebook-dialog-editing}`    /folder name must match frontmatter `name`

- safecmd allowlist: `~/.config/safecmd/config.ini`
- slopometer: first score downloads a spaCy model into `~/.cache/slopometer`: tell user; executable missing: hook skips scoring
- shared rules, `prompts/core.md`: Codex: `~/.codex/AGENTS.md` symlinks to it if uncustomized, else merge rules in; Claude Code: `--append-system-prompt-file <this repo>/prompts/core.md`; Antigravity: `~/.gemini/config/plugins/aai-coding/rules/AGENTS.md` → `prompts/core.md`
- shared kernel/pyskills bootstrap, `prompts/kernel.md` (`trigger: always_on`): Claude Code: `~/.claude/rules/kernel.md` → `prompts/kernel.md`; Antigravity: `~/.gemini/config/plugins/aai-coding/rules/kernel.md` → `prompts/kernel.md` and `rules/GEMINI.md` → `prompts/agy-kernel.md`    /stays in context across compaction in both harnesses; `agy-kernel.md` holds Antigravity-only tool and swarm rules
- replacement system prompt, Claude Code (Jeremy's `ccd` alias): ask first    /replaces Claude's default instructions, incl. environment block, scratchpad path; tool schemas, executable unchanged

```bash
claude --system-prompt-file <this repo>/prompts/sysp.md --append-system-prompt-file <this repo>/prompts/core.md
```

- replacement instructions, Codex, optional: `model_instructions_file = "<this repo>/prompts/codex-sysp.md"` in `~/.codex/config.toml`; explain first: replaces Codex's built-in instructions, so Codex's own prompt updates reach user only when file revised; `~/.codex/AGENTS.md` still loaded

## 6. Optional comforts

- quiet tone when harness finishes or asks (macOS only): Notification hooks: `afplay /System/Library/Sounds/Submarine.aiff` on `permission_prompt`; `afplay /System/Library/Sounds/Pop.aiff` on `idle_prompt`
- user's shell functions in harness shells: `env.BASH_ENV` (Codex: `[shell_environment_policy.set]`) → their aliases file
- Antigravity compaction (`~/.gemini/antigravity-cli/settings.json`): `"contextWindow": "900K"` (`"256K"`, `"512K"`, `"900K"`; env `AGY_CLI_AUTO_COMPACT_OVERRIDE`: `1%`–`100%` or token int)
- Antigravity status bar (same file): `"statusLine": {"type": "command", "command": "<venv>/bin/aai-hook agy-statusline", "enabled": true, "stack_with_default": true}` (`agy-statusline`: starting dir + context `%` and tokens from stdin JSON; `stack_with_default` keeps built-in bar; `/statusline` toggles)
- model, UI, sounds, optional features: personal; never copy from another user's config without asking

## 7. Restart and verify

- restart each configured harness (ask user); Codex with changed hooks: tell user to expect and accept its hook trust prompt
- fresh session, any directory, home too    /startup loads helpers without a project
- installed skills available; Antigravity: plugin rules (`AGENTS.md`, `GEMINI.md`, `kernel.md`) loaded; Claude Code: `~/.claude/rules/kernel.md` loaded
- kernel: state persists; Antigravity prints `startup.py` banner on `create(kernel="py")`; parallel `doc()` calls stay inline; `list_pyskills()` has `aai_coding.*` rows; `doc(acp)` renders; check helpers even if `--quiet` hid startup notice:

```python
create(kernel="py")
exec(code="setup_check = 1")
exec(code="setup_check + 1")   # 2
```

- one fork: own kernel with helpers, no `setup_check`; parent's current kernel, variable unchanged
- then: close check kernels
- failure: report step; fix its config before continuing

## Using the workspace

- activate `<venv>`, work in a project checkout; checkouts: separate Git repos, one shared environment, workspace packages editable
- before `ws-sync` updates: review `ws-status`; keep local work; after: restart harness sessions, kernels    /they load changed skills, code
- personal instructions, settings: outside this repo    /updates then need no reapplying

