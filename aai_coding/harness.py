"""Hook implementations for the team harness, installed as the `aai-hook` CLI. Each subcommand is registered in a harness's hook config (Claude Code settings.json or codex hooks.json) and reads the hook event's JSON payload from stdin. See SETUP.md for the wiring."""
import json, os, re, sys
from datetime import datetime
from pathlib import Path

__all__ = ['main']

NO_TRUNCATE = ('Output pipe truncates below 20 lines. Drop the pipe or keep >=20: truncation is decided '
    'before the output exists, so keep enough to diagnose surprises.')
NO_STDERR_MERGE = ('Do not merge stderr into stdout with 2>&1. Remove redirection entirely where possible - '
    'the harness automatically pushes large outputs to external files when needed; use this form where '
    'strictly needed: `>meta/stdout.txt 2>meta/stderr.txt`, reading the files with clikernel.')
_TRUNC = re.compile(r'\|\s*(tail|head)\s+(-n\s*)?-?([1-9]|1[0-9])\b')
_MERGE = re.compile(r'2>\s*&\s*1')


def bash_guard_msg(cmd):
    "The objection `cmd` earns - a sub-20-line head/tail pipe, or a 2>&1 stderr merge - else None"
    if _MERGE.search(cmd): return NO_STDERR_MERGE
    return NO_TRUNCATE if _TRUNC.search(cmd) else None


Q_NOTICE = ('This prompt ends with a question mark, so it seems to be a question. Claude Code bug: any tool '
    'call made after your answer text prevents the answer from displaying. Make only the tool calls needed '
    'to get the answer, then answer, then stop.')
READ_NOTICE = ('This prompt appears to contain a request to read something. If it could reasonably be interpreted that way, '
    'read the target in full NOW, before composing any response: a notebook via summary_dlg then view_dlg/find_msgs as needed; '
    'a .py or other text file in full. Never respond from assumed or remembered contents.')
APPROVAL_NOTICE = ('This bare approval covers exactly what was explicitly agreed, nothing more. Before '
    'acting, check that each thing you are about to do was confirmed by the user - not merely proposed, '
    'listed, or summarized by you. If approval of any item is uncertain, it is not approved: ask.')


Q_NOTICE_CODEX = ('This prompt ends with a question mark, so it seems to be a question. Answer it directly, '
    'making only the tool calls needed to get the answer, before and instead of any further work.')
BTW_NOTICE = ('This prompt begins with `BTW ` and is a side request. Answer it first, then resume the '
    'previously active task if it still has unfinished items. Do not treat the side request as replacing '
    'or cancelling that task unless the user explicitly says so.')
PF_NOTICE = ('The user sent a bare "`": your previous reply violated one or more of the problem_finding tells, and they may be '
    'committing one of their own. If aai_coding.problem_finding is not in your context, run doc(aai_coding.problem_finding) first. '
    'Then name which tells you committed, by number (1 anchoring, 2 example fixation, 3 premature commitment, 4 hidden constraint, '
    '5 skipping impasse, 6 tutor drift), and any user tell you see, by letter (A options instead of a situation, B refusing to formulate, '
    "C inherited frame, D asking for the answer at impasse, E adopting the AI's proposal, F choosing from the menu). "
    'Then rewrite the reply without yours.')


def prompt_notices(prompt, q_notice=Q_NOTICE):
    "Notices a submitted prompt earns: question-mark answer-first, read-in-full, bare-approval scope, BTW side-request, and bare-backtick tell call"
    out = []
    if prompt.rstrip().endswith('?'): out.append(q_notice)
    if 'please read' in prompt.lower(): out.append(READ_NOTICE)
    if re.sub(r'^\s+|[\s.!]+$', '', prompt.lower()) in ('go', 'ok'): out.append(APPROVAL_NOTICE)
    if prompt.startswith('BTW '): out.append(BTW_NOTICE)
    if prompt.strip() == '`': out.append(PF_NOTICE)
    return out


def synthetic_resume(path):
    "The last compact boundary's epoch time when the transcript compacted after its last SessionStart delivery (this 'resume' rebuilt a compacted context), else None"
    p = Path(path)
    if not p.is_file(): return None
    b = s = -1
    bt = None
    for i, line in enumerate(p.open()):
        try: r = json.loads(line)
        except json.JSONDecodeError: continue
        if r.get('type') == 'system' and r.get('subtype') == 'compact_boundary': b, bt = i, r.get('timestamp')
        if r.get('type') == 'attachment' and r.get('attachment', {}).get('hookEvent') == 'SessionStart': s = i
    if b > s:  # a boundary without a timestamp reads as "now", disabling the age guard so the reset stays unconditional
        return datetime.fromisoformat(bt.replace('Z', '+00:00')).timestamp() if bt else datetime.now().timestamp()


