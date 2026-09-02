import json, os
from datetime import datetime, timezone

import pytest
from shutil import which

from aai_coding.harness import bash_guard_msg, claude_air, claude_drop_sentinel, claude_slop, claude_session_start, codex_orientation, prompt_notices, synthetic_resume


def test_bash_guard():
    assert bash_guard_msg('pytest -q | tail -5')
    assert bash_guard_msg('foo|head -n 3')
    assert bash_guard_msg('foo | tail -19')
    assert bash_guard_msg('foo | tail -n19')
    assert bash_guard_msg('pytest -q | tail -20') is None
    assert bash_guard_msg('pytest -q | tail -50') is None
    assert bash_guard_msg('head -3 file.txt') is None      # no pipe: a file slice, not output truncation
    assert bash_guard_msg('ls') is None
    assert bash_guard_msg('pytest -q 2>&1 | tail -20')
    assert bash_guard_msg('maturin develop 2>&1')
    assert bash_guard_msg('foo 2> &1')
    assert bash_guard_msg('pytest -q >meta/stdout.txt 2>meta/stderr.txt') is None


def test_prompt_notices():
    def kinds(p): return [n.split()[2] for n in prompt_notices(p)]   # third word distinguishes the notices
    assert kinds('Is it done?  ') == ['ends']
    assert kinds('Done.') == []
    assert kinds('ok') == ['approval'] and kinds(' GO! ') == ['approval'] and kinds('Ok.') == ['approval']
    assert kinds('going') == [] and kinds('ok then') == []
    assert kinds('Please read the file') == ['appears']
    assert kinds('please read this?') == ['ends', 'appears']
    assert kinds('BTW can you also check the tests') == ['begins']
    assert kinds('the btw case is prefix-only') == []


def test_prompt_submit(capsys):
    from aai_coding.harness import claude_prompt_submit, codex_prompt_submit
    prompt = "BTW is the '# also activates the Message.to_parts/ai_output patches' still correct for llmsurgery?"
    for f,has_bug in ((claude_prompt_submit,True), (codex_prompt_submit,False)):
        f(dict(prompt=prompt))
        out = json.loads(capsys.readouterr().out)
        ctx = out['hookSpecificOutput']['additionalContext']
        assert out['hookSpecificOutput']['hookEventName'] == 'UserPromptSubmit'
        assert 'question' in ctx and 'side request' in ctx
        assert ('Claude Code bug' in ctx) is has_bug
    codex_prompt_submit(dict(prompt='all good'))
    assert capsys.readouterr().out == ''


def test_synthetic_resume(tmp_path):
    t = tmp_path/'t.jsonl'
    boundary = json.dumps(dict(type='system', subtype='compact_boundary'))
    start = json.dumps(dict(type='attachment', attachment=dict(hookEvent='SessionStart')))
    t.write_text(f'{start}\nnot json\n{boundary}\n')
    assert synthetic_resume(t)
    t.write_text(f'{boundary}\n{start}\n')
    assert not synthetic_resume(t)
    assert not synthetic_resume(tmp_path/'missing.jsonl')


def test_codex_orientation(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv('LLMDOJO_STATE_DIR', str(tmp_path))
    codex_orientation(dict(hook_event_name='PostCompact', session_id='s1', turn_id='t1'))
    codex_orientation(dict(hook_event_name='PreToolUse', session_id='s1'))
    out = json.loads(capsys.readouterr().out)
    assert out['hookSpecificOutput']['permissionDecision'] == 'deny'
    codex_orientation(dict(hook_event_name='PreToolUse', session_id='s1'))
    assert capsys.readouterr().out == ''                    # marker consumed: fires once


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
    (tmp_path/'air'/'s1.json').write_text('{"rounds": 2}}')
    batch()
    assert out() == ''                                      # a torn state file starts fresh instead of crashing
    assert json.loads((tmp_path/'air'/'s1.json').read_text())['rounds'] == 1


def _transcript(path, blocks_per_msg, prompt_uuid='u1'):
    "Write a transcript: one user prompt, then one assistant record per list of block types"
    recs = [dict(type='user', uuid=prompt_uuid, message=dict(content='do the thing'))]
    recs += [dict(type='assistant', message=dict(content=[dict(type=t) for t in bs])) for bs in blocks_per_msg]
    path.write_text('\n'.join(json.dumps(r) for r in recs))


def test_drop_sentinel(tmp_path, monkeypatch, capsys):
    "Scar -> report once at the first boundary; fresh holes re-fire; clean turns, subagents, and new prompts stay silent"
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
    fire(agent_id='sub1')
    assert out() == ''                                      # main session only
    tp.write_text('not json at all\n{"type": "garbage"')
    fire()
    assert out() == ''                                      # unparseable transcript: fail-open, silent on stdout


@pytest.mark.skipif(not which('slopometer'), reason='slopometer not installed')
def test_slop(tmp_path, monkeypatch, capsys):
    "Sloppy previous message -> context rows at the next prompt; repeats, subagents, short and clean prose stay silent"
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
    assert 'previous turn' in r['additionalContext'] and 'splice' in r['additionalContext']
    psub()
    assert out() == ''                                      # the same message reports once
    disp('m3', sloppy)
    psub(agent_id='sub1')
    assert out() == ''                                      # subagents are not scored
    disp('m4', "It isn't just short - it's a paradigm.")
    psub()
    assert out() == ''                                      # under the word gate: never scored, kills included
    disp('m5', 'The gateway never kills an unresponsive kernel. A kernel becomes dead only when its process exits. ' * 5)
    psub()
    assert out() == ''                                      # clean prose stays silent
    disp('m6', sloppy)
    monkeypatch.setenv('SLOP_WORST', '99')
    monkeypatch.setenv('SLOP_DENSITY', '1000')
    psub()
    assert out() == ''                                      # env overrides raise the bar
    monkeypatch.delenv('SLOP_WORST')
    monkeypatch.delenv('SLOP_DENSITY')
    disp('m7', sloppy)
    psub()
    assert 'previous turn' in json.loads(out())['hookSpecificOutput']['additionalContext']   # defaults return
    disp('m8', sloppy)
    psub(prompt=';')
    ctx = json.loads(out())['hookSpecificOutput']['additionalContext']
    assert 'did not understand' in ctx and 'previous turn' in ctx   # bare ; adds the restate notice to the report
    psub(prompt=';')
    ctx = json.loads(out())['hookSpecificOutput']['additionalContext']
    assert 'did not understand' in ctx and 'previous turn' not in ctx   # repeats restate only, scoring once
    psub(prompt="'")
    ctx = json.loads(out())['hookSpecificOutput']['additionalContext']
    assert 'caveat' in ctx and 'did not understand' not in ctx   # bare ' asks whether the closing caveat is real
