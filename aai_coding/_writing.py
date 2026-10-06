"Text that `write_docs` and `write_prose` share. Each module calls `fill` on its docstring at import, replacing each `{name}` placeholder with the matching `SHARED` entry."

SHARED = dict(
markers = r'''The numbers in brackets mark examples of the tells listed below. Where a number appears in both passages, the second passage shows the problem and the first shows the fix.''',

new_tells = r'''When you add a tell, give it the next number. Add a marked example to the second passage if a short sample can show the new tell.''',

splices = r'''Splices. Clauses joined with em dashes, semicolons, colons, ", and" or ", which". Spaced hyphens (` - ` or ` -- `) in place of an em dash are the same interrupted-clause habit with different punctuation. Swapping in a colon or a semicolon does not fix an em dash either. The clause after the splice usually restates the one before it or states an obvious implication. Try deleting it first. Splitting at the splice rarely fixes it, because the halves still read as one interrupted thought. Work out what the reader needs from the sentence, then write that. A colon that introduces a list or an example is not a splice, though the restatement tell covers a colon followed by a list that unpacks it.''',

consequence_glue = r'''Consequence glue. A clause appended with ", so", or with ", and" in the same sense ("the cache is warm, and calls are fast"). Treat every occurrence as wrong. The appended clause repeats the fact, states the obvious, adds detail the reader does not need (", so the channel set is rebuilt"), or makes a link that does not hold. Delete it. If the consequence matters, rebuild the sentence around that relation instead of appending it. Swapping in ", because" is not a rebuild. For example, "The getter returns a copy, so to edit, modify the copy and assign it back." becomes "To edit, modify the copy that the getter returns and assign it back." An ", and" clause that restates the fact goes the same way: "Inside brackets, a space separates items, and a run of tokens with no spaces between them is one item." becomes "Inside brackets, each run of tokens with no spaces in it is one item."''',

hedging = r'''Hedging. "may", "might", "potentially", "in some cases", "should generally". "This approach may potentially help improve performance in some cases" means nothing. Say what is true, such as "this is faster". If something is unspecified or untested, say that directly, such as "behavior with concurrent writers is undefined" or "we haven't benchmarked this yet".''',

noting_fillers = r'''Noting fillers. "note that", "it's worth noting", "it's important to note that", "notably", "importantly", "interestingly", "keep in mind". If the fact matters, state it early and plainly. Delete the filler.''',

filler_transitions = r'''Filler transitions. "Furthermore", "Moreover", "Additionally", "In conclusion", "To summarize", "When it comes to", "In the realm of". Use "and" or "also", or drop the transition and start with the subject. Watch for paragraphs that all open with "However" or "Furthermore".''',

restatement = r'''Restatement. Saying the same thing twice. The commonest forms are a heading repeated by the first line under it, a lead sentence that summarizes its paragraph, and a closing line that summarizes its paragraph or section. State each fact once, where it fits best. A summary earns its place only at document scale, as an abstract, a TL;DR or a README's first paragraph.''',

decorative_verbs = r'''Decorative verbs. A verb chosen for color, not because it names what happens. The subject is inanimate, with no person hidden behind it. The sentence states a property or a mechanical event, as in "native ids ride in summary rows", "an id earns its place", "a note lands in the output" or "media hang identity at different levels". Nothing rides, earns or lands. Say what happens: ids appear in rows, an id qualifies, a note appears in the output, media attach identity. The subject can stay inanimate when it really acts, as in "`watch` polls the process". Its verb must still be the plain word for the event. Standard technical vocabulary is not decoration: a span opens with its heading, you walk the tree, recursion bottoms out, a cache goes stale. The test is whether a maintainer would say the verb at a whiteboard. The "land" and "shape" entries under banned words are instances of this tell.''',

explaining_known = r'''Explaining the known. Telling readers what they already know: defining a term the audience uses daily ("air conditioning, a technology that cools indoor air"), spelling out an inference they make instantly ("an empty anchor, which a browser displays as nothing"), or stating a practice they take for granted ("the README documents each feature").''',

undefined_jargon = r'''Undefined jargon. A term you coined, used without definition, such as "consistent with the glidepath" or "the carrier" in a design doc. The reader is lost from that sentence on. The tell covers local coinages only: a project's own terms and internal vocabulary ("carrier", "wisp", a codename). Established outside terms of art (CFRunLoop, kqueue, TCC, monad) are fine, however specialized. Readers can look those up. Nobody can look up a coinage.''',

audience_judgment = r'''What counts as known depends on the audience. Name the audience when you write or review. Cut what the readers know. Define your own terms at first use, or use a plain word instead.''',

throat_clearing = r'''Throat-clearing. An opener that announces the document instead of starting with the subject, such as "This section describes...", "The purpose of this document is...", "This README covers...", "In this piece, we'll..." or "Let's dive into...". Delete it. Start with the subject itself.''',

todays_world = r'''Today's-world opener. "In today's [fast-paced/digital/modern] world..." or "In today's fast-moving AI landscape...". It is throat-clearing with marketing added. Start with the subject.''',

announce_deliver = r'''Announce-then-deliver. A label and a colon where a sentence should state the fact, such as "The core mechanism: `watch`.", "The fix: retry on timeout.", "Startup: the win." or "Here's the thing: ...". The label is scaffolding. Write the fact as a full sentence, such as "Retrying on timeout fixes it."''',

not_x_but_y = r'''Not-X-but-Y. "It's not X, it's Y", "isn't just X, it's Y" or "not X, but Y", as in "isn't just a poller - it's the liveness authority". It is the commonest LLM rhetorical crutch. Say directly what the thing is. Rewrite the sentence every time.''',

teaser_pivot = r'''Teaser pivot. "but here's where it gets interesting", "X, but the main event is Y", "the real story is...". A contrast flourish that holds back the point to build suspense. State the facts in order and let the emphasis come from what follows.''',

forced_symmetry = r'''Forced symmetry. Three parallel adjectives, as in "more efficient, more affordable, and more accessible" or "fresh ports, fresh channels, and a fresh interpreter". Other forms are three pros and three cons, five steps, sections padded to the same length, bullets where a sentence would do, and list items that all open with the same grammatical structure. Let the material decide the count. Be suspicious of any list of exactly three or five items. Nobody structures their actual thoughts that neatly.''',

appraisal_preamble = r'''Appraisal preamble. A clause that rates the content it introduces instead of delivering it, such as "the distinction is worth being precise about", "here's the key point", "what's interesting is" or "crucially". Its subject is a discourse object ("the reason", "the point", "the distinction") carrying an appraisal ("worth", "key", "important") and no domain content. It usually appears mid-paragraph, dressed as emphasis. State the fact without it.''',

artifact_agent = r'''Artifact-as-agent. An inanimate subject stands where the person who did the work belongs, as in "your tests shaped", "this PR introduces", "the change enables" or "the design lets you". The person vanishes. Name them, as in "I added retry logic". Or state the new behavior, as in "`connect` now retries".''',

recipient_subject = r'''Recipient-as-subject. The thing that benefits becomes the subject, with "gets", "gains" or "receives" as its verb. The doer moves into a trailing "via", "through" or "thanks to" phrase, or disappears, as in "the kernel gains fresh ports via the new process" or "the parser gains three node kinds". Name the doer and the deed ("I added three node kinds to the parser"). Or drop agency and state the new state ("there are now three node kinds in the parser", "the new process listens on fresh ports"). The second form avoids a drone of "I added..." sentences. What is wrong is the middle form, where a made-up event hides the real actor in a preposition.''',

decoration = r'''Decoration. Emoji, decorative unicode and ornamental symbols. Use ASCII unless asked otherwise. Write "->", not an arrow glyph, and write words, not emoji.''',

over_structuring = r'''Over-structuring. Headers, tables or bullets imposed on a document that fits on a screen. Headers are navigation. A document that short needs none. Bullets hold parallel facts. Do not chop prose into bullets.''',

false_depth = r'''False depth. Restating the problem in fancier words, listing obvious considerations, or concluding "it depends". Real depth comes from specifics, such as identifiers, numbers, data, edge cases and failure modes.''',

plain_words = r'''Use the plainest, least jargony word that is still correct:

- use, not "utilize" or "leverage"
- improve, not "enhance" or "optimize" (unless something is literally being optimized)
- complete, not "comprehensive"
- strong, not "robust"
- help, not "facilitate"
- smooth, not "seamless"
- let or help, not "empower"
- encourage, not "foster"''',

hidden_words = r'''Some words hide a plainer one. "Land" and "landed" hide the event. Things do not land, as in "landed on main", "the fix landed" or "a note lands in the output". Say what happened, such as merged, committed, pushed, released, added to the output, or appears. "Shape" and "shaped" are loose jargon for structure or influence, as in "same shape", "the shape of the data, API or process" or "your tests shaped ours". Write structure or format, or say what happened, such as adapted, copied or informed. "Shape" is fine as a geometric term or for array and tensor dimensions. Write "rule" or "guarantee" when that is what "invariant" means. Keep "invariant" only when nothing plainer is accurate. Compounds ending in "-bearing", such as load-bearing or text-bearing, have plainer forms.''',

formatting = r'''Do not hard-wrap prose. Write each paragraph as one continuous line and let the display soft-wrap it. Manual line breaks mid-paragraph make the text painful to reflow, edit and copy.

Put code symbols in backticks. This covers function names, parameters, file paths, module and package names (PyPI distributions included, such as `fastcore` and `toolslm`), and literal syntax (`to_html`, `{=html}`).''',
)