COMPACT_MSG = '**Post-compaction: your context was rewritten — doc() output is gone and skill texts are stale snapshots — but the kernel process survived untouched: namespace, imports, and current-notebook defaults are all still live, so do not re-run startup or re-import.** Read doc(f) again before using any tooling function whose docs you no longer hold. Re-invoke `persistent-python` now — the live SKILL.md always wins over a replayed snapshot. You will need to redo the dojo. The summary\'s "resume directly / pick up the last task" instruction applies only when it records work actually in flight: if the last user message was already answered and no task is open, do not re-answer or resume anything from before the compact — reply with one short line and wait for the next message.'
SYNTH_MSG = '**Post-compaction resume: the conversation context was rewritten and the kernel restarted with a clean namespace.** Tool documentation and skill text shown in the reconstructed history may be truncated or stale: read doc(f) again before using any tooling function whose docs you no longer hold. Re-invoke `persistent-python` now, and rebuild variables, current-notebook defaults, and monkeypatches on demand. Keep any dojo completion id from your context. The summary\'s "resume directly / pick up the last task" instruction applies only when it records work actually in flight: if the last user message was already answered and no task is open, do not re-answer or resume anything from before the compact — reply with one short line and wait for the next message.'
RESUME_MSG = '**Post-resume: your context is exactly as it was when the app closed — everything you can still see (doc() output, dojo completion id) remains valid — but the kernel restarted with a clean namespace (startup.py re-ran, so its imports are back).** Rebuild other session state on demand (variables, set_dlg, monkeypatches), and pass a dojo completion id from your context to dojo_start(id) before file work.'
BOOTSTRAP_MSG = '**NEVER touch local files or run code before completing the bootstrap. "Touch" means any file read, edit, search, or listing (Read/Edit/Grep/Glob, Bash, `fd`/`rg`), any clikernel `execute`, and any subagent that would do these on your behalf — however small it looks: one quick read counts, one search counts, "just checking one thing" counts. Bootstrap = invoke the `persistent-python` skill, run `from llmdojo.dojo import *; dojo_start()` and complete every task it prints (if a completion id from a clean round is in your context, `dojo_start(id)` replays it instantly). Work that never reaches for the filesystem — pure discussion, web research, browser automation — never hits the trigger and needs no bootstrap. Why: this project runs on a persistent Python workbench with curated pyskills, and unbootstrapped sessions reliably regress to ad-hoc Bash and one-off scripts that cost more to review than the dojo costs to run.** After bootstrapping, map each task to a pyskill from the `list_pyskills()` catalog before reaching for Bash, and read the project `README.md` and `DEV.md` before starting work.'
NBDEV_MSG = '**This is an nbdev project: notebooks in `nbs/` are the source of truth, and the exported `.py` files are autogenerated — never edit them.** Before your FIRST edit to any .ipynb you MUST: read doc(nbdev.skill). If its output is not visible in your current context, you have not read it — "I know nbdev" is the trigger to read it, not to skip it, because it documents where this house\'s style differs from your priors. Editing a notebook without it is the same class of error as editing a generated `.py`. Search notebooks by cell id (not line numbers) with the notebook-aware search pyskill, and never grep the generated `.py`. Edit cells through the hash-verified edit pyskill, never the `.py`.'
BLOCK_EDIT_MSG = 'Native file write/edit tools are blocked in this environment: make the edit via the clikernel session instead (exhash / %%exhash, pyskills.edit, pyskills.ipynb).'


def claude_session_start(o):
    "SessionStart: orientation notice by source, then Python-project bootstrap and nbdev addenda"
    d = Path(os.environ.get('CLAUDE_PROJECT_DIR') or os.getcwd())
    src = o.get('source', '')
    if src in ('resume', 'compact'): print(f'[{src} at {datetime.now():%H:%M:%S}]')
    if src == 'compact':
        print(COMPACT_MSG)
    elif src == 'resume' and synthetic_resume(o.get('transcript_path', '')): print(SYNTH_MSG)
    elif src == 'resume' and (d/'pyproject.toml').is_file(): print(RESUME_MSG)
    if (d/'pyproject.toml').is_file(): print(BOOTSTRAP_MSG)
    try: nb = any(l.startswith('[tool.nbdev]') for l in (d/'pyproject.toml').open())
    except OSError: nb = False
    if nb: print(NBDEV_MSG)


