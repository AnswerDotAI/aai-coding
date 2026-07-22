# safecmd Claude Code Plugin

Auto-approve safe bash commands in Claude Code using safecmd's allowlist.

## Prerequisites

Install safecmd:
```bash
pip install safecmd
```

## Installation

Add the marketplace, then install:

```bash
/plugin marketplace add AnswerDotAI/skill-plugins
/plugin install safecmd@answerdotai-skill-plugins
```

A local clone works as the marketplace too: `/plugin marketplace add /path/to/skill-plugins`.

For local development, skip installation and symlink the plugin into your skills directory. It loads in place as `safecmd@skills-dir`, so edits in the repo are live (run `/reload-plugins` after changing `hooks/hooks.json`):

```bash
ln -s /path/to/skill-plugins/plugins/safecmd ~/.claude/skills/safecmd
```

Note that installing copies a snapshot into Claude Code's plugin cache: repo edits don't reach an installed copy until you update the plugin, which is why the symlink route is better for development.

## How It Works

This plugin adds a `PreToolUse` hook for the `Bash` tool that:

1. Intercepts bash commands before execution
2. Validates them against safecmd's allowlist using AST parsing
3. Auto-approves safe commands (no permission prompt)
4. Falls through to normal permission prompt for disallowed commands

## Settings Requirements

Do not put a broad `Bash` rule anywhere in your Claude Code `permissions` settings:

- `Bash` or `Bash(*)` in `allow` silently approves every command the moment this plugin defers, so nothing ever prompts and the allowlist does nothing.
- A bare `Bash` in `deny` removes the Bash tool from Claude entirely.
- No `ask` rule is needed: a command that isn't auto-approved falls through to Claude Code's standard permission prompt on its own, including its "no, and tell Claude what to do differently" text reply.

Narrow rules for specific commands (e.g. `Bash(git status*)` in `allow`) are fine, and still apply after the hook defers.

## Configuration

The allowlist lives in safecmd's config file at `$XDG_CONFIG_HOME/safecmd/config.ini`, which is `~/.config/safecmd/config.ini` by default, on all platforms.

See [safecmd documentation](https://github.com/AnswerDotAI/safecmd) for details on customizing the allowlist.
