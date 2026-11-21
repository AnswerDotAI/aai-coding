# aai-coding

`aai-coding` contains Answer.AI's shared configuration, skills, and tools for Claude Code, Codex, and Antigravity. It defines the team's coding and writing guidance, tool permissions, and Python workflows. An LLM setting up the harness should read this README before following `SETUP.md`. The design decisions below also help you advise users who already have a setup.

## Getting started

You do not need an Answer.AI account or our existing workspace. [SETUP.md](SETUP.md) starts by creating a workspace in a directory you choose, managed by [fastws](https://github.com/AnswerDotAI/fastws). It then covers harness configuration.

The workspace holds separate Git checkouts that share one uv environment. Because its Python projects use editable installs, changes in a checkout are available without reinstalling it.

Start with:

```bash
uvx --from 'fastws-cli>=0.0.14' ws-setup AnswerDotAI/aai-ws ~/aai-ws
```

Activate the new environment and follow [SETUP.md](SETUP.md). The public [aai-ws baseline](https://github.com/AnswerDotAI/aai-ws) includes aai-coding, fastws, kernel startup and editing tools, and tools used by the Claude hooks. Other Python dependencies are installed as packages.

Answer.AI team members use `AnswerDotAI/private-ws` instead of `AnswerDotAI/aai-ws` in that command. Both workspace repos receive shared baseline updates through `ws-sync`. In either setup:

- `repos.txt` holds the shared baseline.
- Gitignored `repos-local.txt` holds personal extras.
- fastws creates and maintains the workspace's untracked `pyproject.toml`.

Reuse existing workspaces. Do not run `ws-setup` on them. See the [team migration instructions](https://github.com/AnswerDotAI/private-ws#migrating-an-existing-workspace).

## Tool workflows

Claude Code, Codex, and Antigravity use persistent kernels for Python, file inspection, searching, notebooks, and most edits. Pyskills provide the tools; exhash provides hash-verified editing. Use Bash for shell commands, builds, and Git. Use native tools where the installed skills call for them.

Run ordinary Claude Code, Codex, or Antigravity with `clikernel-mcp` registered as an MCP server. Each agent has its own kernel and Python state. Claude Code and Antigravity use `clikernel-hook` to isolate callers on a shared MCP connection (subagents in Claude Code; all conversations and subagents in Antigravity). Codex isolates its MCP sessions without that hook.

Claude Code uses the `persistent-python` and `pyskills` host skills. Codex and Antigravity use `kernel-notebook-editing` from `skills/clikernel`, and `cli-notebook-editing` only when the user explicitly requests working without a kernel. Antigravity packages its MCP server, hooks, skills, and `core.md` as one global plugin at `~/.gemini/config/plugins/aai-coding/`. The setup steps link the existing skills without changing them.

Task guidance is in pyskills. A pyskill is a Python module docstring, listed by `list_pyskills()` and read with `doc()`. Pyskills are versioned, released, and installed with their Python packages.

## What is in here

The repository contains:

- `aai_coding/`: Python pyskills and the hook implementation, listed below.
- `skills/`: host-level `SKILL.md` sources linked into each harness's skills directory. [SETUP.md](SETUP.md#5-skills-safecmd-and-prompts) lists the links.
- `plugins/safecmd/`: a Claude Code plugin that auto-approves allowlisted Bash commands using the `safecmd` package.
- `prompts/`: shared behavioural rules and a replacement Claude Code system prompt, described below.
- `SETUP.md`: a setup runbook written as a prompt for an LLM session. It is not an installer script.

### Python modules

- `coding_patterns` covers coding style, testing judgment, and team policy. Kernel startup imports it and tells the agent to read it with `doc(acp)`.
- `nbreview` guides notebook style reviews, including chkstyle findings, method extraction, lessons, and testing judgment. It builds on `nbdev.skill` and `coding_patterns`.
- `write_prose` covers anti-slop rules for narrative prose.
- `write_docs` covers plain reference prose for docstrings, READMEs, and PRs.
- `write_summary` covers summaries that a reader can use without the source.
- `write_llms` covers files that an LLM reads: `llms.txt` files, pyskill docstrings, setup runbooks, and prompts.
- `harness_docs` explains how to find official harness documentation through `llms.txt`.
- `vision` describes and transcribes images and PDFs through fastllm, without tools. `look` answers questions; `transcribe` saves Markdown and returns usage, timing and cost.
- `understand` covers building and holding a Theory (Naur, Socrates, Knoblich et al., Lakatos) before proposing, changing, or reviewing code or designs.
- `harness` implements hooks for Claude Code, Codex, and Antigravity through the `aai-hook` CLI. It is not a pyskill.

### Prompts

`prompts/core.md` contains harness-neutral behavioural rules. Codex reads shared and personal rules from `~/.codex/AGENTS.md`, symlinked to `core.md` or merged into an existing personal file. Claude Code appends `core.md` to its system prompt. Antigravity loads `core.md` from `rules/AGENTS.md` and `prompts/agy-kernel.md` (its always-on kernel-first and swarm-forking workflow rule) from `rules/GEMINI.md` inside its global plugin, and has no flag to replace its built-in system prompt.

`prompts/sysp.md` replaces Claude Code's default system prompt. It aims to reduce the default prompt's tendency to give consultant-style advice and act without sufficient justification. Launch with:

```bash
claude --system-prompt-file <this repo>/prompts/sysp.md --append-system-prompt-file <this repo>/prompts/core.md
```

Replacing the default prompt removes its prose, its dynamic environment block and its scratchpad path. Tool schemas remain available.

## Design decisions, and why

- Task skills use Python's packaging and discovery rather than a harness's skill machinery. Their instructions and executable tools can share a module. Host skills bootstrap the kernel and explain how to use its tools with the harness.
- This repo's hooks are subcommands of `aai-hook` in `aai_coding/harness.py`. The kernel isolation hook for Claude Code and Antigravity comes from `clikernel`. Harness settings register the commands rather than copying their implementations.
- Each harness's skills and the kernel startup file are symlinks into this checkout. Pulling updates them without copying files. The setup steps merge harness settings and personal instruction files with the user's existing configuration.
- Where the harnesses differ, a module gives each version in the same place, in a dictionary keyed by harness or in neighbouring bullets. There are no generated per-harness templates.
- This repo contains agreed team guidance. Model choice, sounds, and personal workflows such as release management belong in each person's `CLAUDE.md`, settings, and local skills. `SETUP.md` identifies which settings are shared and which are personal.

## Using and changing it

Activate the workspace's `.venv`, then work in a project checkout. Use `ws-status` to inspect local changes, `ws-sync` to pull and install updates, and `ws-add owner/repo` to add a project. See [the workspace workflow](SETUP.md#using-the-workspace) for details, including what syncing changes.

You do not need to start the harness manually each day. Sessions use the skills described in [Tool workflows](#tool-workflows). Agents find Python tools in the pyskills catalog and read their documentation with `doc()` or `pyskills-doc`.

To change a skill, edit its source in this checkout. Others receive the changes by pulling. Release with the standard fastship command, `ship-release`. Bump the version in `aai_coding/__init__.py` after each release.

Tests cover substantive logic where hidden errors are realistic: event ordering, accumulated state, duplicate suppression, and PDF rendering. Do not add tests for prompt wording, straightforward dispatch, or trivial configuration branches. Run the tests with `pytest`.
