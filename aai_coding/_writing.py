"Text that `write_docs` and `write_prose` share. Each module calls `fill` on its docstring at import, replacing each `{name}` placeholder with the matching `SHARED` entry."

SHARED = dict(
    markers = r'''`[n]` marks tells; in both passages, 2nd=problem, 1st=fix.''',
    new_tells = r'''New tell: next number; mark 2nd passage if short.''',
    tacked_on = r'''Tacked-on clauses & consequence glue: em dash (` - `,` -- `), `;`, `:`, `, and`, `, which`, or trailing `, so` / same-sense `, and` ("cache is warm, and calls are fast") restating/implying prior clause (list/example `:` OK; label+list=restatement). Rebuild from reader needs, never split or swap `, because`.''',
    hedging = r'''Hedging: "may/might/potentially/in some cases/should generally". State truth or direct uncertainty ("undefined with concurrent writers").''',
    filler = r'''Filler: noting ("note that", "worth/important to note", "notably/importantly/interestingly", "keep in mind"->delete); transitions ("Furthermore/Moreover/Additionally/In conclusion/To summarize/When it comes to/In the realm of"->use "and"/"also" or lead with subject).''',
    restatement = r'''Restatement: heading echoed by line 1; lead/closing paragraph summary. State once; summaries at doc scale only (abstract/TL;DR/README p1).''',
    decorative_verbs = r'''Decorative verbs: verb not naming event or impossible for inanimate subject. Colorful ("ids ride", "note lands"->appear); impossible plain ("dfn names arg", "count takes items", "settings load"->actor/imperative/passive); mental (`want/need/decide/respect/rely on/invent`); ownership/comms (`own/assign/carry/ship/record/respond`, structural `reads as`). OK: real action ("holds value", "`watch` polls"), perceptual ("read as bright"), whiteboard idioms ("walk tree", "goes stale", "costs O(n)"). Whiteboard test. (`land`/`shape` below.)''',
    audience = r'''Audience misjudged: name audience; cut knowns; define local terms or use plain words. Explaining known: daily terms ("air conditioning, a technology that cools air"), instant inferences, obvious practices. Undefined jargon: local coinages ("glidepath", "carrier", "wisp", codenames); terms of art (CFRunLoop, kqueue, monad) OK.''',
    throat_clearing = r'''Throat-clearing: openers announcing doc ("This section describes...", "Purpose of...", "In this piece...", "Let's dive into...") or today's-world ("In today's [fast-paced/digital/modern] world...", "...AI landscape..."). Delete; start with subject.''',
    advertising = r'''Metadiscourse/advertising: stub+`:` ("Core mechanism: `watch`.", "Fix: retry."->full sentence); teaser pivot ("here's where it gets interesting", "X, but main event is Y", "real story is..."->facts in order); appraisal preamble ("worth being precise", "key point", "what's interesting", "crucially"->delete).''',
    not_x_but_y = r'''Not-X-but-Y: "It's not X, it's Y", "isn't just X, it's Y", "not X, but Y". State directly.''',
    symmetry = r'''Forced symmetry & over-structuring: 3 adjectives, 3 pros/cons, 5 steps, equal sections, matching openers (distrust 3/5); headers/tables/bullets on 1-screen doc (headers=navigation; bullets for parallel facts only).''',
    agent_defocusing = r'''Agent defocusing: artifact-as-agent hides person ("tests shaped", "PR introduces", "design lets you"->person "I added..." or behavior "`connect` retries"; UI: "override `--x` on `[ui]`", not "`[ui]` can change `--x`"); recipient-as-subject puts beneficiary with `gets/gains/receives` + doer in `via/through/thanks to` or dropped->name actor or new state ("new process listens on fresh ports").''',
    decoration = r'''Decoration: emoji/ornamental unicode. ASCII unless asked (`->`, words).''',
    false_depth = r'''False depth: fancier restatement, obvious points, "it depends". Give specifics: identifiers, numbers, edge cases, failures.''',
    plain_words = r'''Plain: utilize/leverage->use; enhance/optimize (unless literally optimizing)->improve; comprehensive->complete; robust->strong; facilitate->help; seamless->smooth; empower->let/help; foster->encourage.''',
    banned_words = r'''Banned: streamline, pivotal, "a testament to", realm, landscape (metaphorical), navigate (metaphorical), delve, myriad, plethora, paradigm, synergy, holistic, catalyze, juxtapose, tapestry, embark, endeavor, encompass, multifaceted, elucidate, nuanced (filler), minted (metaphorical).''',
    hidden_words = r'''Hidden jargon: land/landed->merged/committed/pushed/released/appears; shape/shaped (OK geometry/array/tensor)->structure/format/adapted/copied/informed; invariant->rule/guarantee unless none plainer; `-bearing`->plainer form.''',
    formatting = r'''Formatting: 1 line/para (soft-wrap). Backtick code: functions, params, paths, packages (`fastcore`), literal syntax (`to_html`, `{=html}`).''')


def fill(doc):
    "`doc` with each `{name}` placeholder replaced by `SHARED[name]`"
    for k,v in SHARED.items(): doc = doc.replace('{'+k+'}', v)
    return doc


def charter(
    kind, # The checker's register, e.g. 'prose' or 'reference-prose'
    verb_tells, # The guide's numbers for the decorative-verb and agent-defocusing tells, e.g. '10 and 17'
    audience_tells, # The guide's audience tell, e.g. 'tell 11'
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
