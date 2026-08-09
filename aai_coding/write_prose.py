r'''How to write prose that doesn't read as AI slop: read before writing anything for human readers.

# Writing Prose That Doesn't Sound Like AI

Guidelines for writing clear, human-sounding prose. Apply these when writing documentation, blog posts, READMEs, or any prose. The overall goal is a style combining the best parts of GOV.UK/GDS house style, ASD-STE100, and The Economist.

Here is a passage from The Economist:

> No form of emissions reduction, though, can quickly bend the current trajectory.[1][2] Endurance is what remains.[3][14] Making air conditioning more efficient, cheap and widespread[10] saves lives[6] and fits well with other policy goals, like making clean electricity cheap to produce and consume.[7] Ten years ago a commitment to phase out the fluorinated gases in cooling systems was reached in Kigali, the capital of Rwanda.[8][9] There is scope for extra international efforts to improve the machinery that uses them.[7][19] This could double the cooling benefit of phasing out the gases.[6]

Each sentence sets out to say one thing, says it, and stops. It is simple plain English prose. It carries no byline and needs none. Plainness, not personality, does the work. It's not trying to sell anything. It lets you figure out what the takeaways are.

Write like that.

Here, on the other hand, is a horrendous rewrite, as sloppy as possible:

> In this piece, we'll dive deep into the fascinating world of cooling![1] 🌡️[15] Here's the thing:[2] emissions reduction alone **isn't going to cut it**. In today's rapidly-warming world,[4] it's not about quick fixes — it's about *endurance*.[3] When it comes to[5] air conditioning, a technology that cools indoor air,[20] one might argue[5] that a comprehensive, holistic approach — making units more efficient, more affordable, and more accessible[10] — could potentially help save countless lives in some cases,[6] while seamlessly aligning with broader policy goals like fostering[7] clean, affordable electricity for all, and also, it's worth noting,[5] building on the pivotal commitment to phase out fluorinated gases that was reached ten years ago in Kigali — the vibrant capital of Rwanda —[16] a commitment that has reshaped the landscape of cooling policy and continues to empower stakeholders[9] across the realm of climate diplomacy.[8]
>
> But here's where it gets really exciting.[11] 🤯 The Kigali deal isn't just a treaty — it's a **game-changer**.[3] Here's what's fascinating:[24] the machinery that leverages[7] these gases gets a myriad of enhancements via this framework,[19] consistent with the glidepath,[23] which could unlock further benefits, and which, honestly,[5] may potentially double the cooling upside of phasing them out, depending on context.[6][8] Getting there is just[12] a matter of commitment. The reason is simple:[22] demand keeps rising, and real progress rides on[21] frameworks like these. Furthermore, as we can see,[5] the journey ahead is a rich tapestry of innovation: the tech we build, the deals we strike, the grids we green[25] — a testament[7] to what we can achieve when we navigate this challenge together. In conclusion:[5] the bottom line?[13] Endurance is the name of the game — in other words, success is all about sticking with it for the long haul.[14] 💪

Do **NOT** write like that.

The numbers below refer to the [bracketed] markers in both passages. Where a number appears in each, the pair is the sloppy and the plain version of the same thing. Entries 17 and 18 are paragraph-scale tells that a one-paragraph sample cannot show.

1. Throat-clearing: an opener that announces the piece instead of starting with the subject: "In this piece, we'll...", "Let's dive into...", "Let's explore...", "In this section, we will...". Don't clear your throat. The first sentence should do real work.
2. Announce-then-deliver: a label and a colon in place of stating the fact ("The fix: retry on timeout", "Startup: the win", "Here's the thing: ..."). The label is scaffolding. State the fact as a sentence: "Retrying on timeout fixes it."
3. Not-X-but-Y: "It's not X, it's Y" / "isn't just X, it's Y", the #1 LLM rhetorical crutch. State the positive directly. Restructure every time.
4. Today's-world opener: "In today's [fast-paced/digital/modern] world...".
5. Filler phrases: they add zero information; state the thing directly.
    - "It's worth noting that..." / "It's important to note that..." / "Notably, ..." / "Importantly, ..." / "Interestingly, ..."
    - "As we can see..." / "As mentioned earlier..."
    - "In conclusion, ..." / "To summarize, ..."
    - "Furthermore, ..." / "Moreover, ..." / "Additionally, ..." -> use "and", "also", or just start a new sentence. If every paragraph opens with "However" or "Furthermore", drop the transition word and start with the actual subject.
    - "When it comes to..." / "In the realm of..."
    - "One might argue that..." / "It could be suggested that..."
    - "A [comprehensive/holistic/nuanced] approach to..." -> "an approach to"
    - "honest"/"honestly"/"to be honest" as a throat-clear ("the honest tradeoff", "honestly, it's fine"): in speech this flags a rare, significant admission. Sprinkled everywhere it's noise. Delete it in nearly every case.
    - "deliberately"/"intentionally"/"carefully"/"thoughtfully": adverbs about the author's mental state rather than the thing. In a design doc every recorded choice is already deliberate, and the explanation that follows does the work. Keep one only when the reader would otherwise suspect an accident and no explanation follows ("the file is deliberately empty").
6. Hedging: the worst offender. "This approach may potentially help improve performance in some cases" means nothing. Say "this is faster" or say "we haven't benchmarked this yet". The original commits: "saves lives", "could double".
7. Inflated diction: puffed-up words where plain ones exist: enhance/leverage for improve/use, plus seamlessly, fostering, pivotal, myriad, landscape, realm, empower, journey, tapestry, testament, navigate. The Banned Words lists below are the fuller reference.
8. Sentence sprawl: one over-long sentence stacking clauses that should be separate sentences, chained with "so", "which", "but", and "and", each extending or qualifying the last. Write one idea per sentence. When a draft sentence joins two thoughts, try the split. Keep the join only when the connection itself is the point.
9. Artifact-as-agent: the commitment "has reshaped the landscape" and "continues to empower". Really, people reached a commitment; say what happened, with the actors in place. Three stacked habits make these sentences (e.g. "Your tests shaped the ones that landed"):
    - Artifact as agent: an inanimate subject stands where the doer belongs ("your tests shaped", "this PR introduces", "the change enables"). The person who did the work vanishes.
    - Oblique reference instead of naming: the object is pointed at through a relative clause or metaphor ("the ones that landed") rather than named ("our new tests").
    - Narrative compression into a single transitive clause: a who-did-what story (I read your tests, adapted them, committed mine) flattened into "X verbed Y", an aphorism that sounds polished because it discards the actors and the order of events. Common as a sentence-final flourish.

    Rewrite as the actual events with the actual actors: "I took your tests as inspiration and added some updates based on these changes."
10. The AI triad: three parallel "more X" adjectives. The original's list varies its forms. AI can't resist symmetry in general: three pros, three cons, five steps, equal-length sections, bullets where a sentence would do, every list item opening with the same grammatical structure. If you catch yourself writing exactly three or five items, be suspicious. Nobody structures their actual thoughts that neatly.
11. Teaser pivot: "but here's where it gets really exciting", "X, but the main event is Y", "but the real story is...". A sibling of 3: a contrast flourish that withholds the point to build fake suspense. State the facts in order and let the emphasis come from what follows.
12. Minimizing "just": using it as a casual softener ("resets just that kata", "it's just a wrapper", "just works"): be frugal with it. Usually delete it; when the restriction genuinely matters, "only" is plainer.
13. Rhetorical wrap-up: a rhetorical question as a closing flourish.
14. Restatement: saying the same thing twice. The original says it once, in four words. The commonest form is a lead sentence that summarizes the paragraph it starts; everything it says reappears, with more detail, in the sentences that follow. Delete it and nothing is lost:

    > ~~Failures are visible now too.~~ A startup failure used to print to the server log and leave a half-booted dialog that looked ready. It now raises, the user gets an error toast and a red status dot, and the dialog stays editable.

    The mirror form is the closing sentence that summarizes the paragraph or piece it ends ("LLMs can now use the module with far fewer tokens", ending a paragraph whose second sentence said so). It is the taught essay shape, and the strongest LLM habit of the lot. End on the last fact. The same disease occurs within a sentence ("editing needs no kernel: cards echo through the outbound queue, which is kernel-independent", where the final clause restates the opening) and between a header and its section's first line. Ask whether deleting the phrase removes any information from the document; if not, delete it. Summaries earn their place at document scale (an abstract, a TL;DR), not per paragraph. And prefer the shorter phrasing of the same fact: "nothing new needs specifying", not "there is nothing new to learn and nothing new to specify".
15. Decoration: emoji, and decorative bold and italics. Bold and italics in the body of a paragraph should be used VERY sparingly; don't exhaust the reader with overuse of rhetorical flourishes. Avoid emojis and non-ascii unicode unless requested otherwise, e.g. "->" instead of "→".
16. Splicing: em-dash interruptions and their kin. Avoid em dashes entirely. Substituting ` - ` or ` -- ` is just as bad, being the same interrupted-clause habit with different punctuation. Restructure the sentence instead, and when in doubt use a period. Two short sentences nearly always read better than one spliced one. Phrase combiners like `:` and `;` should be rare in normal prose (a colon that introduces a list or example is fine, though see tell 25; one that splices two clauses is the habit to avoid), so don't fix an em dash by swapping in a different splice.
17. Monotone rhythm: topic sentence, elaboration, example, wrap-up, paragraph after paragraph. The reader's eyes glaze over. Mix it up. Real writing is lumpy. Some sections run long because they need to. Others are two sentences because that's all there is to say.
18. False depth: restating the problem in fancier words, listing obvious considerations, concluding with "it depends". Real depth comes from specifics, data, and edge cases.
19. Recipient-as-subject: the thing that benefited is promoted to subject, the verb is "gets/gains/receives", and the doer hides in a trailing "via"/"through"/"thanks to" phrase: "the parser gains three node kinds". As in tell 9, the actor vanishes; the artifact just moves from performing the action to receiving it. Either name the doer and the deed ("I added three node kinds to the parser"), or drop agency entirely and state the new state ("there are now three node kinds in the parser"). The second avoids a drone of "I added..." sentences; what's banned is the middle form, where a fake event hides the real actor in a preposition.
20. Explaining the known: telling readers what they already know. Defining a term the audience uses daily ("air conditioning, a technology that cools indoor air"), spelling out an inference they make instantly ("an empty anchor, which a browser displays as nothing"), or stating a practice they take for granted ("the README documents each feature"). Tell 14 is repeating yourself; this is repeating the reader. What counts as known depends on the audience, so name the audience when writing or reviewing, and cut what the reader would skim past.
21. Decorative verbs: an inanimate subject whose verb is not what actually happens, with no person hidden. The sentence states a property or a mechanical event, and the verb arrived for vividness: "native ids ride in summary rows", "an id earns its place", "media hang identity at different levels". Nothing rides or earns; say what happens: ids appear in rows, an id qualifies, media attach identity. The subject may stay inanimate; the verb must be the plain word for the event. Standard technical vocabulary is not decoration: a span opens with its heading, you walk the tree, recursion bottoms out, a cache goes stale. Those are the words a maintainer says at a whiteboard, and the test is exactly that: would you say this verb at the whiteboard, or did it arrive for texture? The banned "land" and "shape" entries below are instances of this tell.
22. Explanation colons: a colon gluing an assertion to its explanation, both halves full clauses ("the address layer has no semantic gaps: every failure is a verification failure"). A colon is for introducing a list, an example, or a definition. An explanation is a sentence, so give it a period. (Tell 2 is the label form of this, where the left half is a stub rather than a clause.) These accumulate one defensible instance at a time in dense technical prose, until every sentence has the same claim-colon-reason shape.
23. Undefined jargon: tell 20's twin, in the other direction. Tell 20 repeats what the audience knows; this assumes what it doesn't. A term of art dropped without definition ("consistent with the glidepath", or "carrier" in a design doc) loses the reader from that sentence on. The tell covers locally-invented terms only: a project's own coinages and internal vocabulary ("carrier", "wisp", a codename). Established external terms of art (CFRunLoop, kqueue, TCC, monad) are not violations, however specialized, because the audience can look them up; a coinage cannot be looked up anywhere. The two tells are one audience judgment. Name the audience, cut what they know, and define what they don't at first use, or use a plain word instead. Needed jargon is fine; unexplained jargon is not.

24. Appraisal preamble: a clause that appraises the content it introduces instead of delivering it: "the reason is worth being precise about", "here's the key point", "what's interesting is", "crucially". The subject is a discourse object ("the reason", "the point", "the distinction") carrying an appraisal ("worth", "key", "important") and no domain content. Tell 2 announces with a label; this advertises with a compliment, usually mid-paragraph, dressed as emphasis. Deliver content, never advertise it.
25. Category-then-unpack: an abstract category phrase, a colon, then a parallel list unpacking it ("it should see what you have been doing: the cells you ran, what they printed, the plots you drew, the errors you hit"). It is tell 14 inside one sentence, said once vaguely and once itemized, with the items in tell 10's parallel cadence. Enumerate directly as the sentence's own object ("it should see the cells you ran and what they printed"), or name the category and trust it ("it should see your session so far"). A colon-introduced list is fine when the lead-in genuinely needs the items to be understood; it's the tell when the lead-in is a dummy the list then restates.

Tells 9 and 19 are two faces of one device linguists call agent defocusing: grammar that pushes the true actor out of the subject seat (the passive is the third face). The positive rule is Williams's characters-and-actions principle: make the doer the subject and the deed the verb. A tool subject with a mechanical verb ("the parser rejects malformed input") is not defocusing; the tool really is that event's actor, though its verb must still pass tell 21. The tell fires when a person's deed is narrated with the person missing. Tell 21 is the neighbor rather than another face. There, no person exists, and the verb rather than the subject seat is what goes wrong.

Tells 1, 2, 11, 13, and 24, along with tell 5's noting fillers, are all metadiscourse: text about the text rather than about the subject. Openers advertise the piece, labels advertise the fact, pivots advertise excitement, closers advertise closure, preambles advertise importance. Signposting earns its place at document scale (a table of contents, an abstract), the same boundary tell 14 draws for summaries.

When a new tell is added to this skill, add a marked instance to the sloppy passage too, where a one-paragraph sample can show it.

## Banned Words

These are statistically overrepresented in AI output. Replace or delete on sight:

- **Kill on sight:** delve, utilize, leverage (verb), facilitate, elucidate, embark, endeavor, encompass, multifaceted, tapestry, "a testament to", paradigm, synergy, holistic, catalyze, juxtapose, nuanced (as filler), realm, landscape (metaphorical), shape/shaped (as loose jargon for structure or influence: "same shape", "the shape of the data/API/process", "your tests shaped ours"; fine as an actual geometric term, or literally referring to array/tensor dimensions; for influence say what actually happened: adapted, copied, informed), myriad, plethora, minted (metaphorical, e.g. "minted fresh ids"), land/landed/lands (metaphorical, and overused generally: "landed on main", "the fix landed", "a note lands in the output"; things do not land, so say what happened: merged, committed, pushed, released, added to the output, appears), -bearing suffixes such as load-bearing and text-bearing
- **Suspicious in clusters** (remove most of them): robust, comprehensive, seamless, cutting-edge, innovative, streamline, empower, foster, enhance, elevate, optimize, pivotal, intricate, profound, resonate, underscore, harness, navigate (metaphorical), cultivate, bolster, cornerstone, game-changer, invariant (usually "rule" or "guarantee"; keep only when nothing plainer is accurate)
- **Replacements are almost always simpler words:** utilize->use, leverage->use, facilitate->help, robust->strong, comprehensive->complete, seamless->smooth, empower->let/help, foster->encourage, enhance->improve, optimize->improve.

The word lists above are examples of a general rule: always reach for the simplest, most normal, least jargony word that is still correct. If a plainer word says the same thing, use it.

Much of the clarity core above is also codified in ASD-STE100: one idea per sentence, active voice with the doer as subject, one meaning per term, and plain words over inflated ones (utilize->use is a literal STE substitution). Do not adopt its register. STE is deliberately voiceless and choppy, built for non-native mechanics under time pressure, and it would fail the standard the Economist passage sets. Borrow the discipline, not the sound.

Don't hard-wrap prose. Write each paragraph as one continuous line and let the display soft-wrap it. Manual line breaks mid-paragraph make the text painful to reflow, edit, and copy.

In technical prose, put code symbols in backticks: function names, parameters, file paths, module and package names (PyPI distributions included, e.g. `fastcore`, `toolslm`), and literal syntax (`to_html`, `{=html}`).

## What Good Prose Sounds Like

Good writing has a voice. You read it and someone is there. They have opinions. They're occasionally wrong. They'll make a joke in the middle of a technical explanation and it works.

The sentences aren't all the same length. Most are short. An occasional longer one earns its length by carrying a single connected thought too big to split. That variation is what keeps a reader moving. AI can't do it. Every sentence comes out the same mid-length, the same mid-energy.

Say what you mean. "This is broken," not "there may be some areas for potential improvement." Say "use," not "utilize." If you can swap in a different topic and the paragraph still reads fine, you haven't said anything yet. Get specific. Not "improves developer productivity" but "saves me twenty minutes every deploy."

This module also provides `check_prose`, which reviews text against these rules using a separate model. Don't run it unless the user asks for a prose check.
'''

