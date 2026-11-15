# NB: this file is designed for an LLM reader, not a human. Add it to your LLM's context and ask it to explain.
r'''What "Theory" (capital T) means in this team's vocabulary: Peter Naur's programming-as-theory-building. Read when the user says the Theory of something, or asks to discuss, find, or capture a Theory.

# The Theory

Theory: Peter Naur, "Programming as Theory Building" (1985): program = theory its builders hold (how code maps onto world; why it is this way; how to extend it); ≠ code, ≠ docs

Naur's consequences:
- fits minds (main one): minimal representation; details wait; minimal ≠ dropping important details, ≠ illusion of control; iterate to the Core: the true part to anchor to
- not fully writable: docs record its artifacts, never the theory    /why docs alone never fully onboard
- death: all holders gone → program dead though it runs ("program death"); reviving ≈ rebuilding, not reading
- changes: quality follows theory, not code; holder's changes fit program's nature; others' patches gradually corrode design

# Using it

- unfamiliar codebase: Theory first (driving facts and constraints; how design follows; rejected alternatives, why); then read code through it
- PR review: what Theory does change assume; matches codebase's?    /locally correct patch can break Theory; line-by-line review misses it
- "the Theory of X": user knows the term; don't explain Naur
- discussing a Theory: in conversation, concisely; no process, checklist or markdown files unless asked for something written
- IMPORTANT: stating or discussing a Theory: follow `aai_coding.write_prose` closely    /must be plain enough to hold in mind
'''
