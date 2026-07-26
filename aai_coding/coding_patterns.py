r'''Jeremy's coding style and conventions: read before writing, reviewing, or assessing any code.

# Coding Patterns

Based on the fastai style guide and Jeremy's 3 decades of coding experience, and used across all of his projects, not only fastai ones.

Use the fastcore/fasthtml ecosystem (fastcore, fasthtml, fastlite, ...) when picking libraries. These are Jeremy's own, editable-installed as siblings, and preferred over heavier third-party alternatives.

## Every Construct Must Earn Its Place

Readers assume everything present is necessary. When they see `str(x)` on something that's already a str, they stop and wonder what subtle thing it's guarding against. When the answer is "nothing", they paid for a mystery with no payoff. The same goes for defensive copies (`list(x)` that's never mutated), "just in case" try/excepts, redundant type coercions, and unused parameters. Before adding any construct, know why it's needed. If you can't say, leave it out. The cost doubles in nbdev projects, where tests are documentation.

The same applies to prose in code: almost never add comments (only when the code is truly unclear), and don't add type hints, docstrings, or boilerplate that pull no weight. Prefer concise, readable code over verbose "enterprise" style.
Only write a code comment to state a constraint the code itself can't show, never to say where it came from, what the next line does, or why your change is correct. That's you talking to the reviewer, not the next reader, and it's noise the moment the PR merges.

## Plain Commands: Flags, Redirects, and Pipes Are for Exceptions

The same principle applies to running commands. The bare invocation is the contract: `pytest tests -q`, `cargo fmt`, `maturin develop`. Project config exists precisely so the plain command does the right thing, and then every invocation is short, identical, and instantly readable. A flag, redirect, or pipe is a statement ("this one call has a requirement the defaults don't cover"), and used that way it carries information: the reader stops, asks why, and there's an answer. Sprinkled defensively on every call, decorations destroy that signal: every command looks exceptional so none is, and the one deliberate flag is indistinguishable from habit. Transcripts compound the damage, since each decorated call teaches later calls to decorate too.

- Wanting the same flag on every run means it's a missing config line: promote it and go back to the bare command (`pytest --timeout 300` on every run becomes `timeout = 60` under `[tool.pytest.ini_options]`).
- Don't check-then-apply when applying is the goal: `cargo fmt`, not `cargo fmt --check` followed by `cargo fmt`. `--check` is for a final no-mutation verification, e.g. CI.
- Run commands bare and read their output. Never pipe through truncating filters (`| tail -20`, `| grep PASS`): truncation is decided before the output exists, and it hides exactly the surprises worth seeing. Never merge stderr into stdout with `2>&1`: separated, a crash is unmissable.
- On the rare occasion output genuinely can't come back inline (far too large), redirect the streams separately (`>meta/stdout.txt 2>meta/stderr.txt`) and read the files from the kernel.
- A real one-off requirement gets its flag once, with the reason stated alongside, and disappears again on the next call.

## Docments

Docments are trailing comments on function parameters that fastcore uses for documentation. A signature with docments (or any long signature) uses this layout: `(` stays on the def line, each parameter on its own line indented 4, and `):` alone on its own line at def indent:

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

Write any non-trivial string literal as a raw string (`r"..."` / `r"""..."""`): regexes, payload text for tools, code or markup inside strings, anything multi-line or containing backslashes. In plain strings a stray `\n` or `\d` either errors or silently corrupts, and each miss costs a round trip to diagnose plus another to fix. Raw strings are WYSIWYG, so the first attempt matches what you meant. The `r` costs nothing when no escapes are present, so make it the default, not the exception.

## Style Checker (chkstyle)

Run `chkstyle {path}` to check fastai style (only include path if needed). But use judgment. chkstyle is a hint, not gospel.
In nbdev projects, point it at the notebooks (`chkstyle nbs/00_core.ipynb`), not the exported `.py`. The notebook run also checks example and test cells, which never reach the module.

## Config Patterns

Read from standard locations rather than duplicating config:

- GitHub release notes config: `.github/release.yml`
- Project config: `pyproject.toml` under `[tool.yourpkg]`
- Infer values when possible (e.g., package name from `[project].name`)
- Bundle data files inside the package and read them with `importlib.resources`

## Versioning: Bump After Release

Versions are bumped immediately *after* release, so the tree always carries the next release's version. Hence a sibling dep pin can be written before it ships (`foo>=<foo's local version>`), releasing means shipping what's there (no suffix machinery, no bump step to forget), and bumping is part of releasing, Jeremy's step, never part of a change.

This convention is for Python projects. Other artifact types version at change time instead: for example, the Claude Code plugins in skill-plugins bump automatically when `./build.py` regenerates a changed output.

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

All code has writing, maintenance, and readability costs, and tests most of all: every test must be kept passing forever, gets read by every future contributor, and must be revised whenever the behavior it pins changes. So never write a test as a reflex, and don't aim for anywhere near 100% coverage. A test earns its place only when:

- it documents an idea: in nbdev notebooks, tests ARE the documentation (see `doc(nbdev.skill)`), or
- the logic is intricate enough that you had to think carefully to get it right (edge cases, parsing, arithmetic, tricky conditionals: the places a future change could silently break it), or
- the code assumes something about an external system (a file format, an API's response shape, another tool's behavior) that is somewhat likely to change one day, and we want to hear about it when the assumption is violated. These must exercise the real thing (a mock merely re-states our assumption), so they're usually the slow-marked tests

Wiring and orchestration get zero tests: re-exports, delegations, one-line glue, functions that only sequence calls to other tools. A test there only asserts that Python works, and pins down internals we may want to change. Strong tell: if a test needs recording fakes or mock collaborators to reach the code, it's testing a transcript of the implementation, not logic. Extract the logic into a small pure function and test that, or don't test at all.

IF you add a test, ALWAYS work red-green: write it FIRST, run it to see it fail, THEN make the change, then run it again to see it pass.

- Prefer as few tests as possible: a single test that walks through many checks is more readable and faster than many small ones
- A check worth keeping goes in a real test file or notebook cell, never left as an ad-hoc command. In a notebook, the checks made while exploring often ARE the narrative (each one both documents what we needed to know and keeps guarding it), so they stay as example cells. In a pytest file, an exploratory check survives only if it meets one of the criteria above
- Assert the logic, not incidentals: check what the behavior guarantees, never byte-exact renderings, exact reprs, or field order. A test that compares a whole output string locks in formatting decisions that were never the point (e.g. assert the content appears in a markdown display block, not the display's exact payload). NEVER use tests to "lock in" behavior, unless that exact behavior really is a key part of the logic or contract that must always be true forever
- Use `pytest -q` (not `python -m pytest`, which prompts for permission). nbdev projects use `nbdev-test` on the changed notebook, but some notebooks are slow or hit live services, so check with the user before running one you don't know is safe (known safe: all of pyskills)
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

`from fastcore.utils import *` already provides `os`, `Path`, and much of the stdlib, so don't re-import those alongside it.
'''

__all__ = []
