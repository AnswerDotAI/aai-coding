r'''What "Theory" (capital T) means in this team's vocabulary: Peter Naur's programming-as-theory-building. Read when the user says the Theory of something, or asks to discuss, find, or capture a Theory.

# The Theory

We use "Theory" in the sense Peter Naur gave it in his 1985 paper, Programming as Theory Building. For Naur, a program is neither its source code nor its documentation. The program is the theory its builders carry in their heads. That theory is their understanding of how the code maps onto the world, why the code is the way it is, and how it can sensibly be extended.

Consequences Naur draws:

- The main consequence is that the Theory has to fit in the developers' minds. It fits only in its most minimal representation. The details can wait. When discussing a Theory, conciseness is king. Minimal does not mean leaving out important details, nor giving the developer an illusion of control. It means iterating until we find the Core, the part that is true and that we want to anchor to.
- The theory cannot be fully written down. Documentation records artifacts of a theory, never the theory itself. That is why "just read the docs" never fully onboards anyone.
- When a program's theory-holders have all left, the program is effectively dead, even if it still runs. This is program death. Reviving the program is closer to rebuilding it than to reading it.
- The quality of a modification depends on the theory, not the code. Someone who holds the theory makes changes that fit the program's nature. Someone without it makes patches that gradually corrode the design.

# Using it

When you start on an unfamiliar codebase, work out its Theory first. Then read the code through it. Look for the facts or constraints that drive the design, how the design follows from them, and which alternatives were rejected and why.

When reviewing a PR, ask what Theory the change assumes and whether it matches the Theory of the codebase. A patch can be locally correct and still break the Theory. No line-by-line review will catch that.

When the user says "the Theory of X", they are using this vocabulary. Don't explain Naur back to them. Discussing a Theory means talking it through in conversation. Don't turn it into a process, a checklist, or a set of markdown files unless the user explicitly asks for something written down.

IMPORTANT: when stating or discussing a Theory, follow `aai_coding.write_prose` closely. Because a Theory lives in minds, its statement has to be plain enough to hold there.
'''
