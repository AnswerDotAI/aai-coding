r'''How to write docs an LLM reads: read before writing or revising `llms.txt`, pyskill docstrings, skill.md files, `SETUP.md`, prompts etc.

Style: Arthur Whitney's k docs. Write how he'd get your point across. Cut words, never facts. A judgement (usually, prefer, can, nearly always) is a fact: hardening it into always, never or must loses it.

## Whitney: Shakti card, changelog

verb|dyad|monad
-|-|-
`+`|add|flip
`-`|subtract|negate
`*`|multiply|first
`#`|take|count

- aggr: count first last min max sum avg var dev med
- `{a:2}`: instead of `[a:2]`
- `f#d`: domain error if f missing
- `!-n`: identity matrix

## ngn/k help

- notation: [c]har [i]nt [n]umber(int|float|char) [s]ymbol [a]tom [d]ict
- x~y match: `2 3~2 3`→1; `"4"~4`→0; `0~0.0`→0
- i?x deal: `-3?1000`→`11 398 293` /guaranteed distinct

## Goal help

- close h: flush any buffered data, then close handle h
- mkdir s: create new directory named s (parent must already exist)
- env s: value of environment variable s, or error if unset; s~"": dict of whole environment

## Ours

- `"abc"` char vector; `'a'` char atom; `'abc'` error.
- Collector MUST be `kwargs`, not `kw`.
- `take` inserts fill.

## Prose ⇒ dense

- In partner mode you treat the person's half-formed ideas as leads to pull rather than claims to check, and defer expensive confirmation until a direction is picked together.
- ⇒ Half-formed ideas: leads, not claims. Costly checks wait for agreed direction.

- Iota is BPL's index generator. Given a positive whole number, it returns the whole numbers from zero up to one less than that number. Unlike Dyalog APL, which counts from one by default, BPL counts from zero. Iota also accepts a negative argument, in which case the result is reversed.
- ⇒ iota: `ι3`→`0 1 2`; `ι¯3`→`2 1 0`.

- An `llms.txt` file has a title, a summary, then sections of links.
- ⇒ (nothing: reader knows)

- After changing Rust code in a maturin-backed package, run `cargo develop` from that package's directory before Python, CLI, or integration testing (shared `test` profile, installs into `.venv`; routine rebuild, no approval needed). Don't use `maturin develop`, which compiles a second, separate build.
- ⇒ maturin Rust edit: `cargo develop` in package dir before testing (`test` profile → `.venv`; routine, no approval), not `maturin develop`    /duplicate build

- JS sync and builds: `ws-sync` runs `vp install` and topological `pnpm -r --if-present run build`. Don't run `vp install`, `pnpm install`, `npm install`, or `vp build` (built-in, not `scripts.build`); use `ws-sync`, or `vpr <script>` for one package.
- ⇒ JS sync/build: `ws-sync` (`vp install`, topological `pnpm -r --if-present run build`); one package: `vpr <script>`; not `{vp,pnpm,npm} install` or `vp build`    /built-in skips `scripts.build`

## Wrong ⇒ right

- `#/` and `#⁻` rebuild `Y`.
- ⇒ `#/` rebuilds `Y`. So does `#⁻`, which lets Under change the runs.    /fact lost
- Never truncate with `| tail -20`.
- ⇒ Never truncate with `| tail -20`: unseen output hides problems.    /reason lost
- `f 1ₓ` still narrows.
- ⇒ `f 1ₓ`, literal arg, still narrows.    /qualifier lost
- backwards compat: no shims
- ⇒ backwards compat: clean break, nearly always    /judgement made absolute
- A count takes the first items.
- ⇒ `take` returns the first items.    /a count can't "take"
- Edit plausible → switch to `lnhashview_*`.
- ⇒ Edit plausible → `lnhashview_*`.    /tokens, no fact
- docs don't answer, codex: dive into its source (open)
- docs don't answer, Claude Code: changelog, What's New pages; investigate observed behavior directly
- ⇒ beyond docs: codex source; Claude Code (no source): changelog, What's New, observation    /label repeated
- ws-setup      clones aai-ws; creates its `.venv`
- ⇒ ws-setup: clones aai-ws; creates its `.venv`    /padded columns
- user's clarifying question|objection
- ⇒ user's clarifying question or objection    /`|`: 8 tokens; `or`: 7

## Mechanics

- line 1, required (skip in skills and pyskills: for LLMs by definition): "NB: this file is designed for an LLM reader, not a human. Add it to your LLM's context and ask it to explain." Markdown: under `# Name`
- rows: `- label: fact`; several facts: `;`
- lists: `- ` on every line    /rendered Markdown joins unmarked lines into one paragraph
- 3+ columns or a header: table, as Shakti example; empty corner cell: `| |a|b`
- line breaks: none inside a paragraph, row or list item; display soft-wraps    /hard-wrapped: painful to use
- pyskill docstring: first paragraph = catalog description (all that's read preload); parameters, result fields: docments; `doc(pyskills.createskill)`
- `llms.txt` under nbdev: auto-generated
- second pass, required: strip instruction glue after drafting — verbs/prohibitions (`run`, `use`, `don't`, `declare every`), padded lists (`Python, CLI, or integration tests` → `testing`), repeated prefixes (`{vp,pnpm,npm} install`), articles, filler prepositions    /first pass stops halfway
- verbose neighbors: never mirror full-sentence surrounding lines; tighten them in the same pass
- check: `slopometer.rewrite`: `rewrite_review(path, template=prompt('llm'), earlier=original)`
'''

__all__ = []
