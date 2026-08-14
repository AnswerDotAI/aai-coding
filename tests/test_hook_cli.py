"""Subprocess-level contract tests for the aai-hook CLI: invoke each registered subcommand the way
Claude Code does - JSON event payload on stdin, desktop or CLI env - and hold it to the hook
contract. A hook that crashes (nonzero exit, traceback on stderr) or prints non-JSON where JSON is
expected is an error the frontend can surface as an interrupted tool call, so the contract is:
exit 0, stdout empty or one JSON object (SessionStart prints plain context text), nonzero exits
only from the intended CLI enforcement blocks, and no crash on degenerate payloads."""
import json, os, subprocess, sys
from pathlib import Path

import pytest

HOOK = Path(sys.executable).parent/'aai-hook'
SUBS = ('claude-session-start', 'claude-bash-guard', 'claude-block-native-edit', 'claude-prompt-submit',
    'claude-air', 'claude-drop-sentinel', 'claude-slop', 'claude-dojo-sample')
EVENTS = [   # every (subcommand, payload) pair the SETUP.md registrations can produce
    ('claude-session-start', dict(hook_event_name='SessionStart', source='startup')),
    ('claude-bash-guard', dict(hook_event_name='PreToolUse', tool_name='Bash', tool_input=dict(command='ls'))),
    ('claude-block-native-edit', dict(hook_event_name='PreToolUse', tool_name='Edit', tool_input=dict(file_path='x.py'))),
    ('claude-prompt-submit', dict(hook_event_name='UserPromptSubmit', prompt='hello')),
    ('claude-air', dict(hook_event_name='UserPromptSubmit', prompt='hello')),
    ('claude-air', dict(hook_event_name='PostToolBatch', tool_calls=[])),
    ('claude-air', dict(hook_event_name='MessageDisplay', message_id='m1', delta='x', final=True)),
    ('claude-drop-sentinel', dict(hook_event_name='PostToolBatch')),
    ('claude-drop-sentinel', dict(hook_event_name='Stop')),
    ('claude-slop', dict(hook_event_name='MessageDisplay', message_id='m1', delta='x', final=True)),
    ('claude-slop', dict(hook_event_name='UserPromptSubmit', prompt='next')),
    ('claude-dojo-sample', dict(hook_event_name='PreToolUse', tool_name='mcp__clikernel__execute')),
]


def run_hook(sub, payload, tmp, desktop=False):
    env = os.environ | dict(LLMDOJO_STATE_DIR=str(tmp), CLAUDE_PROJECT_DIR=str(tmp))
    env.pop('CLAUDE_CODE_ENTRYPOINT', None)
    if desktop: env['CLAUDE_CODE_ENTRYPOINT'] = 'claude-desktop'
    inp = payload if isinstance(payload, str) else json.dumps(payload)
    return subprocess.run([str(HOOK), sub], input=inp, text=True, capture_output=True, env=env, timeout=60)


def out_ok(r, sub):
    if not r.stdout.strip(): return True
    if sub == 'claude-session-start': return True   # SessionStart stdout is plain context text
    return isinstance(json.loads(r.stdout), dict)


@pytest.mark.parametrize('desktop', (False, True))
def test_registered_events(tmp_path, desktop):
    "Every registered pair honors the contract; the only nonzero exit is the CLI native-edit block"
    for sub, ev in EVENTS:
        r = run_hook(sub, dict(ev, session_id='s1'), tmp_path, desktop)
        expected = 2 if sub == 'claude-block-native-edit' and not desktop else 0
        assert r.returncode == expected, (sub, ev, r.returncode, r.stderr)
        assert out_ok(r, sub), (sub, ev, r.stdout)


def test_intended_blocks(tmp_path):
    "CLI enforcement blocks exit 2 with the redirect on stderr and nothing on stdout"
    r = run_hook('claude-block-native-edit', dict(hook_event_name='PreToolUse', session_id='s1', tool_input=dict(file_path='x')), tmp_path)
    assert r.returncode == 2 and 'clikernel' in r.stderr and r.stdout == ''
    r = run_hook('claude-bash-guard', dict(hook_event_name='PreToolUse', session_id='s1', tool_input=dict(command='x | head -3')), tmp_path)
    assert r.returncode == 2 and 'truncat' in r.stderr and r.stdout == ''


def test_degenerate_payloads(tmp_path):
    "An empty payload or empty stdin never crashes a hook: the frontend treats a crash as an error"
    for sub in SUBS:
        for payload in ({}, ''):
            r = run_hook(sub, payload, tmp_path, desktop=True)
            assert r.returncode == 0, (sub, payload, r.stderr)
            assert out_ok(r, sub), (sub, payload, r.stdout)
