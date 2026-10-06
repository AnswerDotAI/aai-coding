import json

import pytest
from shutil import which

from aai_coding.harness import claude_air, claude_slop, last_request, synthetic_resume


def test_synthetic_resume(tmp_path):
    t = tmp_path/'t.jsonl'
    boundary = json.dumps(dict(type='system', subtype='compact_boundary'))
    start = json.dumps(dict(type='attachment', attachment=dict(hookEvent='SessionStart')))
    t.write_text(f'{start}\nnot json\n{boundary}\n')
    assert synthetic_resume(t)
    t.write_text(f'{boundary}\n{start}\n')
    assert not synthetic_resume(t)
    assert not synthetic_resume(tmp_path/'missing.jsonl')


def test_claude_air(tmp_path, monkeypatch, capsys):
    "Nudge at 8 tool rounds, renudge every 5, reset on substantive text (>=100 chars across a message's deltas) or a new prompt"
    monkeypatch.setenv('LLMDOJO_STATE_DIR', str(tmp_path))
    def batch(): claude_air(dict(hook_event_name='PostToolBatch', session_id='s1', tool_calls=[]))
    def out(): return capsys.readouterr().out
    for _ in range(7): batch()
    assert out() == ''                                      # under threshold: silent
    batch()
    assert 're-points your attention' in json.loads(out())['hookSpecificOutput']['additionalContext']
    for _ in range(4): batch()
    assert out() == ''                                      # renudge interval not yet reached
    batch()
    assert 'made 13 tool rounds' in json.loads(out())['hookSpecificOutput']['additionalContext']
    claude_air(dict(hook_event_name='MessageDisplay', session_id='s1', message_id='m1', final=False, delta='x'*60))
    claude_air(dict(hook_event_name='MessageDisplay', session_id='s1', message_id='m1', final=True, delta='x'*60))
    batch()
    assert out() == ''                                      # accumulated 120 chars reset the counter
    claude_air(dict(hook_event_name='MessageDisplay', session_id='s1', message_id='m2', final=True, delta='short'))
    for _ in range(6): batch()
    assert out() == ''                                      # a sub-100-char message resets nothing: 7 rounds now
    batch()
    assert 'made 8 tool rounds' in json.loads(out())['hookSpecificOutput']['additionalContext']
    claude_air(dict(hook_event_name='UserPromptSubmit', session_id='s1', prompt='hi'))
    batch()
    assert out() == ''                                      # new prompt reset


def test_last_request(tmp_path):
    "Quote the person's latest message, skipping tool results, notifications and skill text, and add the answered message after a short reply"
    t = tmp_path/'t.jsonl'
    def user(c, **kw): return dict(type='user', message=dict(role='user', content=c), **kw)
    def said(s): return dict(type='assistant', message=dict(content=[dict(type='text', text=s)]))
    long = 'Please fix the parser so reference links resolve across blocks, then add a lesson that shows the old failure and the new result in the notebook'
    rows = [user(long), said('Fixed it.'), user([dict(type='tool_result', content='ok')]),
        user('<task-notification>done</task-notification>'), user([dict(type='text', text='skill text')], isMeta=True)]
    t.write_text('\n'.join(map(json.dumps, rows)))
    assert last_request(t) == f'"{long}"'
    rows.append(dict(type='attachment', attachment=dict(type='queued_command', prompt='ok go')))
    t.write_text('\n'.join(map(json.dumps, rows)))
    assert last_request(t) == '"ok go" (replying to your message: "Fixed it.")'
    t.write_text(json.dumps(user([dict(type='text', text='<fork-boilerplate>\nrules\nYour directive: Your part: item 3')])))
    assert last_request(t) == '"Your part: item 3"'
    assert last_request(tmp_path/'missing.jsonl') is None


@pytest.mark.skipif(not which('slopometer'), reason='slopometer not installed')
def test_slop(tmp_path, monkeypatch, capsys):
    "Buffer message deltas, score only the final message, and report it once"
    monkeypatch.setenv('LLMDOJO_STATE_DIR', str(tmp_path))
    def disp(mid, txt, final=True, **kw): claude_slop(dict(hook_event_name='MessageDisplay', session_id='s1', message_id=mid, delta=txt, final=final, **kw))
    def psub(**kw): claude_slop(dict(hook_event_name='UserPromptSubmit', session_id='s1', **kw))
    def out(): return capsys.readouterr().out
    sloppy = "This isn't just a linter - it's a comprehensive paradigm that will streamline your workflow. " * 3
    disp('m1', 'a mid-turn note that nobody should score')
    disp('m2', sloppy[:40], final=False)
    disp('m2', sloppy[40:])
    assert out() == ''                                      # display tracking is silent
    psub()
    r = json.loads(out())['hookSpecificOutput']
    assert 'previous turn' in r['additionalContext'] and 'notxbuty' in r['additionalContext']
    psub()
    assert out() == ''                                      # the same message reports once
