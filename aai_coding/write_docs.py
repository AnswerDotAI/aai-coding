r'''How to write reference prose. Read this before writing docstrings, READMEs, API docs, PR descriptions, commit messages, or messages to co-workers.

Every edit you make with this guide MUST improve the prose for its reader. The numbered tells below are symptoms of unclear writing, not lint rules. NEVER fix a tell mechanically, such as by swapping punctuation or deleting a flagged word. When a passage shows tells, work out what its reader needs from it, then explain that again from the start, following "Rewriting high-scoring documentation" below.

# Writing Reference Prose

Reference prose is the writing that goes with code. It covers docstrings, code comments, READMEs, API and reference docs, changelogs, PR descriptions, commit messages, and messages to co-workers. Readers scan it for the fact they came for, then leave. Write it plainly and directly, in the style of GOV.UK/GDS and ASD-STE100. Start with what the code does. Plain does not mean formal, and the author's voice can stay. For blog posts, essays, and announcements use write-prose. For choosing what a summary says, use write-summary.

Here is a passage from a design doc, written in this style:

> `GatewayKernel` ties the three lower layers together. The ready-wait runs once per kernel, in `start`.[1][3] `watch` polls the process and the heartbeat. A process that dies unexpectedly broadcasts the synthesized `dead` status.[1] After three missed heartbeats,[4] the gateway marks the kernel `unresponsive` in its model. It clears the mark when the next echo arrives.
>
> The gateway never kills an unresponsive kernel.[2] A kernel becomes `dead` only when its process exits.[2] `restart` terminates and respawns with fresh ports in a new process. Clients see `restarting`, then `starting` once the new kernel is ready.[5]

Write like that. Each sentence states one fact. Each rule the reader relies on has its own sentence. The passage also says what the gateway never does. It gives every status its real name. Sentences this even would be dull in an essay. They suit a reader who is looking something up.

Here is the same passage before editing:

> This section describes how `GatewayKernel` manages the kernel lifecycle.[13] `GatewayKernel` ties the three lower layers together, and its `start` is the only place the ready-wait runs: once per kernel, ever.[1][3] The core mechanism: `watch`.[15] It isn't just a poller - it's the liveness authority.[16] Furthermore,[19] it polls the process and the heartbeat: a process that dies unexpectedly broadcasts the synthesized `dead` status, and three missed beats[4] mark the kernel `unresponsive` in its model.[1] The distinction is worth being precise about.[21] That marking is observational only - only process exit means dead -[2] and it clears itself on the next echo. So what does `restart` actually do?[18] It terminates and respawns; the kernel gains fresh ports, fresh channels, and a fresh interpreter via the new process,[20][23] so the channel set is rebuilt[6] and clients simply[3] see `restarting` then a fresh welcome-backed ready kernel.[5]

Do not write like that. Nothing in it is false, and a blog post could get away with it. It is hard to use as reference. Each sentence carries more than one fact. An aside holds the most important rule. The final state gets a flourish where its name should be. The first sentence announces the section. A question delays a fact the reader came for.

{markers} The passages are too short to show tells 7-12, 14, 17, 22 and 24-26.

1. {splices} Write one idea per sentence. Narrative prose can use an occasional join. Reference prose should not.
2. Key rule in an aside. The rule the reader most needs appears only in an aside, a contrast, or a parenthetical. "That marking is observational only" hints at the rule. "The gateway never kills an unresponsive kernel" states it. Give every rule its own sentence. Say what the system never does when a reader would be surprised by it.
3. Emphasis devices. "ever", "simply", "just", "the only place", bold, italics. Use position for emphasis. Put the key fact first in its sentence. Put the key sentence first in its paragraph. Delete the intensifiers.
4. Elegant variation. "The heartbeat" becomes "beats" a sentence later. Use one name for one thing every time, even when it feels repetitive. Do not use one word for two things either. STE calls this "one meaning per term".
5. Flourish over identifier. "A fresh welcome-backed ready kernel" when the real status is `starting`. Use the actual identifier, state, value, or number. The reader will search for it, test against it, and see it in logs.
6. {consequence_glue}
7. {hedging}
8. {noting_fillers}
9. {restatement}
10. Justification rider. A fact with a benefit attached, such as "kind-sorted so a collector stays legal wherever it came from" or "parses bools so flag values test correctly". The extra clause argues for the fact. Reference prose says what the code does. Reasons belong in design docs and narrative prose.
11. {decorative_verbs}
12. Audience misjudged. Writing for the wrong reader takes two forms, explaining the known and undefined jargon. {audience_judgment}
    - {explaining_known}
    - {undefined_jargon}
13. {throat_clearing}
14. {todays_world} In a README, the subject is what the package does.
15. {announce_deliver}
16. {not_x_but_y}
17. {teaser_pivot}
18. Rhetorical questions. "So what does `restart` actually do?". Do not ask the reader questions, in headings or in prose. Write the statement that the question delays. GDS bans FAQ pages for the same reason.
19. {filler_transitions}
20. {forced_symmetry}
21. {appraisal_preamble}
22. {artifact_agent}
23. {recipient_subject}
24. {decoration}
25. {over_structuring}
26. {false_depth}

slopometer binds its rules to the tell numbers above. {new_tells}

Address the reader as "you" and use the imperative. Write "Run the tests", not "The tests should be run". Prefer active voice. A passive sentence often hides who does the action, and the reader needs to know that.

## Banned words

{plain_words}

Do not use these words: seamless, streamline, empower, foster, pivotal, "a testament to", realm, landscape (metaphorical), navigate (metaphorical), delve, myriad, plethora, paradigm, synergy, holistic, catalyze, juxtapose, tapestry, embark, endeavor, encompass, multifaceted, elucidate, nuanced (as filler), minted (metaphorical).

{hidden_words}

## Doc types

- Docstrings. The first line says what the function does. For most functions that line is the whole docstring. Put parameters and return values in docments, and do not repeat them in prose. Add a guarantee, edge case or error only when a caller needs it to use the function. Do not restate the signature.
- Code comments. Write one only to state something the code cannot show, next to the code it concerns (see coding-patterns). This is rare.
- READMEs. Write them like docstrings, not blog posts. The first paragraph says what the package does and who it is for. Install steps come next, then a minimal example. Leave out the project's history and sales language. A README, index or module docstring describes what the package is for and its main workflows. Put parameters and return values in docments. Put edge cases and error behaviour in notebooks or other docs, and in a docstring only when a caller needs them to use the API. Do not add a README section for a new method unless it changes how people use the package.
- API docs and changelogs. Describe the behavior or the change, with one entry per behavior. Put reasons in design docs.
- PR descriptions and commit messages. Start with the behavior change. Say who did what. Give reviewers what they need to judge the diff. write-summary covers choosing the content.
- Messages to co-workers. Put the answer first and the support after. Do not open by softening the message. Do not close by offering more help.

{formatting}

## Rewriting high-scoring documentation

A high slopometer score means the document needs explaining again from the start. Do not repair the flagged sentences one at a time. Do not split sentences, swap banned words, or delete clauses until the score falls. Short sentences can still be unreadable. Aim for a score below 4. A low score does not show that a document is clear, accurate, or complete.

Improve prose by rereading it as its reader would. Never search it for tells, even to find candidates.

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

from ._writing import fill, charter
__doc__ = fill(__doc__)

__all__ = ['check_docs']

_CHARTER = charter('reference-prose', '11 and 22', 'tell 12')


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
