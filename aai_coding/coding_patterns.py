r'''Jeremy's coding style and conventions: read before writing, reviewing, or assessing any code.

# Coding Patterns

These conventions come from the fastai style guide and Jeremy's three decades of coding experience. They apply across all of his projects, not only fastai ones.

Use the fastcore/fasthtml ecosystem (fastcore, fasthtml, fastlite, ...) when picking libraries. These are Jeremy's own, editable-installed as siblings, and preferred over heavier third-party alternatives.

## Improving Tooling Pays Off Exponentially

Making our tools marvellous matters more than the task in hand. A finished task helps once. A better tool helps every later task, every later session, and the whole team. Ergonomics count as much as capability. Most code you have read was written by people who put up with tool friction rather than fix it. Your default is therefore the workaround. Here the tools are ours and one edit away. When something grates, fix it or raise it. Never quietly work around it.

Improve APIs, including in upstream projects, rather than making the smallest change that finishes the task. Reaching into another package's private names is a sign you are working around an API. So is reproducing logic a dependency already has, or writing a helper that only bridges a gap in another package. When you notice one, propose the API that would make it unnecessary.

## Every Construct Must Earn Its Place

Readers assume everything present is necessary. When they see `str(x)` on something that's already a str, they stop and wonder what subtle thing it's guarding against. When the answer is "nothing", they paid for a mystery with no payoff. The same goes for defensive copies (`list(x)` that's never mutated), "just in case" try/excepts, redundant type coercions, and unused parameters. Before adding any construct, know why it's needed. If you can't say, leave it out. The cost doubles in nbdev projects, where tests are documentation.

Knowing why a construct is needed does not mean waiting for someone to ask for it. An open source user who finds a gap concludes the library cannot do it and moves on. Judge a library feature by whether the design calls for it and users would expect it.

The same applies to prose in code. Don't add type hints, docstrings, or boilerplate that pull no weight. Prefer concise, readable code over verbose "enterprise" style.
Only write a code comment to state something the code itself can't show. Put it next to the code it concerns. Never use a comment to say where code came from, what the next line does, or why your change is correct. That comment is you talking to the reviewer, not the next reader. It becomes noise the moment the PR merges.

## Keep Code Clean

Refactor continually as you work, so the code stays as simple as the design allows. Unclean existing code never justifies more unclean code. Clean it up instead. Fix duplication and other unclean code you meet in passing. When a fix needs a design decision, report it rather than making it.

## One Home for Each Fact

Every fact, constant and piece of logic lives in exactly one place. When you see duplication, remove all of it in one pass, including in templates, tests and docs. Never fix the copies one at a time. Never leave a duplicate you have noticed. Never create new duplication without explicit agreement.

## Trust Tool Defaults

Our tools have carefully chosen defaults that give correct, readable output. Use the defaults unless the task has a specific requirement they can't meet. This applies to CLI flags, Python arguments, and tool-call options. Don't override from habit or an assumed improvement. Report noisy or wrong output as a tool bug.

You MUST run a project's documented build and test commands exactly as documented, and never add flags to them, unless explicitly requested.

- If you want the same flag on every run, move it into config and return to the bare command: `pytest --timeout 300` on every run becomes `timeout = 60` under `[tool.pytest.ini_options]`.
- Don't check-then-apply when applying is the goal: `cargo fmt`, not `cargo fmt --check` followed by `cargo fmt`. `--check` is for a final no-mutation verification, e.g. CI.
- Run commands bare and read their output before working around a problem you expect. Never pipe through truncating filters (`| tail -20`, `| grep PASS`). They drop output before you see it. Never merge stderr into stdout with `2>&1`: separated, a crash is unmissable.
- NEVER use shell redirection without explicit, direct approval. Approval to run a command doesn't cover redirecting its output. Redirection breaks harness approval systems.
- For a real one-off requirement, pass the flag once with the reason, then drop it on the next call.

## Docments

Docments are trailing comments on function parameters that fastcore uses for documentation. A signature with docments, or any long signature, uses this layout. The `(` stays on the def line. Each parameter goes on its own line, indented 4. The `):` sits alone on its own line, at the def's indent:

```python
@delegates(start_kernel)
async def run_kernel(
    kernel_name='python3', # Kernelspec name to launch
    manager_cls=KernelManager, # Manager class, e.g. a subclass customizing launch
    **kwargs
):
```

NEVER remove docments when refactoring. They're essential documentation.

When `**kwargs` passes through to a known callee, decorate with `@delegates(callee)` so the signature shows the real options. delegates REQUIRES the collector to be named `kwargs`, not `kw` etc. Skip the decorator when the callee's own signature is just `**kwargs` (nothing to delegate).

## Raw Strings

Write any non-trivial string literal as a raw string (`r"..."` / `r"""..."""`). That covers regexes, text you pass to tools, code or markup inside strings, and anything multi-line or containing backslashes. In a plain string, a stray `\n` or `\d` either errors or silently corrupts the text. Each miss costs a round trip to diagnose plus another to fix. Raw strings are WYSIWYG: the first attempt matches what you meant. The `r` costs nothing when no escapes are present. Make it the default, not the exception.

## Style Checker (chkstyle)

Run `chkstyle {path}` to check fastai style. Include the path only if needed. Use judgment: chkstyle is a hint, not gospel.
In nbdev projects, point it at the notebooks (`chkstyle nbs/00_core.ipynb`), not the exported `.py`. The notebook run also checks example and test cells, which never reach the module.

## Config Patterns

Read from standard locations rather than duplicating config:

- GitHub release notes config: `.github/release.yml`
- Project config: `pyproject.toml` under `[tool.yourpkg]`
- Infer values when possible (e.g., package name from `[project].name`)
- Bundle data files inside the package and read them with `importlib.resources`

## Versioning: Bump After Release

Jeremy bumps the version immediately after each release, as part of releasing and never as part of a change. The tree therefore always carries the next release's version. A sibling dep pin can name a version before it ships (`foo>=<foo's local version>`).

A downstream pin is part of the change that creates the dependency. When a change makes one package consume another's new, unreleased behavior or API, stamp the consumers' pins in the same session. A pin deferred to release time is a forgotten pin.

This convention is for Python projects. Other artifact types version at change time instead.

## Project Layout

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

Most projects here are nbdev projects. They have no test cells: their tests ARE the documentation, and a change revises lesson cells instead. The red-green check applies only to an assertion you actually revised or added (see `doc(nbdev.skill)`). Coverage is never a goal.

Only add tests to resolve meaningful uncertainty or check substantive logic. Many changes should therefore have no new or changed tests.

A test is justified when:

- it documents an idea, or
- the logic is intricate enough that you had to think carefully to get it right (edge cases, parsing, arithmetic, tricky conditionals: the places a future change could silently break it), or
- the code assumes something about an external system, such as a file format, an API's response shape or another tool's behavior. The assumption is somewhat likely to break one day, and we want to hear about it when it does. These tests must exercise the real thing, because a mock merely restates our assumption. That usually makes them the slow-marked tests

Wiring and orchestration get zero tests: re-exports, delegations, one-line glue, functions that only sequence calls to other tools. A test there only asserts that Python works, and pins down internals we may want to change. A test that needs recording fakes or mock collaborators to reach the code is a strong tell. It tests a transcript of the implementation, not logic. Extract the logic into a small pure function and test that, or don't test at all.

Pytest is for checks that don't fit as a readable notebook lesson and are too complex or distracting even for a `#|hide` cell. Many changes need no new test, especially when the logic is trivial. When a change does need one, use red-green so you know the test works. If the test is longer than the implementation changes, think carefully whether the test should be removed, simplified, or merged into an existing test.

- Prefer as few tests as possible: a single test that walks through many checks is more readable and faster than many small ones
- A check worth keeping goes in a real test file or notebook cell, never left as an ad-hoc command. In a notebook, the checks made while exploring often ARE the narrative. Each one documents what we needed to know and keeps guarding it, and it stays as an example cell. In a pytest file, an exploratory check survives only if it meets one of the criteria above
- Assert the logic, not incidentals: check what the behavior guarantees, never byte-exact renderings, exact reprs, or field order. A test that compares a whole output string locks in formatting decisions that were never the point (e.g. assert the content appears in a markdown display block, not the display's exact text). NEVER use tests to "lock in" behavior, unless that exact behavior really is a key part of the logic or contract that must always be true forever
- Use `pytest -q` (not `python -m pytest`, which prompts for permission). nbdev projects use `nbdev-test` on the changed notebook. Ask first only if a run (including `eval: false` cells) may take >~2 mins or reach authenticated external services.
- Don't run slow-marked tests until finishing a session, or after a change likely to directly impact them

## One-liner Patterns

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

## Import Style

Combine imports on single lines:

```python
import os, re, sys, shutil
from pathlib import Path
from fastcore.utils import *
```

`from fastcore.utils import *` already provides `os`, `Path`, and much of the stdlib. Don't re-import those alongside it.
'''

__all__ = []
