"""The `claudesub` command: run a headless Claude child from the current session's compacted history, in its own kernel. It needs llmsurgery and fastclaude, which aai-coding doesn't install."""
from fastcore.script import call_parse

PROTOCOL = """You are a subagent spawned by another Claude Code session with `claudesub`. The history above is that session's compacted transcript: you hold its decisions and evidence, but none of its kernel state. Your clikernel kernel is your own; no other session shares it. No person is watching, so never wait for an answer or ask a question mid-task: if you are blocked, stop and report exactly what you need, and the parent can resume you with `claudesub -r <your session id> '<answer>'`, which restarts your kernel, so finish whatever does not depend on the answer before you stop. Do the directive, and end with a report the parent can act on without reading your transcript: what you did, what you found, and anything left undone."""

@call_parse(nested=True, pos=['directive'])
def main(
    directive:str, # The child's task
    Resume:str=None, # A child session id to continue with `directive` as its next prompt, instead of spawning from this session
    sid:bool=False, # Print the prepared child session id instead of launching
    Quiet:bool=False, # Print only the child's final report, not its progress text
    cwd:str=None, # Project directory to work from, for the parent lookup, the child session, and the child itself; the current directory if None
):
    "Start or resume a headless Claude child and print its progress and result."
    import json, os, subprocess, sys
    from fastclaude.core import claude_env
    from fastclaude.session import save_sess
    from llmsurgery.ant import prepare_compaction
    from llmsurgery.sess import launch_args
    if cwd: os.chdir(cwd)
    s = Resume
    if not s:
        parent = os.environ.get('CLAUDE_CODE_SESSION_ID')
        if not parent: sys.exit('CLAUDE_CODE_SESSION_ID is unset: claudesub runs from inside a Claude Code session')
        s = save_sess(list(prepare_compaction(parent).records), ts=True)
    if sid: return print(s)
    argv = ['claude', '-p', directive, f'--resume={s}', '--output-format=stream-json', '--verbose',
        '--append-system-prompt', PROTOCOL, *launch_args('claude'), *sys.argv[1:]]
    p = subprocess.Popen(argv, stdout=subprocess.PIPE, text=True, env=claude_env())
    res = None
    for line in p.stdout:
        try: e = json.loads(line)
        except json.JSONDecodeError: continue
        if e.get('type') == 'result': res = e
        elif e.get('type') == 'assistant' and not Quiet:
            for b in e['message'].get('content', []):
                if b.get('type') == 'text' and b['text'].strip(): print(b['text'].strip(), flush=True)
    p.wait()
    if res is None: sys.exit(f'claude exited {p.returncode} without a result')
    if Quiet: print(res.get('result', ''))
    print(f"[claudesub {res['subtype']}] session {res['session_id']}, {res['num_turns']} turns, ${res.get('total_cost_usd', 0):.2f}", flush=True)
    if res['subtype'] != 'success': sys.exit(1)
