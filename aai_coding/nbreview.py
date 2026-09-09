r'''Review and improve nbdev notebooks using chkstyle findings. Read before a notebook style review. Start with `chkstyle --fix path/to/notebook.ipynb` on notebooks without substantial intentionally formatted code, such as aligned matrices or tables; inspect the notebook and existing changes before applying it.

# Notebook style review

Read `nbdev.skill` and `aai_coding.coding_patterns` before reviewing, and `aai_coding.write_docs` before revising prose. This skill explains how to assess checker findings and choose changes. Those skills own notebook authorship, execution, coding style, and testing policy. Use the notebook tools provided by the host workflow and read their APIs before use.

The goal is a notebook that is easier to understand and maintain, not zero warnings or more coverage. A review can add a lesson, move one, simplify implementation, or remove a test. Keep one coherent change set for the agreed scope. Do not turn every finding into a separate piece of work.

## 1. Establish the scope and apply mechanical fixes

Read the repo instructions and inspect its Git status and existing diff. Identify the source notebooks and the work already in progress. Preserve that work. In a dirty checkout, retain a baseline of the scoped notebooks and generated files in a temporary directory before editing. Review your changes against that baseline as well as the full Git diff; otherwise pre-existing changes can be mistaken for review changes. Read every cell or a summary of every cell, then read the relevant sections in full, including existing examples. Note intentional formatting before running the fixer.

For ordinary code, run `chkstyle --fix path/to/notebook.ipynb` early. Read its diff before making further changes. If layout carries information, such as matrix rows, aligned cases, or a literal protocol example, do not run an unrestricted fixer over it. Source-inspection and formatting notebooks also use signatures, comments, and docstrings as test inputs: changing their layout can change what an example tests. Read `chkstyle -h` for current controls. Protect the relevant statement or block, choose appropriate `--fix-rule` options, or make the edits manually. Do not sacrifice useful formatting to satisfy a warning.

Run `chkstyle --show-rule path/to/notebook.ipynb` to identify remaining findings. Check the notebook, not its generated Python module. Consult the checker's README for unfamiliar rules rather than guessing from a short diagnostic. Review the effective project configuration if a finding seems unexpectedly absent.

An index notebook without exported implementation is not a candidate for the implementation-between-lessons issue. Do not include it automatically because its file changed; review it only when its own prose or other style issues are in scope.

Separate mechanical findings from structural ones. Mechanical cleanup includes import placement, excess vertical space, and wrapping expressions. Preserve docments and meaningful comments. Structural findings require reading the surrounding narrative and understanding what the code is for.

## 2. Diagnose the notebook structure

Use these findings as questions, not instructions to insert cells blindly:

- `long-implementation-run`: the exported statement score has exceeded 24 since the last markdown/non-exported-code pair. Each `def`, `async def`, and `class` scores 3. Other statements score 1. A function with one simple body statement scores 1 total, including tiny properties and methods, regardless of line wrapping. The score includes nested function and class bodies but excludes imports, docstrings, and directives. It spans cell boundaries and resets only after a complete pair. An intervening exported statement breaks the pair. The checker reports once per run, at the cell that crosses the threshold. Read the whole passage, including later cells before the next lesson. Does the reader have too much implementation to absorb? A small helper does not need its own lesson, and merging it into a larger cell does not improve the score. This rule replaces `undocumented-export` and `exported-run`.
- `long-exported-cell` or `too-many-defs`: does this cell contain several ideas, a class that should be developed with patches, or a useful abstraction hidden inside a large function? Split by concept, not line count. A few closely related helpers can remain together with one lesson.
- `long-example-cell`: is it several lessons, excessive setup, a dense test suite, or a useful example that is naturally longer? Split only when each part has something worth explaining. Consider whether the check belongs outside the notebook or should be removed.
- `example-run`: does the reader get a chance to understand each idea before the next? Add or relocate explanations where they teach something. Empty transitions between cells are not a fix.
- `comment-in-example`: does the comment introduce a new idea that deserves markdown and a separate example? Retain comments that state a constraint the code cannot show. Do not turn every inline comment into a paragraph.
- `mixed-imports` or `exported-import-nonexport`: put imports in the appropriate dedicated import cell. A library dependency and a lesson-only dependency have different homes. Before moving or removing an import, check known downstream imports and re-exports in Python and notebook sources. Notebook-local usage cannot identify a compatibility import. Follow `nbdev.skill` for execution implications.

Check whether a good lesson already exists elsewhere. Move or adapt it when possible. Moving implementation beside an existing integration lesson can be better than inserting a local demonstration. Follow dependencies in either direction: a lesson cannot use a class that is defined later, and an enabled cell cannot depend on disabled setup. Authenticated usage may belong later, after the client and credentials have been introduced.

Judge readability independently of the finding. A coherent operation can exceed the score threshold without needing an extraction or an intervening lesson. Separate helper cells can make a large implementation easier to read. Do not merge them merely to reduce cell counts. A valid markdown/code pair can still be unrelated to the preceding implementation; read what it teaches rather than accepting the checker result.

## 3. Improve implementation before explaining around it

A long class often mixes construction, independent operations, and policy decisions. Keep its small shared setup together. Move methods with their own explanations into `@patch` cells where the notebook can develop them one at a time. Keep methods together when separating them would obscure their shared contract. Do not make one cell per method as a quota.

When moving a method, preserve its signature, docments, decorators, async behavior, and public behavior. Add the receiver annotation required by `@patch`. Check decorator order and any delegated signature. A method moved out of a class cannot retain zero-argument `super()` unchanged: preserve the original dispatch, for example with `super(TheClass, self)`. Check other class-scope assumptions too.

Extract a helper when it names a coherent decision or transformation that can be understood independently. A retry loop can separate deciding whether to stop, refresh, or wait from performing requests and sleeping. That decision can then have a short lesson using real input values. Avoid extracting the whole loop body if doing so introduces awkward sentinels, mutable state shuttling, or an elaborate result type. Shorter code is not necessarily clearer code.

Do not add a helper that merely hides mock setup or moves a long block out of sight. Do not invent public APIs to satisfy the checker. Keep style refactors behavior-preserving, but fix clear, local bugs encountered during review. Being pre-existing is not a reason to leave a bug unfixed. Check the existing contract and callers before treating a failed new assertion as a bug. The assertion might impose a new requirement instead of exposing a defect. Validate the correction in proportion to its risk and report it separately from presentation changes. Ask before a broader redesign or a change whose intended behavior is unclear.

## 4. Decide whether a lesson earns its place

Ask what a reader will learn. Good candidates include an external data format, a non-obvious distinction, an ordering guarantee, a failure boundary, or a useful public calling pattern. A rate-limit error and a permission error sharing status 403 teach a distinction. An HTTP date converted to a delay teaches an input format. A demonstration that a constructor stores a value usually teaches little.

Look for a shared lesson before assessing each function in isolation:

1. Identify the operation the reader wants to understand, such as starting a container and waiting for it to run.
2. Follow the objects through nearby functions. One function's result may supply the real input another needs. If an isolated example seems to need a fake or elaborate setup, check whether the preceding implementation already provides that setup as part of the operation.
3. Place those implementations before one markdown/example pair. Keep separate implementation cells where they aid reading. The lesson should follow the operation, assert its meaningful result, and clean up any resources it creates. It need not test each function separately.

For example, `_run` creates a real container and `is_running` waits for it. They naturally share a start-and-wait lesson. Neither a separate fake-container example for `is_running` nor a lesson for every startup helper is needed. Introduce `_is_ready` and `make` afterward as the convenience operation that adds port readiness.

An end-to-end notebook elsewhere does not by itself justify omitting a useful local lesson. Check for a concise shared operation before accepting a long implementation passage or adding an exemption. Respect external-service prerequisites and execution authority; do not assume a real example can run here without checking.

Choose among these options:

- Move an existing markdown/example pair after the implementation when the lesson is already good.
- Extend an existing lesson when a small addition explains the new distinction without muddying its purpose.
- Add a concise pair when there is a useful concept not yet demonstrated.
- Keep related helpers under one lesson when they serve the same idea. Do not require a separate direct call to each helper.
- Leave trivial glue without a standalone lesson. Consider a narrow exemption after checking whether the cell structure itself should change.

Introduce the example with the fact it illustrates. Use realistic values, little setup, and existing notebook objects where they help. Explain the constraint or guarantee rather than translating the implementation line by line. End with an informative display when useful. Read that output: an escaped wall of text, a huge object representation, or an unlabelled number can obscure the lesson. Use an appropriate existing representation rather than assertions against its incidental formatting.

Do not create a fake client and patch clocks, sleeps, credentials, and network calls merely to demonstrate orchestration. A pure decision helper, a small real local object, or an authorized read-only integration example can be clearer. External examples need suitable authorization and execution controls; style review is not permission to send messages, change remote data, or exercise credentials.

## 5. Put meaningful tests in lessons

A lesson should generally include at least one assertion of the behavior it teaches, as well as its useful display. Assert the nested value, classification, calculated delay, preserved order, or documented failure. Use the notebook assertion conventions in `nbdev.skill`. Do not assert exact repr strings, incidental field order, or whole generated payloads unless that exact representation is the contract.

Setup cells and purely illustrative displays do not need token assertions. Do not add a trivial test just to give every code cell one. Nor should a single assertion be treated as enough if the lesson's central claim remains unchecked. The test follows the idea, not a cell-count target.

Keep the assertion and display about the same idea. Testing one resource while displaying another can hide an untested claim. In documentation-rendering lessons, check inclusion of the relevant symbol or source documentation rather than pinning incidental prose wording. Do not fragment one concise example into a separate markdown/code pair for every assertion.

For new or corrected behavior, follow the lesson-first red-green workflow in `nbdev.skill`. Adding a meaningful assertion to an existing correct example can pass immediately; do not manufacture an incorrect expectation or alter production code to create a failure. For a behavior-preserving extraction, exercise the extracted decision and retain the existing behavioral checks.

## 6. Keep, move, or remove complex checks

Keep a check as a lesson when readers can understand its setup and learn from its result. Move it to pytest when the check is worth maintaining but its setup or case analysis would distract even as a hidden notebook check. Intricate parsing, arithmetic boundaries, and interactions among meaningful conditions can justify this. Follow `coding_patterns` for pytest design and red-green work.

Moving an existing passing check is not new behavior. Verify it before and after relocation rather than manufacturing a failure. Preserve its meaningful guarantees and ensure temporary files, imported example modules, and process-wide state are cleaned up on failure too.

Pytest is not the destination for every awkward notebook test. Recording fakes and assertions about which internal method called which other method usually pin down orchestration, not behavior. Extract and test the meaningful logic if it exists. Otherwise remove coverage that only checks delegation, re-exports, trivial storage, Python behavior, or a transcript of the implementation. Do not replace a removed test with a different trivial test to keep the count steady.

Before deleting a check, identify what it actually protects. Preserve a meaningful guarantee in an existing lesson or a justified pytest when needed. A repeated assertion, an exact-repr snapshot, or scaffolding with no independent behavioral claim may deserve removal with no replacement. Report material removals and their rationale.

## 7. Use exemptions deliberately

An exemption is appropriate for a genuine mismatch between the rule and the best presentation. It is not the first answer to a long class, missing explanation, or mock-heavy example. Revisit the structure first. A method may need to become a patch or a decision may need to become a helper before a useful lesson is apparent.

Distinguish trivial glue from substantive operations whose safe demonstration requires distracting setup. Installing or deleting user configuration can justify the latter. State that reason rather than calling the operation trivial. Keep a coherent, safely isolated example intact when splitting it would obscure its cleanup or central idea.

Read `chkstyle -h` to learn how to skip clearly wanted code or formatting. Once a flagged construct is clearly intentional, use the narrowest applicable skip rather than rewriting it or leaving recurring warning noise. A line-level `# chkstyle: ignore` differs from `ignore-node`, a disabled block, and a whole-cell skip. A whole-cell skip also suppresses unrelated findings. If an inline pragma would alter source used as test input, choose a suitable cell-level skip instead. Avoid broad configuration ignores that hide problems elsewhere. Do not use `#| hide` to conceal substantive implementation or a lesson merely to silence narrative checks.

Keep intentional exemptions visible in the review report with their reasons. Do not pad the notebook to eliminate every warning. If the checker itself is wrong, report the concrete false positive rather than silently weakening its rules or expanding the review into a checker rewrite.

## 8. Validate and hand back

Re-read the changed sections in notebook order, including stored outputs and stderr. Check that code, prose, assertions, and displays agree. A rich representation can fail while the cell execution still reports success. Follow dependencies used by display methods as well as explicit calls when moving cells. Confirm that methods retain their signatures and behavior, and no exemption is hiding an unresolved structural issue.

Follow `nbdev.skill` to regenerate exports and outputs and run the changed notebooks. Run relevant pytests if implementation changed or checks moved there. Inspect external operations before executing unfamiliar notebooks; report anything not run. Re-run chkstyle on the notebooks and inspect the final diff, including generated files. Preserve unrelated changes and do not commit, push, or release without authorization.

For notebooks mixing safe local examples with paid, authenticated, or mutating calls, select safe cells and their prerequisites explicitly. Save only outputs from executed cells. Report which sections ran and which outputs were not refreshed; do not describe selected execution as a whole-notebook pass. After parallel dependency exports settle, rerun relevant dependent checks in fresh processes.

Report what became clearer, meaningful tests added or removed, deliberate exemptions, validation results, and unresolved issues. The report should explain judgment, not just count warnings.

If the user requests parallel reviews, assign each agent one explicit repo and notebook scope, including necessary generated exports and relevant pytest moves. Require this skill and its referenced guidance, preserve each repo's existing work, and keep edits within the assigned scope. Coordinate exports when one reviewed repo is a live dependency of another. Agents should return the same review report before further repos or cross-repo changes are authorized.
'''
