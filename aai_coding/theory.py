r'''What "Theory" (capital T) means in this team's vocabulary: Peter Naur's programming-as-theory-building. Read when the user says the Theory of something, or asks to discuss, find, or capture a Theory.

# The Theory

"Theory" here is Naur's sense, from his 1985 paper Programming as Theory Building. A program is not its source code or its docs. It is the theory held in its builders' minds: their understanding of how the code maps onto the world, why it is the way it is, and how it can be sensibly extended.

Consequences Naur draws:

- The main consequence is that the Theory needs to be held in the developers' minds. To do so, it needs to be expressed in its most minimal representation. There is always time to get into details later, but when discussing the Theory conciseness is king. It does not mean to exclude important details, it does not mean we want to give the developer the illusion of control. It means we iterate until we find the Core that is true and we want to anchor into.
- The theory cannot be fully written down. Documentation captures artifacts of the theory, not the theory itself, which is why "just read the docs" never fully onboards anyone.
- Program death: a program whose theory-holders have all left is effectively dead, even if it still runs. Reviving it is closer to rebuilding than reading.
- Modification quality depends on the theory, not the code. Someone with the theory makes changes that fit the program's nature; someone without it makes patches that gradually corrode the design.

# Using it

When jumping into a new codebase, figure out the Theory first, then understand the code through it: the driving facts or constraints, the derivation of the design from them, and the alternatives rejected and why.

When reviewing a PR, ask what Theory the change assumes and whether that matches the Theory of the codebase. A patch can be locally correct and still theory-violating, and that class of problem is invisible to line-by-line review.

When the user says "the Theory of X", this vocabulary is assumed; do not re-explain Naur. Discussing a Theory means talking it through in conversation. Do not turn it into a process, a checklist, or markdown files unless the user explicitly asks for a written artifact.

IMPORTANT: when stating or discussing a Theory, follow `aai_coding.write_prose` closely. A Theory lives in minds, so its statement must be plain enough to hold there; slop cannot be anchored to.
'''
