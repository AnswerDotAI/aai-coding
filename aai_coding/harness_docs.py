r'''Official docs for the current LLM harness (Claude Code or codex): read before answering questions about harness behavior, config, or features.

# Harness Docs

1. Work in `clikernel`. Fetch `llms_txt(<your harness>)` exactly with `httpx`, save its text to a variable, and display the whole variable. It is the table of contents agents are meant to inspect.
2. Choose the link whose title matches the question. Do not replace the requested URL with a similar page.
3. Fetch that linked Markdown page with `httpx` and save its text to another variable. Never fetch `llms-full.txt`; select the relevant page from `llms.txt` instead.
4. Check the Markdown page's `len()` in its own cell, and read the result before deciding what to display. At most 30,000 characters: display the whole page. Larger: do not display it; load the `toolslm.read_md` pyskill, parse the page variable, inspect `paths()`, and retrieve the relevant sections. Never display an arbitrary slice: the choice is the whole page or selected sections, nothing between. Fetch shared sections separately when an event-specific section refers to them.
5. Use the official documentation for documented interfaces and normal day-to-day behavior. When the docs do not answer the question: codex is open source, so dive into its source (prefer source matching the installed build, and say so if it may be newer or older); Claude Code ships no public source, so check the changelog and What's New pages for recent changes, and investigate observed behavior directly (settings files, `--help`, `/doctor`).
6. Base the answer on the strongest applicable evidence: documented contracts for public behavior, matching source for implementation details where available, and direct observation for runtime behavior. Distinguish among them when it matters.
'''

__all__ = ['llms_txt']

def llms_txt(
    harness: str,  # 'claude' or 'codex'
) -> str:
    "URL of `harness`'s official llms.txt docs index"
    return dict(claude='https://code.claude.com/docs/llms.txt', codex='https://learn.chatgpt.com/docs/llms.txt')[harness]