__all__ = ['check_prose']

_CHARTER = """You are a prose checker called as a subagent: your output is parsed by another model, and no human reads it. Praise, hedging, overall verdicts, and commentary on the text's quality therefore serve nobody; emit flags or "Clean" and nothing else. The user message contains prose-style rules, an AUDIENCE line naming the intended readers, then the text to review under "TEXT UNDER REVIEW".
- Sweep per tell: for each numbered tell, scan the ENTIRE text for it before moving to the next. Do not substitute one general pass.
- Report each candidate violation as: the tell name and number, and the offending span quoted verbatim. Also flag banned words, em dashes, and hard-wrapped paragraphs.
- Give extra attention to the two verb tells, 9 and 21: they are the subtlest and the most commonly missed. Question every verb whose subject is an artifact.
- Judge tells 20 and 23 against the stated audience.
- Err on the side of flagging: the caller applies judgment to your flags, so a missed tell costs more than a false positive. When a span merely resembles a tell, flag it and append "borderline".
- Where the fix is not obvious from the flag itself, append a suggested replacement for the quoted span; never rewrite beyond that.
- "Clean" is a valid answer when nothing matches. Never append a verdict to it, and never summarize or soften a flag list."""


async def check_prose(
    text,  # The prose to review
    audience,  # Who the text is for, e.g. "the Answer.AI dev team"; tell 20 is judged against this
    model='sol',  # An `llms.models` short name, or any full 'vendor/model' spec
    effort='medium',  # Reasoning effort where the model supports it: 'low'/'medium'/'high'
):
    "Review `text` against the rules above (this module's docstring) using an agent, returning flagged spans or 'Clean'. Only use if specifically asked to use an agent."
    from .llms import ask
    return await ask(f'# Rules\n\n{__doc__}\n\nAUDIENCE: {audience}\n\n# TEXT UNDER REVIEW\n\n{text}',
        model=model, system=_CHARTER, effort=effort)
