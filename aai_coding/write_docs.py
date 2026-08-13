r'''How to write reference prose: read before writing docstrings, READMEs, API docs, PR descriptions, commit messages, or messages to co-workers.

# Writing Reference Prose

These rules cover the prose that ships with code: docstrings, code comments, READMEs, API and reference docs, changelogs, PR descriptions, commit messages, and messages to co-workers. The register is GOV.UK/GDS house style with ASD-STE100's discipline: very plain, very direct, no author's voice. Narrative prose has an author on the page. Reference prose has only the contract. For blog posts, essays, and announcements use write-prose. For choosing what a summary says, use write-summary.

Here is a passage from a design doc, written in this register:

> `GatewayKernel` ties the three lower layers together. The ready-wait runs once per kernel, in `start`.[1][3] `watch` polls the process and the heartbeat. A process that dies unexpectedly broadcasts the synthesized `dead` status.[1] Three missed heartbeats[4] mark the kernel `unresponsive` in its model, with the next echo clearing the mark. The gateway never kills an unresponsive kernel.[2] A kernel becomes `dead` only when its process exits.[2] `restart` terminates and respawns with fresh ports in a new process. Clients see `restarting`, then `starting` once the new kernel is ready.[5]

Write like that. Each sentence states one fact and stops. Each guarantee is its own sentence. The negative guarantee is stated too: what the gateway never does. Every status is named by its real identifier. Sentences this uniform would read as monotone in an essay. In reference prose they are correct. Readers scan, take the fact they came for, and leave.

Here is the same passage before editing:

> `GatewayKernel` ties the three lower layers together, and its `start` is the only place the ready-wait runs: once per kernel, ever.[1][3] `watch` polls the process and the heartbeat: a process that dies unexpectedly broadcasts the synthesized `dead` status, and three missed beats[4] mark the kernel `unresponsive` in its model.[1] That marking is observational only - only process exit means dead -[2] and it clears itself on the next echo. `restart` terminates and respawns; the new process gets fresh ports, so the channel set is rebuilt[6] and clients simply[3] see `restarting` then a fresh welcome-backed ready kernel.[5]

Do NOT write like that. Nothing in it is false. In a blog post it might pass. As reference prose it fails. Each sentence carries several facts. The key guarantee is an aside. The final state gets a flourish instead of its name.

The numbers refer to the [bracketed] markers in both passages. Where a number appears in each, the pair is the failing and the working version of the same thing.

1. Splices: clauses joined with em dashes, semicolons, colons, ", and", or ", which". Write one idea per sentence and end it. In narrative prose an occasional join earns its place. Here none does.
2. Contract by aside: the rule the reader most needs, implied by an aside, a contrast, or a parenthetical. "That marking is observational only" implies the guarantee. "The gateway never kills an unresponsive kernel" states it. Give every guarantee its own sentence. State the negative space too. What the system never does is as much of the contract as what it does.
3. Emphasis devices: "ever", "simply", "just", "the only place", bold, italics. Position is the only emphasis mechanism in reference prose. Put the key fact first in its sentence. Put the key sentence first in its paragraph. Delete the intensifiers.
4. Elegant variation: "the heartbeat" becoming "beats" a sentence later. One concept, one name, every time it appears, however repetitive it feels. Never reuse one word for two concepts either. This is STE's "one meaning per term".
5. Flourish over identifier: "a fresh welcome-backed ready kernel" where the real status is `starting`. Name the actual identifier, state, value, or number. The reader will grep for it, test against it, and see it in logs.
6. Consequence glue: a clause joined by ", so". The consequence is usually restatement, internal detail the reader does not need (", so the channel set is rebuilt"), or a link that does not hold. Delete it, or give a real consequence its own sentence.
7. Hedging: "may", "might", "potentially", "in some cases", "should generally". A contract that hedges is not a contract. State what the code does. When behavior is unspecified or untested, say that outright: "behavior with concurrent writers is undefined", "not benchmarked".
8. Noting fillers: "note that", "it's worth noting", "importantly", "keep in mind". If the fact matters, state it plainly and early. Delete the filler every time.
9. Restatement: a heading repeated by its section's first line, a lead sentence summarizing the paragraph it starts, a closing line summarizing the section. State each fact once, in its best position, and stop. Summaries earn their place at document scale only. A README's first paragraph is one.
10. Justification rider: a fact with a benefit clause attached: "kind-sorted so a collector stays legal wherever it came from", "parses bools so flag values test correctly". The rider argues for the fact instead of stating it. Reference prose states the contract. Rationale lives in design docs and narrative prose.
11. Decorative verbs: a verb chosen for texture instead of the plain word for the event: ids "ride" in rows, a note "lands" in the output. Ask whether you would say the verb at a whiteboard. An artifact subject is fine when the artifact really acts ("`watch` polls the process"). Its verb must still be the plain one.
12. Audience misjudged, in either direction: explaining what every reader of the doc already knows ("the README documents the package"), or dropping a local coinage without definition ("the carrier"). Name the audience. Cut what they know. Define your own coinages at first use. Established external terms of art may stay. They can be looked up. A coinage cannot.

Entries 7-12 are tells the passage pair is too short to show. When a new tell is added to this skill, add a marked instance to the before passage where a short sample can show it.

Instructions address the reader as "you", in the imperative: "Run the tests", not "The tests should be run". Prefer active voice everywhere. A passive that hides the actor usually hides part of the contract with it.

## Banned words

Always use the plainest word that is still correct:

- use, not "utilize" or "leverage"
- improve, not "enhance" or "optimize" (unless something is literally being optimized)
- complete, not "comprehensive"
- strong, not "robust"
- help, not "facilitate"

Kill on sight: seamless, streamline, empower, foster, pivotal, "a testament to", realm, landscape (metaphorical), navigate (metaphorical), delve, myriad. For "land"/"landed" say what happened: merged, committed, released, appears. For metaphorical "shape"/"shaped" say structure, format, or the actual event. "Invariant" is usually "rule" or "guarantee". Compounds in "-bearing" (load-bearing, text-bearing) have plainer forms.

## Doc types

- Docstrings: the first line states what the function does. For most functions it is the whole docstring. Parameter detail goes in docments, never repeated in prose. State inputs, outputs, errors raised, and guarantees. Never restate the signature.
- Code comments: only a constraint the code cannot show (see coding-patterns). Almost never.
- READMEs: read like docstrings, not blogs. First paragraph: what the package does and for whom. Then install, then a minimal example. No journey, no sales language.
- API docs and changelogs: the contract or the change, one entry per behavior. Rationale goes in design docs.
- PR descriptions and commit messages: lead with the behavior change, name who did what, and give reviewers what they need to judge the diff. write-summary covers choosing the content.
- Messages to co-workers: the answer first, support after. No softening preamble, no closing offers of further help.

Don't hard-wrap prose. Write each paragraph as one continuous line and let the display soft-wrap it. Put code symbols in backticks: function names, parameters, file paths, module and package names, and literal syntax.

This module also provides `check_docs`, which reviews text against these rules using a separate model. Don't run it unless the user asks for a docs check.
'''

