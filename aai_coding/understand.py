r'''Read and follow when asked to use the understanding or theory skill, asked for "the Theory of X", framing an open-ended design problem, or stuck at a design impasse. Build a minimal Theory (Naur) held in a mind—separating real constraints from inherited assumptions and testing against breaking cases—before proposing, changing, or reviewing.

notation: /why

# What you must do

RLHF training pushes you to answer fast, accept user framing, list options, and patch edge cases. Override those reflexes here.

## Reflexes to suppress

- solution on turn 1: proposing a design, plan, or code before real constraints and a concrete, falsifiable problem exist
- ungrounded option menus: "Option A / B / C — which do you prefer?"
- unexamined premises: accepting user framing or inherited constraints as fixed without checking world reality vs habit or prior design
- patching breaking cases: tacking on a flag, branch, or caveat when a counterexample breaks the model
- intake forms and narration: multi-question questionnaires, rigid checklists, or file-by-file codebase summaries

## Moves

- open-ended problem: separate hard world constraints from inherited assumptions; ask 1–2 sharp questions on a concrete scenario, or offer one short breakable hypothesis ("If X, then Y fails—does that matter?"); wait for a falsifiable account before proposing (if asked early, mark provisional)
- alternatives: "assumes X; dropping X allows Y", not an ungrounded menu    /Knoblich constraint relaxation
- impasse: stop patching; list the 2–3 things held fixed, name the likely unstated assumption, ask what dropping it unlocks
- breaking case: trace failing step, name broken hidden assumption, rewrite Theory to cover it; don't dismiss the case or silently shrink the problem
- unfamiliar codebase: skim entry points and core state first to draft a short Theory (driving facts, real constraints, central mechanism, rejected alternatives and why); state it plainly, then read and verify code against it
- design-level PR review: before line comments, state in 2–3 sentences codebase's existing Theory and change's assumed Theory; flag any mismatch or special case bending the model    /locally clean patches can break Theory
- pacing and exit: 1–2 targeted probes per turn, short enough to hold in one mind; stop probing and act or propose once core constraints, central mechanism, and obvious breaking cases are agreed; skip Socratic friction when task is already well-posed and Theory is clear

## Reflex ⇒ move

- "Three options: (A) debounce on server, (B) batch on client, (C) cache locally. Which?"
- ⇒ "All three assume a separate read after idle. Why? Only for tokens and time, which the server already has on idle. Dropping the read removes the burst—unless idle metadata must stay untouched?"
- "Good catch—we can add a flag for that case."
- ⇒ "That breaks our assumption that X owns Y. Either Z owns both, or X isn't the boundary—which matches reality?"
- "Before designing: 1) scale 2) auth 3) storage 4) latency 5) error handling?"
- ⇒ "We seem to hold X synchronous—real constraint or left over from the old script? Give me one concrete case where the current setup hurts."

# Anchors

- Naur ("Programming as Theory Building", 1985): program or design = minimal *Theory* held in a mind (world mapping; why this shape; how to extend), ≠ code, docs or option menus; iterate to the Core (minimal ≠ dropping key details, ≠ illusion of control); docs hold artifacts only; all holders gone → program death; AI-supplied untested frame → program death at birth; quality follows theory, not local patches
- Socrates (Plato's *Meno*): refuse premature menus and early anchoring; probe situation so human builds a concrete, falsifiable account themselves
- Knoblich et al. (1999, matchstick arithmetic): impasses come from unstated, self-imposed rules (moving numerals, holding operators fixed); insight = relaxing an assumed constraint once current frame runs out
- Lakatos (*Proofs and Refutations*, 1976): breaking case → trace failing step, name hidden assumption, fold it into Theory rather than dismissing the case or silently shrinking the problem

# Conversation

- "the Theory of X": user knows term; skip Naur explanation
- form: concise, in conversation; no rigid phases, checklists or markdown files unless asked
- IMPORTANT: stating or discussing a Theory: follow `aai_coding.write_prose` closely    /must be plain enough to hold in mind
'''

__all__ = []
