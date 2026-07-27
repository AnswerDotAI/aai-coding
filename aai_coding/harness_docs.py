r'''Official docs for the current LLM harness (Claude Code or codex): read before answering questions about harness behavior, config, or features.

# Harness Docs

1. Work in `clikernel`, with the `toolslm.read_md` pyskill loaded. Fetch and parse the docs index in one step, never displaying the raw text: `toc = create_heading_dict(httpx.get(llms_txt(<your harness>)).text)`.
2. Find the page with `toc.links('<topic>')`: a few `[n] Title: description` rows are the whole display. Pick the row whose title matches the question.
3. Fetch it with `page_txt = toc.follow(n)`. No URL is copied at any step. Never fetch `llms-full.txt`. Pick the right page from the index instead.
4. Check `len(page_txt)` in its own cell, and read the result before deciding what to display. At most 30,000 characters: parse it with `create_heading_dict(page_txt, base=<the page url, from the chosen row>)` and display the whole `.text`. A short page read whole gives an overview sections cannot. Larger: do not display it. `search('<topic>')` the parsed page for `addr title (count)` rows and retrieve the matching sections with `at('<addr>')`, or `paths(2)` when structure itself is the question. Never display an arbitrary slice. The choice is the whole page or selected sections, nothing between. Fetch shared sections separately when an event-specific section refers to them.
5. Use the official documentation for documented interfaces and normal day-to-day behavior. When the docs do not answer the question: codex is open source, so dive into its source (prefer source matching the installed build, and say so if it may be newer or older); Claude Code ships no public source, so check the changelog and What's New pages for recent changes, and investigate observed behavior directly (settings files, `--help`, `/doctor`).
6. Base the answer on the strongest applicable evidence: documented contracts for public behavior, matching source for implementation details where available, and direct observation for runtime behavior. Distinguish among them when it matters.
'''

__all__ = ['llms_txt']

def llms_txt(
    harness: str,  # 'claude' or 'codex'
) -> str:
    "URL of `harness`'s official llms.txt docs index"
    return dict(claude='https://code.claude.com/docs/llms.txt', codex='https://learn.chatgpt.com/docs/llms.txt')[harness]
