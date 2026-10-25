r'''Review and improve nbdev notebooks using chkstyle findings. Read before a notebook style review. Start with `chkstyle --fix path/to/notebook.ipynb` on notebooks without substantial intentionally formatted code, such as aligned matrices or tables. Inspect the notebook and existing changes before applying it.

Read `nbdev.skill` and `aai_coding.coding_patterns` before reviewing; they own authorship, execution, coding style and testing policy. Read `aai_coding.write_docs` before revising prose. Use the host workflow's notebook tools; read their APIs before use.

Aim for understanding and maintainability, not zero warnings or more coverage. Adding or moving lessons, simplifying implementation and removing tests are all possible. Keep one coherent change set within the agreed scope, not separate work per finding.

## Scope and mechanical fixes

Read repo instructions, Git status and existing diff. Identify source notebooks and preserve work in progress. In dirty checkouts, snapshot scoped notebooks AND generated files in a temporary directory before editing; compare changes with that baseline AND the full Git diff to distinguish pre-existing work. Read every cell or a summary of every cell, then relevant sections in full, including examples. Note intentional formatting before the fixer.

For ordinary code, run `chkstyle --fix path/to/notebook.ipynb` early and read its diff before further changes. Never run an unrestricted fixer over informative layout (matrix rows, aligned cases, literal protocol examples). In source-inspection/formatting notebooks, signatures, comments and docstrings can be test inputs; reformatting can change the test. Read `chkstyle -h`; protect the statement/block, select appropriate `--fix-rule` options or edit manually. Preserve useful formatting, docments and meaningful comments.

Run `chkstyle --show-rule path/to/notebook.ipynb` for remaining findings, on notebooks, not generated Python. Read the checker README for unfamiliar rules; check effective project config for unexpectedly absent findings. Separate mechanical imports/spacing/wrapping from structural findings requiring narrative and purpose. An index without exported implementation is outside implementation-between-lessons review; a changed file alone isn't grounds to include it. Review its prose/other style only when in scope.

## Diagnose findings

Treat findings as questions, never instructions to insert cells blindly:

- `long-implementation-run`: exported-statement score >24 since the last markdown/non-exported-code pair. Each `def`, `async def`, `class` scores 3; other statements 1. A function with one simple body statement scores 1 TOTAL, including tiny properties/methods, regardless of wrapping. Score includes nested function/class bodies; excludes imports, docstrings and directives. Score spans cells, resets only after a complete pair; an intervening exported statement breaks the pair. Checker reports once per run, at the cell crossing the threshold. Replaces `undocumented-export` and `exported-run`. Read the entire passage through later cells before the next lesson; assess how much implementation the reader must absorb. Small helpers need no separate lesson; merging into a larger cell doesn't improve the score.
- `long-exported-cell` / `too-many-defs`: several ideas, a class to develop with patches, or an abstraction hidden in a large function? Split by concept, not lines. Related helpers can share a lesson.
- `long-example-cell`: several lessons, excessive setup, dense tests, or a naturally long useful example? Split only when each part teaches something; consider moving the check outside the notebook or removing it.
- `example-run`: can the reader understand each idea before the next? Add/relocate explanations where they teach; empty transitions don't fix it.
- `comment-in-example`: a new idea may merit markdown and a separate example. Keep comments saying what code cannot show; don't expand every inline comment into a paragraph.
- `mixed-imports` / `exported-import-nonexport`: use dedicated import cells, distinguishing library and lesson-only dependencies. Before moving/removing imports, check known downstream imports/re-exports in Python AND notebooks; local usage cannot identify compatibility imports. Follow `nbdev.skill` for execution implications.

Judge readability independently of scores. A coherent operation may exceed the threshold without extraction or an intervening lesson. Keep separate helper cells when clearer; don't merge to reduce cell counts. Even a valid markdown/code pair may teach nothing about preceding implementation: read it before accepting the checker result.

## Improve implementation

Long classes can mix construction, independent operations and policy. Keep small shared setup together; develop independently explained methods in `@patch` cells. Keep dependent methods together when splitting hides their relationship; no cell-per-method quota.

Method moves must preserve signatures, docments, decorators, async and public behavior. Add the `@patch` receiver annotation; check decorator order, delegated signatures and class-scope assumptions. Zero-argument `super()` cannot survive the move unchanged; preserve dispatch, e.g. `super(TheClass, self)`.

Extract a helper when it names a coherent decision or transformation that a reader can understand on its own. A retry loop can separate stop/refresh/wait decisions from requests/sleeping; the decision can have a short lesson using real inputs. Avoid extracting the whole body when it introduces awkward sentinels, mutable state shuttling or elaborate result types. Shorter isn't necessarily clearer. No helpers merely hiding mock setup/long blocks; no public APIs invented for the checker.

Style refactors preserve behavior, but fix clear local bugs even if pre-existing. Check existing behavior AND callers before treating a failed new assertion as a bug rather than a new requirement. Validate proportionately to risk; report corrections separately from presentation changes. Ask before broader redesigns or changes whose intended behavior is unclear.

## Choose lessons

Good lesson candidates include external data formats, non-obvious distinctions, ordering guarantees, failure boundaries and useful public calling patterns. Rate-limit and permission errors sharing 403 teach a distinction; HTTP date-to-delay conversion teaches a format. A constructor storing a value usually teaches little.

Look for existing/shared lessons before treating functions separately. Identify the reader's operation (e.g. start a container and wait). Follow objects through nearby functions: one result may supply another's real input. If an isolated example needs fakes/elaborate setup, check whether preceding implementation provides it. Move/adapt a good existing lesson when possible; moving implementation beside an integration lesson can beat a local demonstration. Put the implementations before one markdown/example pair; keep separate implementation cells when clearer. The lesson should follow the operation, assert its meaningful result and clean up resources it creates; no separate call/test per helper is required.

`_run` creates a real container; `is_running` waits for it. They naturally share a start-and-wait lesson; neither a separate fake-container demonstration nor a lesson per startup helper is needed. Introduce `_is_ready` and `make` afterward as the convenience operation adding port readiness.

Respect dependencies in both directions: no lessons using later-defined classes or enabled cells depending on disabled setup. Authenticated usage may belong after introducing client/credentials. An end-to-end notebook elsewhere alone doesn't justify omitting a useful local lesson. Seek a concise shared operation before accepting long implementation passages or exemptions.

Options: move an existing good pair after implementation; extend a lesson for a small distinction without muddying its purpose; add a concise pair for an undemonstrated useful concept; group helpers serving one idea; leave trivial glue without a standalone lesson; consider narrow exemptions after checking cell structure.

Introduce the fact illustrated; use realistic values, minimal setup and existing objects where helpful. Explain constraints/guarantees, not code line by line. End with an informative display when useful and READ it: escaped walls of text, huge reprs and unlabelled numbers obscure lessons. Use an appropriate existing representation, not assertions against incidental formatting.

Don't demonstrate orchestration with fake clients and patched clocks, sleeps, credentials or network calls. A pure decision helper, small real local object or authorized read-only integration may be clearer. Check external-service prerequisites and execution authority before assuming examples can run here; use suitable authorization/execution controls. Style review does NOT authorize messages, remote mutations or exercising credentials.

## Assertions and complex checks

A lesson needs at least one assertion of its taught behavior plus its useful display: nested value, classification, calculated delay, preserved order or documented failure. Follow `nbdev.skill` assertion conventions. Test the central claim, not a count: one assertion can be insufficient; setup/purely illustrative displays need no token assertions. Keep the assertion and display about the same idea. Testing one resource while displaying another can hide an untested claim. Don't split a concise example into a pair per assertion.

Assert exact reprs, incidental field order or whole generated payloads only when callers depend on that exact representation. Documentation-rendering lessons check relevant symbol/source-documentation inclusion, not incidental prose wording.

New/corrected behavior follows `nbdev.skill` lesson-first red-green. Meaningful assertions added to correct examples may pass immediately; never invent wrong expectations or change production code to manufacture failure. For behavior-preserving extraction, exercise the decision and retain behavioral checks. Relocated passing checks need verification before AND after, not manufactured failure; moving isn't new behavior. Preserve guarantees; clean up temporary files, imported example modules and process-wide state on failure too.

Keep understandable, instructive checks as lessons. Use pytest for worthwhile checks whose setup/case analysis distracts even hidden: intricate parsing, arithmetic boundaries or meaningful condition interactions can justify it. Follow `coding_patterns` for pytest design/red-green. Awkwardness alone isn't a reason to move: recording fakes/internal-call assertions usually pin orchestration. Extract/test meaningful logic if present; otherwise remove checks ONLY of delegation, re-exports, trivial storage, Python behavior or implementation transcripts. Don't substitute another trivial check to preserve counts.

Before deletion, identify what the check protects; preserve meaningful guarantees in existing lessons or justified pytests when needed. Repeated assertions, exact-repr snapshots or scaffolding without independent behavioral claims may need no replacement. Report material removals and rationale.

## Exemptions

An exemption is appropriate for a genuine mismatch between the rule and the best presentation. It is not the first answer to a long class, missing explanation, or mock-heavy example. Revisit the structure first. Patching a method/extracting a decision may reveal a lesson. Substantive operations needing distracting safe setup (e.g. installing/deleting user config) aren't trivial glue: state the actual reason. Keep coherent safely isolated examples intact when splitting obscures cleanup or the central idea.

Read `chkstyle -h` for skips. For intentional flagged constructs, use the narrowest applicable skip, not rewrites or recurring noise. Line `# chkstyle: ignore`, `ignore-node`, disabled blocks and whole-cell skips differ; whole-cell also hides unrelated findings. If inline pragmas would change test inputs, choose suitable cell-level skips. Avoid broad configuration ignores that hide problems elsewhere; never use `#| hide` to conceal substantive implementation or lessons to silence narrative checks.

Report exemptions and reasons; don't pad toward zero warnings. Report concrete checker false positives, never silently weaken rules or turn the review into a checker rewrite.

## Validate and report

Reread changed sections in notebook order, including stored outputs/stderr. Check code/prose/assertion/display agreement: rich reprs can fail despite successful execution. When moving cells, follow display-method dependencies AND explicit calls. Confirm method signatures/behavior retained and no exemption hides unresolved structure.

Follow `nbdev.skill` for regenerated exports/outputs and changed-notebook runs. Run relevant pytests if implementation changed or checks moved there. Inspect external operations before unfamiliar notebook execution. Report anything you did not run. Rerun chkstyle; inspect final diff including generated files. Preserve unrelated work; no commit/push/release without authorization.

For mixed safe/paid/authenticated/mutating notebooks, explicitly select safe cells AND prerequisites. Save only executed-cell outputs. Report sections run and unrefreshed outputs; selected execution is NOT a whole-notebook pass. After parallel dependency exports settle, rerun relevant dependent checks in fresh processes.

Report what became clearer, meaningful tests added/removed, deliberate exemptions, validation and unresolved issues. Explain judgments, not just warning counts.

If the user requests parallel reviews, assign each agent one explicit repo/notebook scope including necessary exports/pytest moves. Require this skill and referenced guidance; preserve existing work and stay in scope. Coordinate exports for live dependencies. Agents should return the same review report before further repos/cross-repo changes are authorized.
'''
