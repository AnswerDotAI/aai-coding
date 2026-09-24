"""Hook implementations for the team harness, installed as the `aai-hook` CLI. Each subcommand is registered in a harness's hook config (Claude Code settings.json or codex hooks.json) and reads the hook event's JSON payload from stdin. See SETUP.md for the wiring."""
import json, os, re, sys
from datetime import datetime
from pathlib import Path

__all__ = ['main']

NO_TRUNCATE = 'Output pipe truncates below 20 lines. Drop the pipe or keep >=20: truncation is decided before the output exists, so keep enough to diagnose surprises.'
NO_STDERR_MERGE = 'Do not merge stderr into stdout with 2>&1. Run the command bare: the harness pushes large output to a file by itself, and stderr kept separate makes a crash unmissable.'
_TRUNC = re.compile(r'\|\s*(tail|head)\s+(-n\s*)?-?([1-9]|1[0-9])\b')
_MERGE = re.compile(r'2>\s*&\s*1')


def bash_guard_msg(cmd):
    "The objection `cmd` earns - a sub-20-line head/tail pipe, or a 2>&1 stderr merge - else None"
    if _MERGE.search(cmd): return NO_STDERR_MERGE
    return NO_TRUNCATE if _TRUNC.search(cmd) else None


Q_NOTICE = 'This looks like a question. Claude Code bug: a tool call after answer text hides the answer. End the turn with the answer. Most questions need no tool call.'
READ_NOTICE = 'This prompt appears to contain a request to read something. If it could reasonably be interpreted that way, read the target in full NOW, before composing any response: a notebook via summary_dlg then view_dlg/find_msgs as needed; a .py or other text file in full. Never respond from assumed or remembered contents.'
APPROVAL_NOTICE = 'This bare approval covers exactly what was explicitly agreed, nothing more. Before acting, check that each thing you are about to do was confirmed by the user - not merely proposed, listed, or summarized by you. If approval of any item is uncertain, it is not approved: ask.'


Q_NOTICE_CODEX = 'This looks like a question. Answer it directly, before and instead of any further work. Most questions need no tool call.'
BTW_NOTICE = 'This prompt begins with `BTW ` and is a side request. Answer it first, then resume the previously active task if it still has unfinished items. Do not treat the side request as replacing or cancelling that task unless the user explicitly says so.'
SLOP_CAVEAT = 'The user sent a bare "\'": your previous reply appears to end with an unnecessary caveat. Identify what you meant: a concrete obstacle requiring a user decision, an ordinary implementation or testing task, or an unsupported hypothetical concern. If it requires a decision, explain the obstacle, its consequence, and the decision needed. If it is routine work, say so without implying the plan’s feasibility is uncertain. If it is unsupported or irrelevant to the question, withdraw it. Do not invent a justification for having included it.'
CONTINUE_NOTICE = 'The user pressed ".", which means they want you to continue with your existing tasks.'
SLOP_RESTATE = 'The user sent a bare ";": they did not understand your previous reply, possibly because it has AI slop characteristics, or it\'s too long. Restate it in simple precise English: short sentences, named actors, plain words, no joins, and define every term. Use code snippets, symbol and route names, etc instead of prosaic descriptions or invented terms. Remove anything from your response which isn\'t strictly necessary to know, or could be obviously implied or expected.'
NEEDS_LIST_NOTICE = 'The user pressed ",", which means the last response was long and did not appear to explicitly call out at the end of the response an explicit concise list of anything the user needs to know or respond to. Either respond "there is nothing you need to know or respond to", or else respond with a concise complete list of those things now.'


def prompt_notices(prompt, q_notice=Q_NOTICE):
    "Notices for questions, reading requests, bare approvals, BTW side-requests, and the bare `'`, `.`, `;` and `,` shortcuts"
    out = []
    if prompt.rstrip().endswith('?'): out.append(q_notice)
    if 'please read' in prompt.lower(): out.append(READ_NOTICE)
    if re.sub(r'^\s+|[\s.!]+$', '', prompt.lower()) in ('go', 'ok'): out.append(APPROVAL_NOTICE)
    if prompt.startswith('BTW '): out.append(BTW_NOTICE)
    if prompt.strip() == "'": out.append(SLOP_CAVEAT)
    if prompt.strip() == '.': out.append(CONTINUE_NOTICE)
    if prompt.strip() == ';': out.append(SLOP_RESTATE)
    if prompt.strip() == ',': out.append(NEEDS_LIST_NOTICE)
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