def fill(doc):
    "`doc` with each `{name}` placeholder replaced by `SHARED[name]`"
    for k,v in SHARED.items(): doc = doc.replace('{'+k+'}', v)
    return doc


def charter(
    kind, # The checker's register, e.g. 'prose' or 'reference-prose'
    verb_tells, # The guide's numbers for the decorative-verb and artifact-as-agent tells, e.g. '11 and 22'
    audience_tells, # The guide's audience tells, e.g. 'tell 12'
):
    "System prompt for a subagent that checks text against a writing guide"
    return f"""You are a {kind} checker called as a subagent: your output is parsed by another model, and no human reads it. Praise, hedging, overall verdicts, and commentary on the text's quality therefore serve nobody; emit flags or "Clean" and nothing else. The user message contains prose-style rules, an AUDIENCE line naming the intended readers, then the text to review under "TEXT UNDER REVIEW".
- Sweep per tell: for each numbered tell, scan the ENTIRE text for it before moving to the next. Do not substitute one general pass.
- Report each candidate violation as: the tell name and number, and the offending span quoted verbatim. Also flag banned words, em dashes, and hard-wrapped paragraphs.
- Give extra attention to the two verb tells, {verb_tells}: they are the subtlest and the most commonly missed. Question every verb whose subject is an artifact.
- Judge {audience_tells} against the stated audience.
- Err on the side of flagging: the caller applies judgment to your flags, so a missed tell costs more than a false positive. When a span merely resembles a tell, flag it and append "borderline".
- Where the fix is not obvious from the flag itself, append a suggested replacement for the quoted span; never rewrite beyond that.
- "Clean" is a valid answer when nothing matches. Never append a verdict to it, and never summarize or soften a flag list."""
