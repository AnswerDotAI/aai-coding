# NB: this file is designed for an LLM reader, not a human. Add it to your LLM's context and ask it to explain.
r'''Review and improve nbdev notebooks using chkstyle findings. Read before a notebook style review. Start with `chkstyle --fix path/to/notebook.ipynb` on notebooks without substantial intentionally formatted code, such as aligned matrices or tables. Inspect the notebook and existing changes before applying it.

notation: /why

- read first: `nbdev.skill`, `aai_coding.coding_patterns` (they own authorship, execution, coding style, testing policy); `aai_coding.write_docs` before revising prose; host workflow's notebook tools: use them, reading their APIs first
- aim: understanding, maintainability; not zero warnings or more coverage; adding or moving lessons, simplifying implementation, removing tests: all possible
- one coherent change set within agreed scope, not separate work per finding

## Scope and mechanical fixes

- read repo instructions, Git status, existing diff; identify source notebooks; preserve work in progress and unrelated work throughout
- dirty checkout: snapshot scoped notebooks AND generated files to a temp dir before editing; compare changes with it AND full Git diff    /tells pre-existing work apart
- relevant sections: read in full, examples included; note intentional formatting before the fixer; read fixer's diff before further changes
- informative layout (matrix rows, aligned cases, literal protocol examples), or formatting that's a test input (source-inspection or formatting notebooks: signatures, comments, docstrings): never unrestricted fixer; protect the statement or block, pick `--fix-rule` options (`chkstyle -h`), or edit by hand; keep useful formatting, docments, meaningful comments
- remaining findings: `chkstyle --show-rule path/to/notebook.ipynb`, on notebooks, not generated Python; unfamiliar rule: checker README; finding unexpectedly absent: check effective project config
- separate mechanical (imports, spacing, wrapping) from structural findings needing narrative, purpose
- index without exported implementation: outside implementation-between-lessons review; a changed file alone isn't grounds to include it; its prose or other style: only when in scope

## Diagnose findings

- finding = question, never an instruction to insert cells blindly; judge readability apart from scores
- `long-implementation-run` (scoring: checker README): read the whole passage through later cells to next lesson; judge how much implementation reader must absorb; coherent operation may exceed threshold with no extraction or intervening lesson; small helpers need no lesson of their own; merging cells doesn't change score, and cell counts aren't a goal
- `long-exported-cell`, `too-many-defs`: several ideas? class to develop with patches? abstraction hidden in a large function? split by concept, not lines; related helpers can share a lesson; separate helper cells when clearer
- `long-example-cell`: several lessons, excess setup, dense tests, or naturally long useful example? split only when each part teaches; consider moving the check out of the notebook, or removing it
- `example-run`: can reader grasp each idea before the next? add or relocate explanations where they teach; empty transitions don't fix it
- `comment-in-example`: new idea may merit markdown + separate example; keep comments saying what code can't show; don't turn every inline comment into a paragraph
- `mixed-imports`, `exported-import-nonexport`: dedicated import cells, library vs lesson-only dependencies; before moving or removing imports, check known downstream imports and re-exports in Python AND notebooks; execution implications: `nbdev.skill`    /local usage can't reveal compatibility imports
- valid markdown and code pair may still teach nothing about the implementation before it: read it before accepting checker result

## Improve implementation

- long class: may mix construction, independent operations, policy; small shared setup together; independently explained methods: `@patch` cells; dependent methods together when splitting hides their relationship; no cell-per-method quota
- moving a method: keep signature, docments, decorators, async, public behavior; add `@patch` receiver annotation; check decorator order, delegated signatures, class-scope assumptions; zero-argument `super()` can't move unchanged: keep dispatch, e.g. `super(TheClass, self)`
- extract a helper when it names a coherent decision or transformation a reader understands alone (retry loop: stop, refresh or wait decision apart from requests and sleeping; the decision can get a short lesson with real inputs)
- don't extract: whole body when that brings awkward sentinels, mutable state shuttling, elaborate result types; helpers merely hiding mock setup or long blocks; public APIs invented for the checker    /shorter ≠ clearer
- style refactors preserve behavior, but fix clear local bugs, pre-existing ones too
- new assertion fails: check existing behavior AND callers before calling it a bug, not a new requirement
- validate in proportion to risk; broader redesign or unclear intended behavior: ask first

## Choose lessons

- good candidates: external data formats, non-obvious distinctions, ordering guarantees, failure boundaries, useful public calling patterns (rate-limit vs permission errors, both 403: a distinction; HTTP date → delay: a format); constructor storing a value: usually teaches little
- find the reader's operation (e.g. start a container, wait for it) and existing and shared lessons before treating functions separately; one lesson follows the operation, asserts its meaningful result, cleans up resources it creates; no call or test per helper needed; implementations before that one markdown and example pair
- e.g. `_run` creates a real container, `is_running` waits for it: one start-and-wait lesson; fake-container demo, lesson per startup helper: not needed; then `_is_ready`, `make` as convenience operation adding port readiness
- follow objects through nearby functions: one result may supply another's real input; isolated example needs fakes or elaborate setup: check whether preceding implementation provides it
- move or adapt a good existing lesson when possible; moving implementation beside an integration lesson can beat a local demonstration; extend a lesson for a small distinction without muddying its purpose; add a concise pair for an undemonstrated useful concept; trivial glue: no standalone lesson needed
- dependencies, both directions: no lesson using a later-defined class; no enabled cell depending on disabled setup; authenticated usage may belong after client and credentials are introduced
- end-to-end notebook elsewhere alone doesn't justify omitting a useful local lesson
- lesson: introduce the fact illustrated; constraints and guarantees, not code line by line; end with informative display when useful, and READ it    /escaped text walls, huge reprs, unlabelled numbers obscure lessons
- orchestration: no demos with fake clients, patched clocks, sleeps, credentials or network calls; pure decision helper, small real local object, authorized read-only integration may be clearer
- external services: check prerequisites, execution authority before assuming examples can run here; use suitable authorization and execution controls; style review does NOT authorize messages, remote mutations, exercising credentials

## Assertions and complex checks

- lesson: ≥1 assertion of taught behavior + useful display (nested value, classification, calculated delay, preserved order, documented failure); conventions: `nbdev.skill`, `coding_patterns`
- test the central claim, not a count: one assertion can be too few; setup and purely illustrative displays need no token assertions
- assertion and display about the same idea    /testing one resource while displaying another can hide an untested claim
- don't split a concise example into a pair per assertion
- docs-rendering lessons: check relevant symbol and source docs are included, not incidental wording
- new or corrected behavior: `nbdev.skill` lesson-first red-green; meaningful assertions added to correct examples may pass at once; never invent wrong expectations or change production code to manufacture failure
- behavior-preserving extraction: exercise the decision; keep behavioral checks
- relocated passing checks: verify before AND after, no manufactured failure    /moving isn't new behavior
- preserve guarantees; clean up temp files, imported example modules, process-wide state, on failure too
- understandable, instructive checks: keep as lessons; pytest (per `coding_patterns`): checks whose setup or case analysis distracts even hidden; awkwardness alone is no reason to move a check there
- wiring-only checks (delegation, re-exports, trivial storage, Python behavior, implementation transcripts): remove, after extracting and testing any meaningful logic; no substitute trivial check to keep counts
- before deleting: identify what the check protects; keep meaningful guarantees in existing lessons or justified pytests; repeated assertions, exact-repr snapshots, scaffolding with no independent behavioral claim may need no replacement

## Exemptions

- for a genuine mismatch between rule and best presentation; not the first answer to a long class, missing explanation, mock-heavy example, long implementation passage: revisit structure first (concise shared operation; patching a method or extracting a decision may reveal a lesson)
- substantive operation needing distracting safe setup (e.g. installing or deleting user config): not trivial glue; state actual reason
- coherent, safely isolated example: keep intact when splitting obscures cleanup or central idea
- skips (checker README "Opting Out", `chkstyle -h`): narrowest that fits an intentional flagged construct, not rewrites or recurring noise; whole-cell `skip` also hides unrelated findings; inline pragma would change a test input: cell-level skip
- no broad config ignores hiding problems elsewhere; never `#| hide` to conceal substantive implementation or lessons to silence narrative checks
- don't pad toward zero warnings; never silently weaken rules or turn review into a checker rewrite

## Validate and report

- reread changed sections in notebook order, stored outputs and stderr too; code, prose, assertion, display agree?    /rich reprs can fail despite successful execution
- moving cells: follow display-method dependencies AND explicit calls; confirm method signatures and behavior kept; no exemption hides unresolved structure
- regenerated exports and outputs, changed-notebook runs: `nbdev.skill`; relevant pytests if implementation changed or checks moved there
- unfamiliar notebook execution: inspect external operations first
- notebook mixing safe, paid, authenticated or mutating cells: select safe cells AND prerequisites explicitly; save only executed cells' outputs    /selected execution is NOT a whole-notebook pass
- parallel dependency exports settled: rerun relevant dependent checks in fresh processes
- rerun chkstyle; inspect final diff, generated files too; no commit, push or release without authorization
- report: what became clearer; corrections, apart from presentation changes; meaningful tests added or removed, with reasons; exemptions, with reasons; concrete checker false positives; sections run, what wasn't run, unrefreshed outputs; unresolved issues; judgments, not just warning counts
- parallel reviews requested: one explicit repo or notebook scope per agent (needed exports, pytest moves included); each reads this skill + referenced guidance; coordinate exports for live dependencies; each returns this report before further repos or cross-repo changes are authorized
'''
