import json

import pytest
from shutil import which

from aai_coding.harness import claude_air, claude_drop_sentinel, claude_slop, synthetic_resume


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


def _transcript(path, blocks_per_msg, prompt_uuid='u1'):
    "Write a transcript: one user prompt, then one assistant record per list of block types"
    recs = [dict(type='user', uuid=prompt_uuid, message=dict(content='do the thing'))]
    recs += [dict(type='assistant', message=dict(content=[dict(type=t) for t in bs])) for bs in blocks_per_msg]
    path.write_text('\n'.join(json.dumps(r) for r in recs))


def test_drop_sentinel(tmp_path, monkeypatch, capsys):
    "Report new scars once across batch and stop events, resetting the count for each turn"
    monkeypatch.setenv('LLMDOJO_STATE_DIR', str(tmp_path))
    tp = tmp_path/'t.jsonl'
    def fire(ev='PostToolBatch', **kw): claude_drop_sentinel(dict(hook_event_name=ev, session_id='s1', transcript_path=str(tp), **kw))
    def out(): return capsys.readouterr().out
    _transcript(tp, [['thinking', 'text', 'tool_use'], ['thinking', 'tool_use']])
    fire()
    assert out() == ''                                      # clean turn: no adjacent thinking
    _transcript(tp, [['thinking', 'thinking', 'tool_use']])
    fire()
    r = json.loads(out())['hookSpecificOutput']
    assert r['hookEventName'] == 'PostToolBatch' and 'thinking blocks in a row' in r['additionalContext'] and 'end the turn' in r['additionalContext']
    fire()
    assert out() == ''                                      # already claimed: silent
    fire('Stop')
    assert out() == ''                                      # backstop silent after the batch boundary reported
    _transcript(tp, [['thinking', 'thinking', 'tool_use'], ['thinking', 'thinking', 'tool_use']])
    fire()
    assert 'thinking blocks in a row' in json.loads(out())['hookSpecificOutput']['additionalContext']   # only the fresh hole
    _transcript(tp, [['thinking', 'thinking', 'tool_use']]*3)
    fire('Stop')
    r = json.loads(out())
    assert r['decision'] == 'block' and 'thinking blocks in a row' in r['reason'] and 'state that missing thing now' in r['reason']
    fire('Stop')
    assert out() == ''                                      # blocks once, not forever
    _transcript(tp, [['thinking', 'thinking', 'tool_use']], prompt_uuid='u2')
    fire()
    assert 'thinking blocks in a row' in json.loads(out())['hookSpecificOutput']['additionalContext']   # new turn: count restarts


def test_desktop_relaxed(tmp_path, monkeypatch, capsys):
    "Desktop sessions keep native Write/Edit (never NotebookEdit) and get core.md instead of the bootstrap gate; terminal sessions enforce both"
    from aai_coding.harness import claude_block_native_edit, claude_session_start
    monkeypatch.setenv('CLAUDE_PROJECT_DIR', str(tmp_path))
    (tmp_path/'pyproject.toml').write_text('')
    monkeypatch.setenv('CLAUDE_CODE_ENTRYPOINT', 'claude-desktop')
    claude_block_native_edit(dict(tool_name='Edit'))
    with pytest.raises(SystemExit): claude_block_native_edit(dict(tool_name='NotebookEdit'))   # its writer's escape churn corrupts notebooks
    for source in ('startup', 'resume', 'compact'):
        claude_session_start(dict(source=source, session_id='s1'))
        out = capsys.readouterr().out
        assert 'final text message' in out and 'dojo' not in out
    monkeypatch.setenv('CLAUDE_CODE_ENTRYPOINT', 'cli')
    with pytest.raises(SystemExit): claude_block_native_edit(dict(tool_name='Edit'))
    claude_session_start(dict(source='startup', session_id='s1'))
    out = capsys.readouterr().out
    assert 'NEVER touch local files' in out and 'final text message' not in out