def _prompt_submit(o, q_notice):
    ns = prompt_notices(o.get('prompt') or '', q_notice)
    if ns: print(json.dumps(dict(hookSpecificOutput=dict(
        hookEventName='UserPromptSubmit', additionalContext='\n'.join(ns)))))


def claude_prompt_submit(o):
    "Claude UserPromptSubmit: emit all notices as one hookSpecificOutput JSON object"
    _prompt_submit(o, Q_NOTICE)


def codex_prompt_submit(o):
    "codex UserPromptSubmit: emit all notices as one hookSpecificOutput JSON object"
    _prompt_submit(o, Q_NOTICE_CODEX)


def claude_bash_guard(o):
    "PreToolUse(Bash): reject output-truncating pipes"
    if m := bash_guard_msg(o.get('tool_input', {}).get('command') or ''):
        print(m, file=sys.stderr)
        sys.exit(2)


def claude_block_native_edit(o):
    "PreToolUse(Write|Edit|NotebookEdit): route edits to the kernel tooling"
    print(BLOCK_EDIT_MSG, file=sys.stderr)
    sys.exit(2)


AIR_ROUNDS, AIR_RENUDGE, AIR_SUBSTANCE = 8, 5, 100
AIR_MSG = 'You may have made {0} tool rounds without surfacing. Write real response text that re-points your attention (long runs collapse it onto recent results): restate the request, including one constraint you\'d stopped mentioning; name your most questionable recent tool call (nbdev => nb tooling, pyskills over Bash, exhash for edits, wrapping param in unneeded str() or Path().expanduser, unneeded final print()) and correct it if wrong (do not mention this in your final reply to the user); state the next step. Write any upcoming user-facing text in GOV.UK style. One idea per sentence. No dash asides, no semicolon joins. Re-read any docstrings, docs, or comments you wrote since the last surfacing and fix them to the same standard. If this reads like your last surfacing, you haven\'t reconnected.'


def _state_file(kind, sid):
    "Per-session state file of the given `kind` under the shared state root, sweeping abandoned siblings"
    d = Path(os.environ.get('LLMDOJO_STATE_DIR', Path.home()/'.local/state/llmdojo'))/kind
    d.mkdir(parents=True, exist_ok=True)
    import time
    for g in d.glob('*'):
        try:
            if g.stat().st_mtime < time.time() - 86400: g.unlink(missing_ok=True)
        except FileNotFoundError: pass   # a concurrent sweep got it first
    return d/f'{sid}.json'


def claude_air(o):
    "UserPromptSubmit/MessageDisplay/PostToolBatch: nudge after AIR_ROUNDS tool rounds with no substantive text"
    f = _state_file('air', o.get('session_id', ''))
    try: st = json.loads(f.read_text())
    except (OSError, ValueError): st = {}   # missing, torn by a concurrent writer, or otherwise unreadable: start fresh
    if not isinstance(st, dict): st = {}
    st = {k: st.get(k, d) for k, d in dict(rounds=0, nudged=0, mid='', midlen=0).items()}
    ev = o['hook_event_name']
    if ev == 'UserPromptSubmit': st.update(rounds=0, nudged=0)
    elif ev == 'MessageDisplay':
        if o.get('message_id') != st['mid']: st.update(mid=o.get('message_id'), midlen=0)
        st['midlen'] += len(o.get('delta') or '')
        if o.get('final') and st['midlen'] >= AIR_SUBSTANCE: st.update(rounds=0, nudged=0)
    elif ev == 'PostToolBatch':
        st['rounds'] += 1
        if st['rounds'] >= AIR_ROUNDS and st['rounds'] - st['nudged'] >= AIR_RENUDGE:
            st['nudged'] = st['rounds']
            print(json.dumps(dict(hookSpecificOutput=dict(
                hookEventName='PostToolBatch', additionalContext=AIR_MSG.format(st['rounds'])))))
    tmp = f.with_suffix(f'.{os.getpid()}.tmp')   # concurrent hook processes share this file: atomic replace, never a torn write
    tmp.write_text(json.dumps(st))
    tmp.replace(f)


