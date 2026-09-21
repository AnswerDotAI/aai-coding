r'''How to write reference prose. Read this before writing docstrings, READMEs, API docs, PR descriptions, commit messages, or messages to co-workers.

# Writing Reference Prose

Reference prose is the writing that goes with code. It covers docstrings, code comments, READMEs, API and reference docs, changelogs, PR descriptions, commit messages, and messages to co-workers. Readers scan it for the fact they came for, then leave. Write it plainly and directly, in the style of GOV.UK/GDS and ASD-STE100. Start with what the code does. Plain does not mean formal, and the author's voice can stay. For blog posts, essays, and announcements use write-prose. For choosing what a summary says, use write-summary.

Here is a passage from a design doc, written in this style:

> `GatewayKernel` ties the three lower layers together. The ready-wait runs once per kernel, in `start`.[1][3] `watch` polls the process and the heartbeat. A process that dies unexpectedly broadcasts the synthesized `dead` status.[1] Three missed heartbeats[4] mark the kernel `unresponsive` in its model, with the next echo clearing the mark.
>
> The gateway never kills an unresponsive kernel.[2] A kernel becomes `dead` only when its process exits.[2] `restart` terminates and respawns with fresh ports in a new process. Clients see `restarting`, then `starting` once the new kernel is ready.[5]

Write like that. Each sentence states one fact. Each rule the reader relies on has its own sentence. The passage also says what the gateway never does. It gives every status its real name. Sentences this even would be dull in an essay. They suit a reader who is looking something up.

Here is the same passage before editing:

> This section describes how `GatewayKernel` manages the kernel lifecycle.[13] `GatewayKernel` ties the three lower layers together, and its `start` is the only place the ready-wait runs: once per kernel, ever.[1][3] The core mechanism: `watch`.[15] It isn't just a poller - it's the liveness authority.[16] Furthermore,[19] it polls the process and the heartbeat: a process that dies unexpectedly broadcasts the synthesized `dead` status, and three missed beats[4] mark the kernel `unresponsive` in its model.[1] The distinction is worth being precise about.[21] That marking is observational only - only process exit means dead -[2] and it clears itself on the next echo. So what does `restart` actually do?[18] It terminates and respawns; the kernel gains fresh ports, fresh channels, and a fresh interpreter via the new process,[20][23] so the channel set is rebuilt[6] and clients simply[3] see `restarting` then a fresh welcome-backed ready kernel.[5]

Do not write like that. Nothing in it is false, and a blog post could get away with it. It is hard to use as reference. Each sentence carries more than one fact. An aside holds the most important rule. The final state gets a flourish where its name should be. The first sentence announces the section. A question delays a fact the reader came for.

The numbers in brackets mark examples of the tells listed below. Where a number appears in both passages, the second passage shows the problem and the first passage shows the fix.

1. Splices. Clauses joined with em dashes, semicolons, colons, ", and", or ", which". Write one idea in each sentence, then end the sentence. Narrative prose can use an occasional join. Reference prose should not.
2. Key rule in an aside. The rule the reader most needs appears only in an aside, a contrast, or a parenthetical. "That marking is observational only" hints at the rule. "The gateway never kills an unresponsive kernel" states it. Give every rule its own sentence. Also say what the system never does. Readers rely on that as much as on what it does.
3. Emphasis devices. "ever", "simply", "just", "the only place", bold, italics. Use position for emphasis. Put the key fact first in its sentence. Put the key sentence first in its paragraph. Delete the intensifiers.
4. Elegant variation. "The heartbeat" becomes "beats" a sentence later. Use one name for one thing every time, even when it feels repetitive. Do not use one word for two things either. STE calls this "one meaning per term".
5. Flourish over identifier. "A fresh welcome-backed ready kernel" when the real status is `starting`. Use the actual identifier, state, value, or number. The reader will search for it, test against it, and see it in logs.
6. Consequence glue. A clause joined with ", so". The consequence often repeats the fact, adds detail the reader does not need (", so the channel set is rebuilt"), or does not follow. Delete it. If the consequence matters, give it its own sentence.
7. Hedging. "may", "might", "potentially", "in some cases", "should generally". Say what the code does. If behavior is unspecified or untested, say that directly, for example "behavior with concurrent writers is undefined" or "not benchmarked".
8. Noting fillers. "note that", "it's worth noting", "importantly", "keep in mind". If the fact matters, state it early and plainly. Delete the filler.
9. Restatement. A heading repeated by the first line under it. A lead sentence that summarizes its paragraph. A closing line that summarizes its section. State each fact once, where it fits best. A summary is worth having only for a whole document. A README's first paragraph is one.
10. Justification rider. A fact with a benefit attached, such as "kind-sorted so a collector stays legal wherever it came from" or "parses bools so flag values test correctly". The extra clause argues for the fact. Reference prose says what the code does. Reasons belong in design docs and narrative prose.
11. Decorative verbs. A verb chosen for color when a plain verb names the event. Ids "ride" in rows. A note "lands" in the output. Ask whether you would say the verb at a whiteboard. An artifact can be the subject when it really acts, as in "`watch` polls the process". Its verb must still be the plain one.
12. Audience misjudged. This goes wrong in two ways. One is explaining what every reader of the doc already knows, such as "the README documents the package". The other is using a term you coined, such as "the carrier", without defining it. Decide who the readers are. Cut what they know. Define your own terms at first use. Established terms from outside can stay, because readers can look them up. They cannot look up a term you coined.
13. Throat-clearing. An opener that announces the document, such as "This section describes...", "The purpose of this document is...", or "This README covers...". Delete it. The first sentence states the first fact.
14. Today's-world opener. "In today's fast-moving AI landscape...". This is the README form of throat-clearing, with marketing added. Start with what the package does.
15. Announce-then-deliver. A label and a colon where a sentence should be, such as "The core mechanism: `watch`." or "The fix: retry on timeout." Write a full sentence, such as "Retrying on timeout fixes it."
16. Not-X-but-Y. "isn't just a poller - it's the liveness authority", "not X, but Y". Say directly what the thing is. Rewrite the sentence every time.
17. Teaser pivot. "but here's where it gets interesting", "the real story is". These hold back a fact to build suspense. State the facts in order.
18. Rhetorical questions. "So what does `restart` actually do?". Do not ask the reader questions, in headings or in prose. Write the statement that the question delays. GDS bans FAQ pages for the same reason.
19. Filler transitions. "Furthermore", "Moreover", "Additionally", "In conclusion", "When it comes to". Use "and" or "also", or start with the subject.
20. Forced symmetry. Three parallel adjectives, as in "fresh ports, fresh channels, and a fresh interpreter". Three pros and three cons. Sections padded to the same length. List items forced into one grammatical pattern. Let the material decide the count. Check any list of exactly three.
21. Appraisal preamble. A clause that rates what comes next, such as "the distinction is worth being precise about", "the key point is", or "crucially". State the fact without it.
22. Artifact-as-agent. "this PR introduces", "the change enables", "the design lets you". A person did the work. Name that person, as in "I added retry logic". Or state the new behavior, as in "`connect` now retries".
23. Recipient-as-subject. The thing that benefits becomes the subject, with "gets", "gains", or "receives". The doer moves into a "via" or "through" phrase, as in "the kernel gains fresh ports via the new process". Name the doer and the action. Or state the result, as in "the new process listens on fresh ports".
24. Decoration. Emoji, decorative unicode, and ornamental symbols. Use ASCII. Write "->", not an arrow glyph. Write words, not emoji.
25. Over-structuring. Headers, tables, or bullets added to a document that fits on a screen. Headers are for navigation, and a short document needs none. Bullets hold parallel facts. Do not chop prose into bullets.
26. False depth. Restating the problem in fancier words. Listing obvious considerations. Concluding "it depends". Give specifics, such as identifiers, numbers, edge cases, and failure modes.

The passages are too short to show tells 7-12, 14, 17, 22, and 24-26. When you add a tell, give it the next number. slopometer binds its rules to these numbers. Add a marked example to the second passage if a short sample can show the new tell.

Address the reader as "you" and use the imperative. Write "Run the tests", not "The tests should be run". Prefer active voice. A passive sentence often hides who does the action, and the reader needs to know that.

## Banned words

Use the plainest word that is still correct:

- use, not "utilize" or "leverage"
- improve, not "enhance" or "optimize" (unless something is literally being optimized)
- complete, not "comprehensive"
- strong, not "robust"
- help, not "facilitate"

Do not use these words: seamless, streamline, empower, foster, pivotal, "a testament to", realm, landscape (metaphorical), navigate (metaphorical), delve, myriad, plethora, paradigm, synergy, holistic, catalyze, juxtapose, tapestry, embark, endeavor, encompass, multifaceted, elucidate, nuanced (as filler), minted (metaphorical).

Some words hide a plainer one. "Land" and "landed" hide the event. Say what happened, such as merged, committed, released, or appears. Replace a metaphorical "shape" or "shaped" with structure, format, or the actual event. Write "rule" or "guarantee" when that is what "invariant" means. Compounds ending in "-bearing", such as load-bearing or text-bearing, have plainer forms.

## Doc types

- Docstrings. The first line says what the function does. For most functions that line is the whole docstring. Put parameter detail in docments, and do not repeat it in prose. State inputs, outputs, errors raised, and guarantees. Do not restate the signature.
- Code comments. Write one only for a constraint the code cannot show (see coding-patterns). This is rare.
- READMEs. Write them like docstrings, not blog posts. The first paragraph says what the package does and who it is for. Install steps come next, then a minimal example. Leave out the project's history and sales language.
- API docs and changelogs. Describe the behavior or the change, with one entry per behavior. Put reasons in design docs.
- PR descriptions and commit messages. Start with the behavior change. Say who did what. Give reviewers what they need to judge the diff. write-summary covers choosing the content.
- Messages to co-workers. Put the answer first and the support after. Do not open by softening the message. Do not close by offering more help.

Do not hard-wrap prose. Write each paragraph as one continuous line and let the display soft-wrap it. Put code symbols in backticks. This covers function names, parameters, file paths, module and package names, and literal syntax.

## Rewriting high-scoring documentation

A high slopometer score means the document needs explaining again from the start. Do not repair the flagged sentences one at a time. Do not split sentences, swap banned words, or delete clauses until the score falls. Short sentences can still be unreadable. Aim for a score below 4. A low score does not show that a document is clear, accurate, or complete.

Change how the document explains things, and keep its information. Keep technical detail that a reader might need. A shorter document is worse if it drops a capability, condition, or explanation that the reader needs.

Removing slop does not mean removing character. Keep the author's informality, conversational phrasing, contractions, and humor where they communicate clearly. Informal language is not slop. AI slop is often too clever. It uses strained metaphors, elaborate phrasing, and invented terms that make a simple point hard to follow. Judge language by what it communicates, not by how formal it sounds. Do not replace a human voice with generic reference prose. Do not invent a new persona for the author.

Work through these steps in order:

- Establish the facts. Read the implementation and executable examples before drafting. Decide who the readers are and what they need to understand or do. List the original's substantive points. These include capabilities, responsibilities, inputs, outputs, identifiers, defaults, guarantees, exclusions, edge cases, failure behavior, and context. Check claims against the code. Record claims that are wrong or uncertain. Do not repeat them silently.
- Write from understanding. Put the old wording aside and draft from the facts. Choose an order that explains the system to the intended reader. Do not keep old sentences, paragraph structure, or coined terms because they are already there. Name who performs each operation. Introduce each concept before you use it. State guarantees directly.
- Keep the context. Explain the problem the code solves and the relationships a reader needs to understand its behavior. Keep prerequisites, setup, protocol distinctions, and reasons that affect correct use. Do not turn an explanation into disconnected facts. Do not squeeze it into unexplained identifiers. Remove sales-style justification. Keep the reasoning a reader needs to use the code correctly.
- Audit technical coverage. Find every substantive point of the original in the rewrite. Repeated facts can share one clear statement. If you move a fact, check that the reader can still find it where they need it. Keep details whose relevance is uncertain. Flag proposed omissions for review. Do not decide silently that they do not matter. Correct false claims from evidence and report the corrections.
- Review descriptions separately. In nbdev, the first blockquoted paragraph below the title becomes the description. Module listings and generated documentation reuse it without the surrounding explanation. Keep its coverage of capabilities and its technical scope. For example, a description covers NDJSON transport, control routing, and deferred tool results. Replacing it with "Communicate through standard input and output" loses two of those responsibilities. Check the description on its own, even when the body explains all three.
- Verify the finished document. Read the rewrite from top to bottom beside its examples. Check accuracy, readability, retained context, technical coverage, and the author's voice before scoring. For notebooks, follow `nbdev.skill`, edit the source notebook, regenerate exports, and run the affected notebook tests. Leave implementation behavior unchanged unless the user separately asks for code changes. Update stale example outputs by running the code, not by editing them.
- Rescore independently at the end. Use a fresh scoring process after the rewrite and its coverage audit are complete. Do not use intermediate scores to choose wording or remove information. Report the final score, word count, findings, and test results. If the score is still high, reconsider the explanation as a whole. Do not dismiss the document's problems because some individual findings are false positives.

When the user authorizes delegated rewrites, give each agent one bounded document scope and these instructions. Require the agent to report corrections, proposed omissions, verification results, and the final independent score. Review the rewritten document against the original's technical content and against the implementation. A score below 4 does not replace that review.

This module also provides `check_docs`. It sends text and these rules to a separate model for review. Do not run it unless the user asks for a docs check.
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
