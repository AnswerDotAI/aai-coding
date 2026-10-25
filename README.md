# aai-coding

`aai-coding` contains Answer.AI's shared configuration, skills, and tools for Claude Code and Codex. It defines the team's coding and writing guidance, tool permissions, and Python workflows. An LLM setting up the harness should read this README before following `SETUP.md`. The design decisions below also provide context for advising users of an existing setup.

## Getting started

You do not need an Answer.AI account or our existing workspace. [SETUP.md](SETUP.md) starts with a workspace in a directory you choose, managed by [fastws](https://github.com/AnswerDotAI/fastws). It then covers harness configuration.

The workspace holds separate Git checkouts sharing one uv environment. Its Python projects use editable installs. Changes in a checkout are available without reinstalling it.

Start with:

```bash
uvx --from 'fastws-cli>=0.0.14' ws-setup AnswerDotAI/aai-ws ~/aai-ws
```

Activate the new environment and follow [SETUP.md](SETUP.md). The public [aai-ws baseline](https://github.com/AnswerDotAI/aai-ws) includes aai-coding, fastws, kernel startup and editing tools, and tools used by the Claude hooks. Other Python dependencies install as packages.

Answer.AI team members use `AnswerDotAI/private-ws` instead of `AnswerDotAI/aai-ws` in that command. Both workspace repos receive shared baseline updates through `ws-sync`. In either setup:

- `repos.txt` holds the shared baseline.
- Gitignored `repos-local.txt` holds personal extras.
- fastws creates and maintains the workspace's untracked `pyproject.toml`.

Reuse existing workspaces. Do not run `ws-setup` on them. See the [team migration instructions](https://github.com/AnswerDotAI/private-ws#migrating-an-existing-workspace).

## Tool workflows

Claude Code and Codex use persistent kernels for Python, file inspection, searching, notebooks, and most edits. Pyskills provide the tools; exhash provides hash-verified editing. Use Bash for shell commands, builds, and Git. Native tools remain available where the installed skills call for them.

Run ordinary Claude Code or Codex with `clikernel-mcp` registered as an MCP server. Each agent has its own kernel and Python state. Claude's `clikernel-hook` supplies subagent identity; Codex isolates its MCP sessions without that hook.

Claude uses the `persistent-python` and `pyskills` host skills. Codex uses `kernel-notebook-editing` from `skills/clikernel`. Its `cli-notebook-editing` skill applies only when the user explicitly requests working without a kernel. Setup links the existing skills without changing them.

Task guidance lives in pyskills. A pyskill is a Python module docstring, listed by `list_pyskills()` and read with `doc()`. Pyskills are versioned, released, and installed with their Python packages.

## What is in here

The repository contains:

- `aai_coding/`: Python pyskills and the hook implementation, listed below.
- `skills/`: host-level `SKILL.md` sources linked into each harness's skills directory. [SETUP.md](SETUP.md#5-skills-safecmd-and-prompts) lists the links.
- `plugins/safecmd/`: a Claude Code plugin that auto-approves allowlisted Bash commands using the `safecmd` package.
- `prompts/`: shared behavioural rules and a replacement Claude Code system prompt, described below.
- `SETUP.md`: a setup runbook written as a prompt for an LLM session. It is not an installer script.

### Python modules

- `coding_patterns` covers coding style, testing judgment, and team policy. Kernel startup includes reading it.
- `nbreview` guides notebook style reviews, including chkstyle findings, method extraction, lessons, and testing judgment. It builds on `nbdev.skill` and `coding_patterns`.
- `write_prose` covers anti-slop rules for narrative prose.
- `write_docs` covers plain reference prose for docstrings, READMEs, and PRs.
- `harness_docs` explains how to find official harness documentation through `llms.txt`.
- `vision` describes and transcribes images and PDFs through fastllm, without tools. `look` answers questions; `transcribe` saves Markdown and returns usage, timing and cost.
- `harness` implements both harnesses' hooks through the `aai-hook` CLI. It is not a pyskill.

### Prompts

`prompts/core.md` contains harness-neutral behavioural rules. Codex reads shared and personal rules from `~/.codex/AGENTS.md`. Setup can symlink that file to `core.md` or merge the shared rules into an existing personal file. Claude Code can append `core.md` to its system prompt.

`prompts/sysp.md` replaces Claude Code's default system prompt. It aims to reduce the default prompt's tendency to give consultant-style advice and act without sufficient justification. Launch with:

```bash
claude --system-prompt-file <this repo>/prompts/sysp.md --append-system-prompt-file <this repo>/prompts/core.md
```

Replacement removes the default prompt's prose. Tool schemas remain available. The default prompt's dynamic environment block and scratchpad path are lost.

## Design decisions, and why

- Task skills use Python's packaging and discovery rather than a harness's skill machinery. Their instructions and executable tools can share a module. Host skills bootstrap the kernel and explain how to use its tools with the harness.
- This repo's hooks are subcommands of `aai-hook` in `aai_coding/harness.py`. Claude's kernel isolation hook comes from clikernel. Harness settings register the commands rather than copying their implementations.
- Symlinks point skills and startup at the checkout. Pulling updates changes those sources without copying files. Setup merges harness settings and personal instruction files with the user's existing configuration.
- Modules record differences between harnesses directly, using a dictionary keyed by harness or adjacent bullets. There are no generated per-harness templates.
- This repo contains agreed team guidance. Model choice, sounds, and personal workflows such as release management belong in each person's `CLAUDE.md`, settings, and local skills. The runbook identifies which settings are shared and which are personal.

## Using and changing it

Activate the workspace's `.venv`, then work in a project checkout. Use `ws-status` to inspect local changes, `ws-sync` to pull and install updates, and `ws-add owner/repo` to add a project. See [the workspace workflow](SETUP.md#using-the-workspace) for details, including what syncing changes.

The harness needs no manual startup each day. Sessions use the skills described in [Tool workflows](#tool-workflows). Both setups discover Python tools through the pyskills catalog and read their documentation with `doc()` or `pyskills-doc`.

To change a skill, edit its source in this checkout. Others receive the changes by pulling. Releases use the standard fastship command, `ship-release`. Bump the version in `aai_coding/__init__.py` after each release.

Tests cover substantive logic where hidden errors are realistic: event ordering, accumulated state, duplicate suppression, and PDF rendering. Do not add tests for prompt wording, straightforward dispatch, or trivial configuration branches. Run the retained tests with `pytest`.
