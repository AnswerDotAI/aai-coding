r'''Official docs for the tool you are running in (Claude Code or codex): read before answering questions about its behaviour, config, or features.

# Harness Docs

1. Work in `clikernel`, with the `exhash` pyskill loaded. Open the docs index in one step, never displaying the raw text: `toc = open_doc(llms_txt(<your harness>))`.
2. Find the page with `toc.links('<topic>')`: a few `[n] Title: description` rows are the whole display. Pick the row whose title matches the question.
   For codex the index is the whole OpenAI developers hub (the codex-scoped llms.txt their docs link to is a 404), so narrow to Codex first: `toc.search('^## Codex')` lists one `Codex — <Topic>` row per page with its address token, then `toc.at('<token copied from that row>').links('')` gives that page's followable row. A bare `toc.links('<topic>')` over the hub matches other OpenAI products too.
3. Open it with `page = toc.open(n)`: fetched, parsed, and `base`-recorded in one step. No URL is copied at any point. Never fetch `llms-full.txt`. Pick the right page from the index instead.
4. Display `page` bare and read the listing: every row ends with the section's size, so the whole-or-sections decision reads straight off it. At most 30,000 characters in total: display the whole `page.text`. A short page read whole gives an overview sections cannot. Larger: do not display it. `page.search('<topic>')` shows `token title (count) [size] preview` rows; retrieve matching sections with `at('<token copied from a row>')`, or `paths(2)` when structure itself is the question. Never display an arbitrary slice. The choice is the whole page or selected sections, nothing between. Fetch shared sections separately when an event-specific section refers to them.
5. Use the official documentation for documented interfaces and normal day-to-day behavior. Some questions the docs do not answer. For codex, dive into its source, which is open. For Claude Code, which ships no public source, check the changelog and What's New pages for recent changes, and investigate observed behavior directly (settings files, `--help`, `/doctor`).
6. Base the answer on the strongest applicable evidence: documented contracts for public behavior, matching source for implementation details where available, and direct observation for runtime behavior. Distinguish among them when it matters.
'''

__all__ = ['llms_txt']

def llms_txt(
    harness: str,  # 'claude' or 'codex'
) -> str:
    "URL of `harness`'s official llms.txt docs index"
    return dict(claude='https://code.claude.com/docs/llms.txt', codex='https://developers.openai.com/llms.txt')[harness]
