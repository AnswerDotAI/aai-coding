import json

from aai_coding.harness import bash_guard_msg, codex_orientation, prompt_notices, synthetic_resume


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
    doced = tmp_path/'doced'
    doced.mkdir()
    (doced/'123.json').write_text('["x"]')
    (doced/'abc.json').write_text('["x"]')
    codex_orientation(dict(hook_event_name='PostCompact', session_id='s1', turn_id='t1'))
    assert (doced/'123.json').read_text() == '[]'           # numeric stems reset
    assert (doced/'abc.json').read_text() == '["x"]'        # others untouched
    assert (doced/'s1.json').read_text() == '[]'
    codex_orientation(dict(hook_event_name='PreToolUse', session_id='s1'))
    out = json.loads(capsys.readouterr().out)
    assert out['hookSpecificOutput']['permissionDecision'] == 'deny'
    codex_orientation(dict(hook_event_name='PreToolUse', session_id='s1'))
    assert capsys.readouterr().out == ''                    # marker consumed: fires once
