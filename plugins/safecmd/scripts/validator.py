#!/usr/bin/env python3
"""Claude Code PreToolUse hook that auto-approves safe bash commands using safecmd."""
import sys,json,os

def respond(decision, reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": decision,
        "permissionDecisionReason": reason
    }}), flush=True)
    sys.exit(0)

try: from safecmd import validate, DisallowedError
except ImportError: sys.exit(0)   # no opinion: exit 0 with no output falls through to the normal permission flow

def main():
    try: hook_input = json.load(sys.stdin)
    except json.JSONDecodeError as e: respond("deny", f"JSON decode failed: {e}")

    cmd = hook_input.get("tool_input", {}).get("command", "")
    if not cmd: respond("deny", "No command in tool_input")

    try:
        validate(cmd)
        respond("allow", "safecmd: validated")
    except DisallowedError:
        sys.exit(0)   # off-allowlist: no opinion, normal permission flow ("defer" means resume-later and ends the run in the desktop app)

if __name__ == "__main__": main()
