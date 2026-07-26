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


def prompt_notices(prompt, q_notice=Q_NOTICE):
    "Notices a submitted prompt earns: question-mark answer-first, read-in-full, bare-approval scope, and BTW side-request"
    out = []
    if prompt.rstrip().endswith('?'): out.append(q_notice)
    if 'please read' in prompt.lower(): out.append(READ_NOTICE)
    if re.sub(r'^\s+|[\s.!]+$', '', prompt.lower()) in ('go', 'ok'): out.append(APPROVAL_NOTICE)
    if prompt.startswith('BTW '): out.append(BTW_NOTICE)
    return out


def synthetic_resume(path):
    "True when the transcript compacted after its last SessionStart delivery: this 'resume' rebuilt a compacted context"
    p = Path(path)
    if not p.is_file(): return False
    b = s = -1
    for i, line in enumerate(p.open()):
        try: r = json.loads(line)
        except json.JSONDecodeError: continue
        if r.get('type') == 'system' and r.get('subtype') == 'compact_boundary': b = i
        if r.get('type') == 'attachment' and r.get('attachment', {}).get('hookEvent') == 'SessionStart': s = i
    return b > s


COMPACT_MSG = '**Post-compaction: your context was rewritten — all doc() output is gone and skill texts are stale snapshots — but the kernel process survived untouched: namespace, imports, and current-notebook defaults are all still live, so do not re-run startup or re-import.** The doc-state record has been reset mechanically: doc notes will simply re-fire, so read doc(f) afresh before each tooling function\'s next use. Re-invoke `persistent-python` now — the live SKILL.md always wins over a replayed snapshot. You will need to redo the dojo. The summary\'s "resume directly / pick up the last task" instruction applies only when it records work actually in flight: if the last user message was already answered and no task is open, do not re-answer or resume anything from before the compact — reply with one short line and wait for the next message.'
SYNTH_MSG = '**Post-compaction resume: the conversation context was rewritten and the kernel restarted with a clean namespace.** Tool documentation and skill text shown in the reconstructed history may be truncated or stale. The doc-state record has been reset mechanically: doc notes will simply re-fire, so read doc(f) afresh before each tooling function\'s next use. Re-invoke `persistent-python` now, and rebuild variables, current-notebook defaults, and monkeypatches on demand. Keep any dojo completion id from your context. The summary\'s "resume directly / pick up the last task" instruction applies only when it records work actually in flight: if the last user message was already answered and no task is open, do not re-answer or resume anything from before the compact — reply with one short line and wait for the next message.'
RESUME_MSG = '**Post-resume: your context is exactly as it was when the app closed — everything you can still see (doc() output, dojo completion id) remains valid — but the kernel restarted with a clean namespace (startup.py re-ran, so its imports are back).** The doc-state record survived on disk, keyed to this conversation: doc notes fire only for functions whose docs you don\'t hold. Rebuild other session state on demand (variables, set_dlg, monkeypatches), and pass a dojo completion id from your context to dojo_start(id) before file work.'
BOOTSTRAP_MSG = '**NEVER touch local files or run code before completing the bootstrap. "Touch" means any file read, edit, search, or listing (Read/Edit/Grep/Glob, Bash, `fd`/`rg`), any clikernel `execute`, and any subagent that would do these on your behalf — however small it looks: one quick read counts, one search counts, "just checking one thing" counts. Bootstrap = invoke the `persistent-python` skill, run `from llmdojo.dojo import *; dojo_start()` and complete every task it prints (if a completion id from a clean round is in your context, `dojo_start(id)` replays it instantly). Work that never reaches for the filesystem — pure discussion, web research, browser automation — never hits the trigger and needs no bootstrap. Why: this project runs on a persistent Python workbench with curated pyskills, and unbootstrapped sessions reliably regress to ad-hoc Bash and one-off scripts that cost more to review than the dojo costs to run.** After bootstrapping, map each task to a pyskill from the `list_pyskills()` catalog before reaching for Bash, and read the project `README.md` and `DEV.md` before starting work.'
NBDEV_MSG = '**This is an nbdev project: notebooks in `nbs/` are the source of truth, and the exported `.py` files are autogenerated — never edit them.** Read `doc(nbdev.skill)` before touching anything. Search notebooks by cell id (not line numbers) with the notebook-aware search pyskill, and never grep the generated `.py`. Edit cells through the hash-verified edit pyskill, never the `.py`.'
BLOCK_EDIT_MSG = 'Native file write/edit tools are blocked in this environment: make the edit via the clikernel session instead (exhash / %%exhash, pyskills.edit, pyskills.ipynb).'


def _forget(session_id):
    "Reset llmdojo doc-state for `session_id`, matching the env contract its Session derives from"
    os.environ.pop('CLAUDE_PROJECT_DIR', None)
    os.environ['CLAUDE_CODE_SESSION_ID'] = session_id
    try:
        from llmdojo.rules import forget_doced
        forget_doced()
    except Exception: pass


def claude_session_start(o):
    "SessionStart: orientation notice by source, then Python-project bootstrap and nbdev addenda"
    d = Path(os.environ.get('CLAUDE_PROJECT_DIR') or os.getcwd())
    src = o.get('source', '')
    if src in ('resume', 'compact'): print(f'[{src} at {datetime.now():%H:%M:%S}]')
    if src == 'compact':
        _forget(o.get('session_id', ''))
        print(COMPACT_MSG)
    elif src == 'resume' and synthetic_resume(o.get('transcript_path', '')):
        _forget(o.get('session_id', ''))
        print(SYNTH_MSG)
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


def codex_orientation(o):
    "codex PostCompact/SessionStart/PreToolUse: post-compaction doc-state reset and one-shot reorientation"
    state = Path(os.environ.get('LLMDOJO_STATE_DIR', Path.home()/'.local/state/llmdojo'))
    doced, markers = state/'doced', state/'compact'
    marker = markers/f"{o['session_id']}.json"
    event = o['hook_event_name']
    import llmdojo
    message = ('Context was compacted, so the clikernel documentation is no longer in context. Read the startup documentation in '
        'two separate calls: first `doc(clik,pysk,edsk)`, then `doc(dsk,exh,rgsk)`. If function documentation is already visible in '
        'the sample below, use `from llmdojo.rules import doced; doced(...)` to declare it instead of rereading it. Run `doc()` for '
        'anything else you need as you continue. Do not rerun the dojo. After running the two `doc()` calls, retry your last tool '
        'call; it should now work. Then continue your existing task if it is not complete.')
    sample = (Path(llmdojo.__file__).parent/'dojo_data/codexdojo_sample.md').read_text()
    message += ('\n\nThe following is a sample usage session from before compaction. Treat it as reference '
        'for correct tool usage; do not repeat or score it.\n\n') + sample
    if event == 'PostCompact':
        doced.mkdir(parents=True, exist_ok=True)
        for p in doced.glob('*.json'):
            if p.stem.isdigit(): p.write_text('[]')
        (doced/f"{o['session_id']}.json").write_text('[]')
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