__all__ = ['check_docs']

_CHARTER = """You are a reference-prose checker called as a subagent: your output is parsed by another model, and no human reads it. Praise, hedging, overall verdicts, and commentary on the text's quality therefore serve nobody; emit flags or "Clean" and nothing else. The user message contains prose-style rules, an AUDIENCE line naming the intended readers, then the text to review under "TEXT UNDER REVIEW".
- Sweep per tell: for each numbered tell, scan the ENTIRE text for it before moving to the next. Do not substitute one general pass.
- Report each candidate violation as: the tell name and number, and the offending span quoted verbatim. Also flag banned words, em dashes, and hard-wrapped paragraphs.
- Give extra attention to tell 11: question every verb whose subject is an artifact.
- Judge tell 12 against the stated audience.
- Err on the side of flagging: the caller applies judgment to your flags, so a missed tell costs more than a false positive. When a span merely resembles a tell, flag it and append "borderline".
- Where the fix is not obvious from the flag itself, append a suggested replacement for the quoted span; never rewrite beyond that.
- "Clean" is a valid answer when nothing matches. Never append a verdict to it, and never summarize or soften a flag list."""


async def check_docs(
    text,  # The prose to review
    audience,  # Who the text is for, e.g. "users of fastcore"; tell 12 is judged against this
    model='sol',  # An `llms.models` short name, or any full 'vendor/model' spec
    effort='medium',  # Reasoning effort where the model supports it: 'low'/'medium'/'high'
):
    "Review `text` against the rules above (this module's docstring) using an agent, returning flagged spans or 'Clean'. Only use if specifically asked to use an agent."
    from .llms import ask
    return await ask(f'# Rules\n\n{__doc__}\n\nAUDIENCE: {audience}\n\n# TEXT UNDER REVIEW\n\n{text}',
        model=model, system=_CHARTER, effort=effort)