# Port of podlayer/message-drop-sentinel (MIT). Workaround for a live platform bug: mid-turn
# `thinking -> text -> thinking -> tool_use` drops the text upstream - never rendered, never in the
# transcript, gone from the agent's replayed context - leaving two ADJACENT thinking blocks as a scar.
# Retire when fixed; upstream reports and the re-test recipe are in that repo's README.
DROP_MSG_BATCH = 'Two thinking blocks in a row appeared in this turn: you probably just emitted text that the platform silently ate (it reached neither the user nor the transcript, and will not be in your future context). If the user should see it, say it again in your turn-final message; if the user may need it NOW, say it now and immediately end the turn.'
DROP_MSG_STOP = 'Two thinking blocks in a row appeared in this turn: text you emitted mid-turn may have been silently dropped (it reached neither the user nor the transcript, and will not be in your future context). If your turn-final message already contains everything the user needs, reply with exactly "ok" and nothing else - do not re-summarize. Only if something important appears nowhere in your final message should you state that missing thing now: just the missing part, not a recap.'


def _is_user_prompt(r):
    "A real user prompt record: non-meta, plain text content, not a tool_result carrier"
    if r.get('type') != 'user' or r.get('isMeta'): return False
    c = (r.get('message') or {}).get('content')
    if isinstance(c, str): return True
    return isinstance(c, list) and any(b.get('type') == 'text' for b in c) and not any(b.get('type') == 'tool_result' for b in c)


def count_scars(transcript_path):
    "`(scars, prompt_uuid)` for the current turn: adjacent thinking-block pairs mark where a dropped text used to be"
    recs = []
    for line in Path(transcript_path).open():
        try: recs.append(json.loads(line))
        except ValueError: pass   # blank or malformed line
    start = 0
    for i, r in enumerate(recs):
        if _is_user_prompt(r): start = i
    types = [b.get('type') for r in recs[start:] if r.get('type') == 'assistant' and isinstance((r.get('message') or {}).get('content'), list)
        for b in r['message']['content']]
    scars = sum(1 for a, b in zip(types, types[1:]) if a == b == 'thinking')
    return scars, (recs[start].get('uuid') if recs else None)


def claude_drop_sentinel(o):
    "PostToolBatch/Stop: detect thinking-sandwich message drops via the transcript scar, and prompt a pinned restate"
    try:
        if o.get('agent_id'): return   # a subagent's deliverable is its turn-final message: the shape the bug never touches
        tp = o.get('transcript_path')
        if not tp or not Path(tp).is_file(): return
        scars, uid = count_scars(tp)
        f = _state_file('drop-sentinel', o.get('session_id', ''))
        try: st = json.loads(f.read_text())
        except (OSError, ValueError): st = {}
        done = st.get('reported', 0) if isinstance(st, dict) and st.get('prompt_uuid') == uid else 0
        if scars <= done: return   # whichever boundary reports first claims the holes
        tmp = f.with_suffix(f'.{os.getpid()}.tmp')
        tmp.write_text(json.dumps(dict(prompt_uuid=uid, reported=scars)))
        tmp.replace(f)
        if o['hook_event_name'] == 'PostToolBatch':
            print(json.dumps(dict(hookSpecificOutput=dict(hookEventName='PostToolBatch',
                additionalContext=DROP_MSG_BATCH))))
        else: print(json.dumps(dict(decision='block', reason=DROP_MSG_STOP)))
    except Exception as e: print(f'[drop-sentinel] fail-open: {e!r}', file=sys.stderr)


SLOP_WORST, SLOP_DENSITY, SLOP_WORDS, SLOP_TOP = 10, 10, 40, 8
SLOP_MSG = ("slopometer: your previous turn's final message scored density {d} (flag threshold {t}), worst finding {w}. "
    'The rows below apply to your own prose only: a span that is a quoted example, discussed text, or a title needs no change. '
    'Write your reply to the prompt above in the reference register, avoiding these patterns.\n{rows}')
SLOP_RESTATE = ('The user sent a bare ";": they did not understand your previous reply. Restate it in simple precise English: '
    'short sentences, named actors, plain words, no joins, and define every term you keep.')
SLOP_CAVEAT = ('The user sent a bare "\'": your previous reply appears to contain a caveat in the last or penultimate paragraph, and they cannot tell whether it is '
    'a real critical issue they must fully understand and respond to before proceeding, or an LLM sign-off habit they need not act on. '
    'Say plainly which it is. If real, restate the issue, what hangs on it, and what response it needs; if habit, withdraw it.')


_SLOP_KEYS = dict(mid='', buf='', last='', lastmid='', done='')

def _slop_state(f):
    try: st = json.loads(f.read_text())
    except (OSError, ValueError): st = {}
    if not isinstance(st, dict): st = {}
    return {k: st.get(k, d) for k, d in _SLOP_KEYS.items()}

