r'''How to write reference prose. Read this before writing docstrings, READMEs, API docs, PR descriptions, or commit messages. Use write-prose for messages to users or colleagues.

Every edit MUST improve prose for readers. Tells=symptoms, not lint rules: NEVER patch mechanically; rebuild from reader needs (see Rewriting).

# Writing Reference Prose

Scope: docstrings, comments, READMEs, API/reference docs, changelogs, PRs, commits (GOV.UK/GDS + ASD-STE100; plain, direct, author's voice, lead with what code does). Narrative/messages: `write_prose`; summaries: `write_summary`.

Good:

> `GatewayKernel` ties the three lower layers together. The ready-wait runs once per kernel, in `start`.[1][3] `watch` polls the process and the heartbeat. A process that dies unexpectedly broadcasts the synthesized `dead` status.[1] After three missed heartbeats,[4] the gateway marks the kernel `unresponsive` in its model. It clears the mark when the next echo arrives.
>
> The gateway never kills an unresponsive kernel.[2] A kernel becomes `dead` only when its process exits.[2] `restart` terminates and respawns with fresh ports in a new process. Clients see `restarting`, then `starting` once the new kernel is ready.[5]

Bad:

> This section describes how `GatewayKernel` manages the kernel lifecycle.[12] `GatewayKernel` ties the three lower layers together. Its `start` is the only place the ready-wait runs: once per kernel, ever.[1][3] The core mechanism: `watch`.[13] It isn't just a poller - it's the liveness authority.[14] Furthermore,[7] it polls the process and the heartbeat. A process that dies unexpectedly broadcasts the synthesized `dead` status, which every client receives.[1] Three missed beats[4] mark the kernel `unresponsive` in its model. The distinction is worth being precise about.[13] That marking is observational only - only process exit means dead -[2] and it clears itself on the next echo. So what does `restart` actually do?[15] It terminates and respawns; the kernel gains fresh ports, fresh channels, and a fresh interpreter via the new process,[16][17] so the channel set is rebuilt[1] and clients simply[3] see `restarting` then a fresh welcome-backed ready kernel.[5]

{markers} Unshown: 6, 8-11, 18, 19.

1. {tacked_on} Wrong register.
2. Key rule in aside: hidden in aside/contrast/parenthetical ("observational only" vs "never kills"). Own sentence/rule; state what system never does.
3. Emphasis devices: "ever/simply/just/the only place", bold/italics. Position key fact/sentence first; cut intensifiers.
4. Elegant variation: "heartbeat"->"beats". One name/concept, one meaning/term (ASD-STE100).
5. Flourish over identifier: "welcome-backed ready kernel" vs `starting`. Use real identifiers/states/values.
6. {hedging}
7. {filler}
8. {restatement}
9. Justification rider: fact+benefit ("kind-sorted so collector stays legal"). Say what code does; reasons go in design/narrative docs.
10. {decorative_verbs}
11. {audience}
12. {throat_clearing} README subject=package purpose.
13. {advertising}
14. {not_x_but_y}
15. Rhetorical questions: never in headings/prose (GDS bans FAQs); state fact.
16. {symmetry}
17. {agent_defocusing}
18. {decoration}
19. {false_depth}

slopometer numbers tells as above. {new_tells} Use "you", imperative ("Run the tests"), active voice.

## Banned words

{plain_words}
{banned_words}
{hidden_words}

## Doc types

- Docstrings: line 1=what fn does (usually all); params/returns in docments; guarantees/edges/errors only if callers need; no signature echo.
- Comments: rare; only what code can't show, beside it (`coding_patterns`).
- READMEs: docstring style; p1 (purpose+audience), install, minimal example; no history/sales; README/index/module=purpose+workflows, edges/errors in notebooks/docs; new section only if usage changes.
- API/changelogs: 1 entry/behavior; reasons in design docs.
- PRs/commits: behavior change first, who did what, reviewer needs (`write_summary`).

{formatting}

## Rewriting high-scoring documentation

High slopometer score: re-explain from scratch, never patch words to game score. Aim <4 (<4 != clear/accurate/complete). Reread as reader; never search for tells. Keep clear informality/contractions/humor (slop=strained metaphors/coinages); don't flatten voice or invent persona.

Order:
- Facts: read code+examples; audience/goals; list substantive points (capabilities, responsibilities, I/O, identifiers, defaults, guarantees, exclusions, edges, failures, context); verify against code, flag wrong/uncertain claims.
- Draft: drop old wording/coinages; write from facts in reader order; name actors, introduce before use, state guarantees directly.
- Context: keep problem, relationships, prerequisites, setup, protocol distinctions, usage reasoning; cut sales.
- Coverage: keep every substantive point (dedupe repeats, keep moved facts findable, keep uncertain detail); flag omissions; correct/report false claims.
- Descriptions: nbdev first blockquote renders standalone; keep full scope (don't collapse NDJSON transport, control routing, deferred tool results into "Communicate through stdin/stdout").
- Verify: reread beside examples before scoring; notebooks follow `nbdev.skill` (edit `nbs/`, export, test; leave code unchanged unless asked; rerun stale outputs).
- Rescore: fresh pass after audit; never edit from intermediate scores; report score, words, findings, tests; reconsider if high; don't dismiss as false positives.
- Delegated: give rules+bounded slice; require corrections, omissions, verification, final score; review against original+code (<4 != review).

`check_docs` checks text via separate model; run only if asked.
'''

from ._writing import fill, charter
__doc__ = fill(__doc__)

__all__ = ['check_docs']

_CHARTER = charter('reference-prose', '10 and 17', 'tell 11')


async def check_docs(
    text,  # The prose to review
    audience,  # Who the text is for, e.g. "users of fastcore"; tell 11 is judged against this
    model='sol',  # An `llms.models` short name, or any full 'vendor/model' spec
    effort='medium',  # Reasoning effort where the model supports it: 'low'/'medium'/'high'
):
    "Review `text` against the rules above (this module's docstring) using an agent, returning flagged spans or 'Clean'. Only use if specifically asked to use an agent."
    from .llms import ask
    return await ask(f'# Rules\n\n{__doc__}\n\nAUDIENCE: {audience}\n\n# TEXT UNDER REVIEW\n\n{text}',
        model=model, system=_CHARTER, effort=effort)
