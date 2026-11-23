r'''Jeremy's coding style and conventions: read before writing, reviewing, or assessing any code.

notation: /why

- applies: all Jeremy's projects; from fastai style guide, his three decades' experience
- libraries: his sibling-editable ecosystem (`fastcore`, `fasthtml`, `fastlite`, ...) over heavier alternatives

## Design

- improving a tool > finishing one task    /helps future tasks, sessions, team
- ergonomics: matter as much as capability
- friction: fix or raise; never quietly work around    /workarounds are the learned default; our tools are one edit away
- APIs, upstream too: improve beyond smallest fix; another package's private names, reproduced dependency logic, helpers only bridging a package's gap: workaround signs; propose the API that removes them
- omit: constructs whose need you can't explain (redundant `str(x)` or other coercions, unmutated `list(x)` copies, just-in-case try/excepts, unused parameters); weightless type hints, docstrings, boilerplate; prefer concise readable code    /readers infer necessity: useless constructs cost confusion, doubled in nbdev where tests document code
- useful features: needn't await request; judge by design needs, user expectations    /open-source users meeting gaps assume incapability, leave
- comments: only what code can't show, next to that code; never provenance, next-line narration, change justification    /those address reviewers, not future readers
- refactor continually, encountered mess too: as simple as design allows; inherited mess never excuses more
- fix needing design decision: report, don't decide
- one home per fact, constant or piece of logic; noticed duplication: remove all of it together, templates, tests and docs too; never fix copies singly; new duplication: explicit agreement only

## Tools

- defaults (CLI flags, Python arguments, tool options): trust unless a task requirement can't otherwise be met; never override habitually or for assumed gains; noisy or wrong output: report as tool bug    /defaults target correct, readable output

## Python

- docments (fastcore trailing parameter comments): NEVER remove in refactors
- docmented or long signature:

```python
@delegates(start_kernel)
async def run_kernel(
    kernel_name='python3', # Kernelspec name to launch
    manager_cls=KernelManager, # Manager class, e.g. a subclass customizing launch
    **kwargs
):
```

- `**kwargs` forwarded to known callee: `@delegates(callee)`, exposing its options; skip if callee's signature is only `**kwargs`; collector MUST be `kwargs`, not `kw`
- raw strings for ANY nontrivial literal: regexes, tool text, code, markup, multiline, backslashes    /plain `\n` `\d` can error or silently corrupt text; raw costs nothing when escapes absent
- one-line bodies:

```python
if not x: return default
try: return run("cmd").strip() or default
except Exception: return default
for i in range(n): result[i] = 0
```

- imports combined: `import os, re, sys, shutil`; `from fastcore.utils import *` supplies `os`, `Path`, much of stdlib: don't re-import them

## Projects

- `chkstyle {path}` (path only if needed): hint, not gospel; nbdev: on notebooks (`chkstyle nbs/00_core.ipynb`), not exported `.py`    /notebooks include unexported examples, tests
- standard config: read, don't duplicate (`.github/release.yml` release notes; `pyproject.toml` `[tool.yourpkg]`); infer values when possible, e.g. package name from `[project].name`
- bundled data: inside package, read via `importlib.resources`
- layout: prefer flat (`myproject/mypkg/`, `tests/`, `pyproject.toml`) over `src/`
- Python versions: Jeremy bumps right AFTER release, as part of it, never during changes    /tree holds next release version
- sibling floors may name unreleased local versions (`foo>=<foo's local version>`)
- new dependency: its downstream pin is part of the change; consuming unreleased dependency behavior or API: update consumers' pins SAME SESSION, never at release
- other artifacts: version at change time
- runtime, toolchain, CI action versions: floating channels (`lts/*`, `stable`), or verify active workspace/latest; older pin (from sibling config or prior too): NEVER without explicit discussion    /stale pins propagate and break builds

## Testing

- MUST read `testing` skill before writing, editing, or requesting any test
- nbdev (most projects): no test cells; tests ARE documentation; revise lesson cells
- MUST NOT add tests for trivial logic or tests longer than the implementation without explicit agreement
- add tests only for meaningful uncertainty or substantive logic, never for coverage: logic needing careful thought (edge cases, parsing, arithmetic, tricky conditionals open to silent breakage); somewhat-likely-to-break external assumption (file format, API response shape, another tool's behavior): exercise REAL system, usually slow-marked    /mocks merely restate assumptions
- wiring and orchestration (re-exports, delegation, one-line glue, functions ONLY sequencing tool calls): zero tests    /they assert Python works, constrain changeable internals
- reaching code needs recording fakes or mock collaborators: strongly suggests testing implementation transcripts, not logic; extract and test a small pure function, or don't test
- red-green: only for assertions actually added or revised, to check the test works (`doc(nbdev.skill)`)
- pytest: checks that fit no readable notebook lesson AND are too complex or distracting even for `#|hide`; as few as possible, combined into readable, faster stories
- one-off checks: verify in `clikernel` and discard; permanent pytest only under criteria above (nbdev: keep exploration cells that double as readable narrative)    /smoke checks belong in the kernel, not test files
- assert logic and guarantees, not incidental renderings, reprs or field order (content in Markdown display block, not exact text); NEVER lock in behavior unless essential logic or contract guaranteed forever
- Rust: no inline `#[cfg(test)]` tests; set `test = false` (and `doctest = false` on libs) on `[lib]`/`[[bin]]`, put Rust tests in `tests/`    /inline tests push testing internals over real external behavior, hide useful APIs instead of making them public, and don't play well with fastws
## CLI harness

- **IMPORTANT**: this section applies to CLI coding harnesses only; inside an interactive dialog, follow the dialog skills instead
- documented build and test commands: MUST run exactly, no added flags unless explicitly requested; read output before working around expected problems
- flag wanted every run: into config, back to bare command (recurring `pytest --timeout 300` → `timeout = 60` under `[tool.pytest.ini_options]`)
- applying is the goal: `cargo fmt`, not `cargo fmt --check` then `cargo fmt`; `--check`: final no-mutation verification, e.g. CI
- never truncate (`| tail -20`, `| grep PASS`) or merge stderr (`2>&1`)    /unseen output hides problems; separate stderr makes crashes unmissable
- shell output redirect (`>`, `>>`): ASK separately (stdin `<`, `<<` fine)    /breaks harness approvals
- real one-off flag: give reason; use once; drop next call
- run: `pytest -q`, not `python -m pytest` (prompts for permission); nbdev: `nbdev-test` on changed notebook
- ask first only if runs (`eval: false` cells too) may take >~2min or reach authenticated external services
- slow-marked tests: only at session finish or after changes likely to affect them directly
'''

__all__ = []
