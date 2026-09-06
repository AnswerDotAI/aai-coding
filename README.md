# aai-coding

The Answer.AI coding harness: the shared configuration, skills, and tooling that make a Claude Code or codex session work the way our team works. If you are an LLM reading this, you are probably either setting the harness up (follow `SETUP.md`, but read this file first) or working inside it and wanting to understand why it is shaped this way, so you can give your user informed advice.

## Getting started

You do not need an Answer.AI account or our existing workspace. [SETUP.md](SETUP.md) starts with a workspace in a directory you choose, managed by [fastws](https://github.com/AnswerDotAI/fastws), then walks through configuring the harness. The workspace holds separate Git checkouts sharing one uv environment; its Python projects are installed editably, so changes in a checkout are available without reinstalling it.

The copyable [repos.txt](repos.txt) supplies a small starter workspace for the setup below, not our full collection of projects. It includes aai-coding, fastws, the kernel startup and editing tools, and the tools used by the Claude hooks. Other Python dependencies are installed as packages; add their repos when you want editable source checkouts too.

## The system in one paragraph

The Claude Code setup and one codex setup are kernel-centric: native file tools are denied, and file reading, editing, searching, and Python execution go through one persistent IPython kernel (clikernel) loaded with curated tooling discovered via `pyskills`. Codex can instead use a hybrid setup: normal `apply_patch` and Bash for files and shell work, with a quiet clikernel reserved for Python-specific work. The kernel-centric setup uses two host-level bootstrap skills, `persistent-python` and `pyskills`; the hybrid setup uses `clikernel-workflow` to define the boundary and `notebook-dialog-editing` as the CLI adapter for the required `aidialog.dlgskill` entry point. That adapter overrides pyskill tool preferences for local files: use native tools within allowed editing locations. Everything else that would conventionally be a host skill is a pyskill in this package: skill text lives in module docstrings, read with `doc()`, listed by `list_pyskills()`, and versioned, released, and installed like any other Python code.

## What is in here

- `aai_coding/` - the pyskills. `coding_patterns` (style, testing judgment, and team policy; part of the kernel startup doc round), `write_prose` (anti-slop rules for narrative prose), `write_docs` (the voiceless register for docstrings, READMEs, and PRs), `harness_docs` (how to find official harness docs via llms.txt), and `harness` (not a skill: the `aai-hook` CLI that implements both harnesses' hooks).
- `skills/` - the harness-level SKILL.md sources, symlinked into `~/.claude/skills` or `~/.codex/skills`. `persistent-python` and `pyskills` bootstrap the kernel-centric setup; `clikernel` and `notebook-dialog-editing` support the hybrid codex setup.
- `plugins/safecmd/` - a Claude Code plugin that auto-approves allowlisted Bash commands via the `safecmd` package, so the deny-heavy permission setup stays livable.
- `prompts/` - shared prompt text. `core.md` holds harness-neutral behavioral rules: codex reads it natively via a `~/.codex/AGENTS.md` symlink, and Claude Code can append it. `sysp.md` is a full replacement for Claude Code's default system prompt, tuned against the default's consultant and action biases; install it as a `~/.claude/sysp` symlink and launch with `claude --system-prompt-file ~/.claude/sysp --append-system-prompt-file <this repo>/prompts/core.md` (replacement drops the default prompt's prose but tool schemas survive; the dynamic environment block and scratchpad path are the known losses).
- `SETUP.md` - the setup runbook, written as a prompt for an LLM session rather than an installer script.
- `repos.txt` - a starter repo list to copy into your workspace root, then extend with your own projects.

## Design decisions, and why

- **Task skills are pyskills.** In a kernel-centric harness the native skill list stops being the discovery surface; `list_pyskills()` is. Docstrings-as-skill-text means nothing depends on the harness's skill machinery. It also lets skill text live beside its executable companions in one module. The hybrid codex workflow remains a host skill because it tells codex when to cross into the kernel at all.
- **Hooks are a CLI.** Every hook body is a subcommand of `aai-hook` (`aai_coding/harness.py`): versioned, unit-tested Python instead of shell one-liners scattered through settings files. Harness configs only register command names.
- **Everything installs by symlink.** Like the workspace's editable installs, config points into the checkout, so `git pull` updates every machine and there is no copy to drift. The only exceptions are settings files that must be merged (Claude Code's `settings.json`, codex's `config.toml`), which is why setup is a runbook and not a script: merging into someone's existing configuration takes judgment and conversation, which an LLM has and an installer does not.
- **Per-harness differences are data, not templates.** Where Claude Code and codex genuinely differ, a module carries both facts (a `dict` keyed by harness, or two adjacent bullets); nothing is rendered or generated.
- **Team-agreeable versus personal.** This repo holds only what any team member would nod at. Personal preferences (model choice, sounds people disagree about, individual workflow like release management) belong in each person's own CLAUDE.md, settings, and local skills, and the runbook is explicit about which is which.

## Using and changing it

Activate the workspace's `.venv`, then work in a project checkout. Use `ws-status` to inspect local changes, `ws-sync` to pull and install updates, and `ws-add owner/repo` to add a project. See [the workspace workflow](SETUP.md#using-the-workspace) for details, including what syncing changes.

The harness itself needs no manual startup each day. Kernel-centric sessions bootstrap through `persistent-python`; hybrid codex sessions use `clikernel-workflow` for Python, `notebook-dialog-editing` for notebooks and aidialog dialogs, and the native tools otherwise. Both discover Python tooling through the pyskills catalog and read it with `doc()` or `pyskills-doc`. To change a skill, edit its source in this checkout and let others pick it up by pulling; releases go through the standard fastship flow (`ship-release`), with the version in `aai_coding/__init__.py` bumped after each release.

Tests cover substantive logic where hidden errors are realistic: event ordering, accumulated state, duplicate suppression, and PDF rendering. Do not add tests for prompt wording, straightforward dispatch, or trivial configuration branches. Run the retained tests with `pytest`.
