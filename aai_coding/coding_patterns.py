r'''Jeremy's coding style and conventions: read before writing, reviewing, or assessing any code.

From the fastai style guide and Jeremy's three decades' experience; applies to all his projects. Use his own sibling-editable fastcore/fasthtml ecosystem (`fastcore`, `fasthtml`, `fastlite`, ...), preferred over heavier alternatives.

## Design

Prioritize tool improvement over one task: it helps future tasks, sessions and the team. Ergonomics matter as much as capability. Tool-friction workarounds are the learned default; our tools are one edit away. Fix or raise friction; never quietly work around it.

Improve APIs, including upstream, beyond the smallest task fix. Reaching into another package's private names, reproducing dependency logic, or helpers solely bridging another package's gap signal API workarounds. Propose the API that removes them.

Omit constructs whose need you cannot explain: redundant `str(x)`/coercions, unmutated `list(x)` copies, just-in-case try/excepts, unused parameters. Readers infer necessity; useless constructs cost confusion, doubled in nbdev where tests document code. Omit weightless type hints, docstrings and boilerplate; prefer concise readable code.

Useful features needn't await explicit requests. Open-source users encountering gaps assume incapability and leave. Judge features by design needs and user expectations.

Comments: only what code cannot show, next to that code. Never provenance, next-line narration or change justification: those address reviewers, not future readers.

Refactor continually to keep code as simple as the design allows, including encountered mess; inherited mess never excuses more. Report fixes needing design decisions rather than deciding. Give each fact/constant/logic one home. Remove all noticed duplication together, including templates/tests/docs; never fix copies individually or leave noticed duplicates. New duplication requires explicit agreement.

## Tools

Defaults target correct, readable output. Trust them (CLI flags, Python arguments, tool options) unless a specific task requirement cannot be met. Don't override habitually or for assumed improvements. Report noisy/wrong output as tool bugs.

MUST run documented build/test commands exactly, without added flags unless explicitly requested.

- Flags wanted every run belong in config; return to bare commands: recurring `pytest --timeout 300` becomes `timeout = 60` under `[tool.pytest.ini_options]`.
- Don't check-then-apply when applying is the goal: `cargo fmt`, not `cargo fmt --check` followed by `cargo fmt`. `--check` is for a final no-mutation verification, e.g. CI.
- Run bare; read output before working around expected problems. Never truncate with `| tail -20`/`| grep PASS`, or merge stderr using `2>&1`: unseen output hides problems; separated stderr makes crashes unmissable.
- NEVER shell-redirect without explicit direct approval, separate from command approval; redirection breaks harness approvals.
- Real one-off flag: give the reason, use once, drop next call.

## Python

Docments are fastcore's trailing parameter-comment documentation. NEVER remove them in refactors. Docmented/long signatures: `(` on def line; one parameter per line, four-space indent; `):` alone at def indent:

```python
@delegates(start_kernel)
async def run_kernel(
    kernel_name='python3', # Kernelspec name to launch
    manager_cls=KernelManager, # Manager class, e.g. a subclass customizing launch
    **kwargs
):
```

Known-callee `**kwargs` forwarding requires `@delegates(callee)` to expose options. Collector MUST be `kwargs`, not `kw`. Skip the decorator if callee's signature is only `**kwargs` (nothing to delegate).

Use raw strings for ANY nontrivial string literal (`r"..."`/`r"""..."""`): regexes, tool text, code/markup, multiline, backslashes. Plain `\n`/`\d` can error/silently corrupt text, costing diagnosis and repair round trips; raw strings preserve intended text with no cost when escapes are absent. Make it the default, not the exception.

```python
# Conditionals
if not x: return default
if x and y: do_thing()

# Try/except
try: return run("cmd").strip() or default
except Exception: return default

# Loops
for i in range(n): result[i] = 0
while len(items) < 3: items.append(0)
```

Combine imports:

```python
import os, re, sys, shutil
from pathlib import Path
from fastcore.utils import *
```

`from fastcore.utils import *` already supplies `os`, `Path`, much of the stdlib; don't re-import alongside it.

## Projects

Run `chkstyle {path}`; path only if needed. Hint, not gospel. For nbdev, check notebooks (`chkstyle nbs/00_core.ipynb`), not exported `.py`, to include unexported examples/tests.

Read standard config, don't duplicate: `.github/release.yml` for release notes; `pyproject.toml`'s `[tool.yourpkg]` for project config. Infer values when possible, e.g. package name from `[project].name`. Bundle data inside the package; read using `importlib.resources`.

Python: Jeremy bumps versions immediately AFTER release, as part of releasing, never during changes; tree holds next release version. Sibling floors may name unreleased local versions (`foo>=<foo's local version>`). A downstream pin is part of the change that creates the dependency. Changes consuming new, unreleased dependency behavior/API must update consumers' pins in the SAME SESSION, never defer to release. Other artifacts version at change time.

Prefer flat layout over src/:

```
myproject/
├── mypkg/
│   └── __init__.py
├── tests/
├── pyproject.toml
└── README.md
```

## Testing

Most projects use nbdev: no test cells; tests ARE documentation; revise lesson cells. Use red-green only for assertions actually added/revised (`doc(nbdev.skill)`), to check the test works. Coverage is never a goal. Many changes, especially trivial logic, need no new/changed tests.

Add tests only for meaningful uncertainty or substantive logic. Justifications:
- Documents an idea.
- Logic required careful thought: edge cases, parsing, arithmetic, tricky conditionals vulnerable to silent future breakage.
- Somewhat-likely-to-break external assumption: file format, API response shape, another tool's behavior. Exercise the REAL system; mocks merely restate assumptions. Usually slow-marked.

Zero tests for wiring/orchestration: re-exports, delegation, one-line glue, functions ONLY sequencing tool calls. These assert Python works and constrain changeable internals. Needing recording fakes/mock collaborators to reach code strongly suggests testing implementation transcripts, not logic. Extract/test a small pure function, or don't test.

Pytest: checks that don't fit a readable notebook lesson AND are too complex/distracting even for `#|hide`. When a change needs a new test, use red-green to check the test works. Prefer as few tests as possible, combining checks into readable, faster stories. If a test exceeds implementation changes in length, think carefully about removing, simplifying or merging it.

Keep useful checks in real tests/notebook cells, never ad-hoc commands. Notebook explorations often ARE narrative: retain example cells documenting what we needed to know and guarding it. Pytest explorations survive only under the criteria above.

Assert logic/guarantees, not incidental exact renderings/reprs/field order: check content appears in a Markdown display block, not exact text. NEVER lock in behavior unless that exact behavior is essential logic/contract guaranteed forever.

Run `pytest -q`, not permission-prompting `python -m pytest`; nbdev: `nbdev-test` on changed notebook. Ask first only if runs (including `eval: false` cells) may take >~2min or reach authenticated external services. Slow-marked tests only at session finish or after changes likely to affect them directly.
'''

__all__ = []