@pytest.mark.skipif(not which('slopometer'), reason='slopometer not installed')
def test_slop(tmp_path, monkeypatch, capsys):
    "Buffer message deltas, score only the final message, and report it once"
    monkeypatch.setenv('LLMDOJO_STATE_DIR', str(tmp_path))
    def disp(mid, txt, final=True, **kw): claude_slop(dict(hook_event_name='MessageDisplay', session_id='s1', message_id=mid, delta=txt, final=final, **kw))
    def psub(**kw): claude_slop(dict(hook_event_name='UserPromptSubmit', session_id='s1', **kw))
    def out(): return capsys.readouterr().out
    sloppy = "This isn't just a linter - it's a comprehensive paradigm that will streamline your workflow. " * 12
    disp('m1', 'a mid-turn note that nobody should score')
    disp('m2', sloppy[:40], final=False)
    disp('m2', sloppy[40:])
    assert out() == ''                                      # display tracking is silent
    psub()
    r = json.loads(out())['hookSpecificOutput']
    assert 'previous turn' in r['additionalContext'] and 'splice' in r['additionalContext']
    psub()
    assert out() == ''                                      # the same message reports once


@pytest.mark.skipif(not which('slopometer'), reason='slopometer not installed')
def test_codex_slop(tmp_path, monkeypatch, capsys):
    "Codex Stop captures the final reply; the next prompt reports it once and handles the punctuation notices"
    from aai_coding.harness import codex_slop
    monkeypatch.setenv('LLMDOJO_STATE_DIR', str(tmp_path))
    def stop(tid, txt): codex_slop(dict(hook_event_name='Stop', session_id='s1', turn_id=tid, last_assistant_message=txt))
    def psub(prompt='hi'): codex_slop(dict(hook_event_name='UserPromptSubmit', session_id='s1', prompt=prompt))
    def out(): return capsys.readouterr().out
    sloppy = "This isn't just a linter - it's a comprehensive paradigm that will streamline your workflow. " * 12
    stop('t1', sloppy)
    assert json.loads(out()) == {}
    psub()
    ctx = json.loads(out())['hookSpecificOutput']['additionalContext']
    assert 'previous turn' in ctx and 'splice' in ctx
    psub()
    assert out() == ''
    stop('t2', 'The parser rejects malformed input. ' * 10)
    assert json.loads(out()) == {}
    psub(';')
    ctx = json.loads(out())['hookSpecificOutput']['additionalContext']
    assert 'did not understand' in ctx and 'previous turn' not in ctx


@pytest.mark.skipif(not which('slopometer'), reason='slopometer not installed')
def test_slop_short_report():
    "The scorer can decline a message above the hook's local word threshold."
    from aai_coding.harness import _slop_report
    assert _slop_report('The parser rejects malformed input. ' * 10) == []


def test_browser_prompt_shortcuts(tmp_path, monkeypatch, capsys):
    "Browser context must not hide a punctuation request or become the request itself."
    from aai_coding.harness import codex_slop, codex_prompt_submit
    monkeypatch.setenv('LLMDOJO_STATE_DIR', str(tmp_path))
    wrapper = '''
<in-app-browser-context source="ambient-ui-state">
This block is automatically supplied ambient UI state, not part of the user's request.
# In app browser:
- Current URL: http://127.0.0.1:5197/?pr=example
</in-app-browser-context>

## My request:
'''
    annotation = '# Response annotations:\n<response-annotations>[]</response-annotations>\n## My request:\n'
    for prefix in ('', wrapper, annotation):
        codex_slop(dict(hook_event_name='UserPromptSubmit', session_id='browser', prompt=prefix+';\n'))
        expected = 'selected text' if prefix == annotation else 'did not understand'
        assert expected in json.loads(capsys.readouterr().out)['hookSpecificOutput']['additionalContext']
        codex_prompt_submit(dict(prompt=prefix+"'\n"))
        assert 'caveat' in json.loads(capsys.readouterr().out)['hookSpecificOutput']['additionalContext']
    for prompt in (wrapper+'Explain the semicolon ;', 'Quoted example:\n'+wrapper+';'):
        codex_slop(dict(hook_event_name='UserPromptSubmit', session_id='browser', prompt=prompt))
        assert capsys.readouterr().out == ''
    codex_slop(dict(hook_event_name='UserPromptSubmit', session_id='browser', prompt=annotation+'; Why does this happen?'))
    ctx = json.loads(capsys.readouterr().out)['hookSpecificOutput']['additionalContext']
    assert 'selected text' in ctx and 'answer' in ctx and 'question' in ctx
