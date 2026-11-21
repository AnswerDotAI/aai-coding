r'''Official docs for the tool you are running in (Claude Code or codex): read before answering questions about its behaviour, config, or features.

# Harness Docs

- where: `clikernel`, `exhash` loaded
- index: `toc = open_doc(llms_txt(<harness>))`; never display raw
- find: `toc.links('<topic>')`; pick row by title
- codex: index = whole OpenAI hub (Codex llms.txt: 404); `toc.search('^## Codex')` → row per page; `toc.at(<token>).links('')` → its link    /bare `links` matches other OpenAI products
- open: `page = toc.open(n)`; never `llms-full.txt`
- read: display `page` bare; ≤30k chars: whole `page.text`    /overview sections can't give
- larger: `page.search('<topic>')` → `at(<token>)`; structure question: `paths(2)`; never arbitrary slice
- event section cites shared sections: fetch them too
- beyond docs: codex source; Claude Code (no public source): changelog, What's New, settings files, `--help`, `/doctor`
- evidence: docs for public contract, source for implementation, observation for runtime; say which when it matters
'''

__all__ = ['llms_txt']

def llms_txt(
    harness: str,  # 'claude' or 'codex'
) -> str:
    "URL of `harness`'s official llms.txt docs index"
    return dict(claude='https://code.claude.com/docs/llms.txt', codex='https://developers.openai.com/llms.txt')[harness]