def _slop_report(txt):
    "Zero or one scored-message notices for `txt`, applying the env-tunable thresholds"
    if len(txt.split()) < int(os.environ.get('SLOP_WORDS', SLOP_WORDS)): return []
    from shutil import which
    if not which('slopometer'): return []
    import subprocess
    r = subprocess.run(['slopometer', '--json'], input=txt, capture_output=True, text=True, timeout=60)
    if r.returncode: return []
    j = json.loads(r.stdout)
    worst_min = int(os.environ.get('SLOP_WORST', SLOP_WORST))
    dens_min = float(os.environ.get('SLOP_DENSITY', SLOP_DENSITY))
    if not (j['worst'] >= worst_min or j['density'] >= dens_min): return []
    def row(f):
        tl = f" (tell {f['tell']})" if f['tell'] is not None else ''
        return f"[{f['weight']}] {f['rule']}{tl}: {f['text']!r}"
    rows = '\n'.join(row(f) for f in j['findings'][:SLOP_TOP])
    return [SLOP_MSG.format(d=j['density'], t=dens_min, w=j['worst'], rows=rows)]


def claude_slop(o):
    "MessageDisplay/UserPromptSubmit: track the displaying message, then report the previous turn's score with the new prompt"
    try:
        if o.get('agent_id'): return
        f = _state_file('slop', o.get('session_id', ''))
        st = _slop_state(f)
        if o['hook_event_name'] == 'MessageDisplay':
            if o.get('message_id') != st['mid']: st.update(mid=o.get('message_id'), buf='')
            st['buf'] += o.get('delta') or ''
            if o.get('final'): st['last'], st['lastmid'] = st['buf'], st['mid']
            tmp = f.with_suffix(f'.{os.getpid()}.tmp')
            tmp.write_text(json.dumps(st))
            tmp.replace(f)
            return
        notes = []
        if (o.get('prompt') or '').strip() == ';': notes.append(SLOP_RESTATE)
        if (o.get('prompt') or '').strip() == "'": notes.append(SLOP_CAVEAT)
        txt, fresh = st['last'], st['lastmid'] != st['done']
        if txt and fresh:
            st['done'] = st['lastmid']
            tmp = f.with_suffix(f'.{os.getpid()}.tmp')
            tmp.write_text(json.dumps(st))
            tmp.replace(f)
            notes += _slop_report(txt)
        if notes: print(json.dumps(dict(hookSpecificOutput=dict(
            hookEventName='UserPromptSubmit', additionalContext='\n'.join(notes)))))
    except Exception as e: print(f'[slop] fail-open: {e!r}', file=sys.stderr)
def codex_orientation(o):
    "codex PostCompact/SessionStart/PreToolUse: one-shot post-compaction reorientation"
    state = Path(os.environ.get('LLMDOJO_STATE_DIR', Path.home()/'.local/state/llmdojo'))
    markers = state/'compact'
    marker = markers/f"{o['session_id']}.json"
    event = o['hook_event_name']
    import llmdojo
    message = ('Context was compacted, so the clikernel documentation is no longer in context. Read the startup documentation in '
        'two separate calls: first `doc(clik,pysk,edsk)`, then `doc(dsk,exh,rgsk)`. Run `doc()` for '
        'anything else you need as you continue. Do not rerun the dojo. After running the two `doc()` calls, retry your last tool '
        'call; it should now work. Then continue your existing task if it is not complete.')
    sample = (Path(llmdojo.__file__).parent/'dojo_data/codexdojo_sample.md').read_text()
    message += ('\n\nThe following is a sample usage session from before compaction. Treat it as reference '
        'for correct tool usage; do not repeat or score it.\n\n') + sample
    if event == 'PostCompact':
        markers.mkdir(parents=True, exist_ok=True)
        marker.write_text(json.dumps(dict(turn_id=o.get('turn_id'))))
    elif event == 'PreToolUse':
        try: marker.unlink()
        except FileNotFoundError: pass
        else: print(json.dumps(dict(hookSpecificOutput=dict(hookEventName='PreToolUse', permissionDecision='deny', permissionDecisionReason=message))))
    elif event == 'SessionStart':
        try: marker.unlink()
        except FileNotFoundError: pass
        else: print(json.dumps(dict(hookSpecificOutput=dict(hookEventName='SessionStart', additionalContext=message))))


def main():
    "Dispatch `aai-hook <subcommand>` to its handler with the stdin JSON payload"
    globals()[sys.argv[1].replace('-', '_')](json.load(sys.stdin))