COMPACT_MSG = '**Post-compaction: your context was rewritten — doc() output is gone and skill texts are stale snapshots — but the kernel process survived untouched: namespace, imports, and current-notebook defaults are all still live, so do not re-run startup or re-import.** Read doc(f) again before using any tooling function whose docs you no longer hold. Re-invoke `persistent-python` now — the live SKILL.md always wins over a replayed snapshot. The summary\'s "resume directly / pick up the last task" instruction applies only when it records work actually in flight: if the last user message was already answered and no task is open, do not re-answer or resume anything from before the compact — reply with one short line and wait for the next message.'
SYNTH_MSG = '**Post-compaction resume: the conversation context was rewritten and the kernel restarted with a clean namespace.** Tool documentation and skill text shown in the reconstructed history may be truncated or stale: read doc(f) again before using any tooling function whose docs you no longer hold. Re-invoke `persistent-python` now, and rebuild variables, current-notebook defaults, and monkeypatches on demand. The summary\'s "resume directly / pick up the last task" instruction applies only when it records work actually in flight: if the last user message was already answered and no task is open, do not re-answer or resume anything from before the compact — reply with one short line and wait for the next message.'
RESUME_MSG = '**Post-resume: your context is exactly as it was when the app closed — everything you can still see (doc() output) remains valid — but the kernel restarted with a clean namespace (startup.py re-ran, so its imports are back).** Rebuild other session state on demand (variables, set_dlg, monkeypatches).'
BOOTSTRAP_MSG = '**NEVER touch local files or run code before completing the bootstrap. "Touch" means any file read, edit, search, or listing (Read/Edit/Grep/Glob, Bash, `fd`/`rg`), any clikernel `py`, and any subagent that would do these on your behalf — however small it looks: one quick read counts, one search counts, "just checking one thing" counts. Bootstrap = invoke the `persistent-python` skill and follow its startup steps. Work that never reaches for the filesystem — pure discussion, web research, browser automation — never hits the trigger and needs no bootstrap. Why: this project runs on a persistent Python workbench with curated pyskills, and unbootstrapped sessions reliably regress to ad-hoc Bash and one-off scripts that cost more to review than the bootstrap costs to run.** After bootstrapping, map each task to a pyskill from the `list_pyskills()` catalog before reaching for Bash, and read the project `README.md` and `DEV.md` before starting work.'
NBDEV_MSG = '**This is an nbdev project: notebooks in `nbs/` are the source of truth, and the exported `.py` files are autogenerated. Never edit them.** Before any work on this project, including reading and reviewing, you MUST read doc(nbdev.skill). If its output is not visible in your current context, you have not read it. Read it even if you know nbdev: it documents where this house\'s style differs from your priors. Working here without it is the same class of error as editing a generated `.py`. Search notebooks by cell id (not line numbers) with the notebook-aware search pyskill. Read, search and diff the notebooks, never the generated `.py`. Edit cells through the hash-verified edit pyskill.'
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


SLOP_WORST, SLOP_DENSITY, SLOP_WORDS, SLOP_TOP = 15, 15, 40, 8
SLOP_MSG = "Your previous turn's final message was marked as likely unacceptable and unreadable by slopometer. It scored density {d} (flag threshold {t}), worst finding {w}. If you have not done so yet, read the docs writing pyskill and stick to it rigorously in the future.\n{rows}"


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
    r = subprocess.run(['slopometer', '--json', '--min-words', '0'], input=txt, capture_output=True, text=True, timeout=60)
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
    message = 'Context was compacted, so the clikernel documentation is no longer in context. Read the startup documentation in two separate calls: first `doc(clik,pysk,edsk)`, then `doc(dsk,exh,rgsk)`. Run `doc()` for anything else you need as you continue. After running the two `doc()` calls, retry your last tool call; it should now work. Then continue your existing task if it is not complete.'
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
