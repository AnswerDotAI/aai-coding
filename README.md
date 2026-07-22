# aai-coding

The Answer.AI coding harness: the shared configuration, skills, and tooling that make a Claude Code or codex session work the way our team works. If you are an LLM reading this, you are probably either setting the harness up (follow `SETUP.md`, but read this file first) or working inside it and wanting to understand why it is shaped this way, so you can give your user informed advice.

## The system in one paragraph

Sessions here run bash-and-python-only: the harness's native file tools are denied, and all file reading, editing, and searching goes through one persistent IPython kernel (clikernel) loaded with curated tooling discovered via `pyskills`. Two host-level skills exist solely to get a session into that kernel: `persistent-python` (the bootstrap ladder) and `pyskills` (a catch-all trigger whose whole message is "the tooling catalog lives in the kernel"). Everything else that would conventionally be a host skill is a pyskill in this package: skill text lives in module docstrings, read with `doc()`, listed by `list_pyskills()`, and versioned, released, and installed like any other Python code.

## What is in here

- `aai_coding/` - the pyskills. `coding_patterns` (style, testing judgment, and team policy; part of the kernel startup doc round), `write_prose` (anti-slop prose rules), `harness_docs` (how to find official harness docs via llms.txt), and `harness` (not a skill: the `aai-hook` CLI that implements both harnesses' hooks).
- `skills/` - the two harness-level SKILL.md sources, symlinked into `~/.claude/skills` and `~/.codex/skills`.
- `plugins/safecmd/` - a Claude Code plugin that auto-approves allowlisted Bash commands via the `safecmd` package, so the deny-heavy permission setup stays livable.
- `prompts/` - shared prompt text. `core.md` holds harness-neutral behavioral rules: codex reads it natively via a `~/.codex/AGENTS.md` symlink, and Claude Code can append it. `sysp.md` is a full replacement for Claude Code's default system prompt, tuned against the default's consultant and action biases; install it as a `~/.claude/sysp` symlink and launch with `claude --system-prompt-file ~/.claude/sysp --append-system-prompt-file <this repo>/prompts/core.md` (replacement drops the default prompt's prose but tool schemas survive; the dynamic environment block and scratchpad path are the known losses).
- `SETUP.md` - the setup runbook, written as a prompt for an LLM session rather than an installer script.

## Design decisions, and why

- **Skills are pyskills.** In a kernel-centric harness the native skill list stops being the discovery surface; `list_pyskills()` is. Docstrings-as-skill-text means the mechanical doc-state tracking (llmdojo) knows exactly which skills a session has read, re-fires them after compaction, and nothing depends on the harness's skill machinery. It also lets skill text live beside its executable companions in one module.
- **Hooks are a CLI.** Every hook body is a subcommand of `aai-hook` (`aai_coding/harness.py`): versioned, unit-tested Python instead of shell one-liners scattered through settings files. Harness configs only register command names.
- **Everything installs by symlink.** Like the workspace's editable installs, config points into the checkout, so `git pull` updates every machine and there is no copy to drift. The only exceptions are settings files that must be merged (Claude Code's `settings.json`, codex's `config.toml`), which is why setup is a runbook and not a script: merging into someone's existing configuration takes judgment and conversation, which an LLM has and an installer does not.
- **Per-harness differences are data, not templates.** Where Claude Code and codex genuinely differ, a module carries both facts (a `dict` keyed by harness, or two adjacent bullets); nothing is rendered or generated.
- **Team-agreeable versus personal.** This repo holds only what any team member would nod at. Personal preferences (model choice, sounds people disagree about, individual workflow like release management) belong in each person's own CLAUDE.md, settings, and local skills, and the runbook is explicit about which is which.

## Using and changing it

Day to day there is nothing to operate: sessions bootstrap through `persistent-python`, discover tooling through the catalog, and read skills with `doc()`. To change a skill, edit its module docstring like any code and let the team pick it up by pulling; releases go through the standard fastship flow (`ship-release`), with the version in `aai_coding/__init__.py` bumped after each release.
