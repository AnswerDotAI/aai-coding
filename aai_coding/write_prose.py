r'''How to write narrative prose that reads as though a person wrote it: read before writing blog posts, essays, announcements, tutorials and explanatory guides, or anything else with the author's voice. write-docs covers reference prose.

# Writing Prose That Doesn't Sound Like AI

Guidelines for narrative prose: blog posts, essays, announcements, talks, tutorials and explanatory guides, and any other writing where the author is present on the page. For reference prose (docstrings, READMEs, API docs, PR descriptions, commit messages, messages to co-workers) use write-docs instead. The same slop is banned there, but the register is voiceless. The standard here is The Economist's.

Here is a passage from The Economist:

> No form of emissions reduction, though, can quickly bend the current trajectory.[1][2] Endurance is what remains.[3][14] Making air conditioning more efficient, cheap and widespread[10] saves lives[6] and fits well with other policy goals, like making clean electricity cheap to produce and consume.[7] Ten years ago a commitment to phase out the fluorinated gases in cooling systems was reached in Kigali, the capital of Rwanda.[8][9] There is scope for extra international efforts to improve the machinery that uses them.[7][19] This could double the cooling benefit of phasing out the gases.[6]

Each sentence sets out to say one thing, says it, and stops. It is simple plain English prose. It carries no byline and needs none. Plainness does the work. It's not trying to sell anything. It lets you figure out what the takeaways are.

Write like that.

Here, on the other hand, is a horrendous rewrite, as sloppy as possible:

> In this piece, we'll dive deep into the fascinating world of cooling![1] 🌡️[15] Here's the thing:[2] emissions reduction alone **isn't going to cut it**. In today's rapidly-warming world,[4] it's not about quick fixes — it's about *endurance*.[3] When it comes to[5] air conditioning, a technology that cools indoor air,[20] one might argue[5] that a comprehensive, holistic approach — making units more efficient, more affordable, and more accessible[10] — could potentially help save countless lives in some cases,[6] while seamlessly aligning with broader policy goals like fostering[7] clean, affordable electricity for all, and also, it's worth noting,[5] building on the pivotal commitment to phase out fluorinated gases that was reached ten years ago in Kigali — the vibrant capital of Rwanda —[16] a commitment that has reshaped the landscape of cooling policy and continues to empower stakeholders[9] across the realm of climate diplomacy.[8]
>
> But here's where it gets really exciting.[11] 🤯 The Kigali deal isn't just a treaty — it's a **game-changer**.[3] Here's what's fascinating:[24] the machinery that leverages[7] these gases gets a myriad of enhancements via this framework,[19] consistent with the glidepath,[23] which could unlock further benefits, and which, honestly,[5] may potentially double the cooling upside of phasing them out, depending on context.[6][8] Getting there is just[12] a matter of commitment. The reason is simple:[22] demand keeps rising, and real progress rides on[21] frameworks like these. Furthermore, as we can see,[5] the journey ahead is a rich tapestry of innovation: the tech we build, the deals we strike, the grids we green[14] — a testament[7] to what we can achieve when we navigate this challenge together. In conclusion:[5] the bottom line?[13] Endurance is the name of the game — in other words, success is all about sticking with it for the long haul.[14] 💪

Do **NOT** write like that.

{markers} The passages are too short to show tells 17, 18, 25 and 26.

1. {throat_clearing}
2. {announce_deliver}
3. {not_x_but_y}
4. {todays_world}
5. Filler phrases. They add zero information. State the thing directly.
    - {noting_fillers}
    - "As we can see..." / "As mentioned earlier..."
    - {filler_transitions}
    - "One might argue that..." / "It could be suggested that..."
    - "A [comprehensive/holistic/nuanced] approach to..." -> "an approach to"
    - "honest"/"honestly"/"to be honest" as a throat-clear ("the honest tradeoff", "honestly, it's fine"): in speech this flags a rare, significant admission. Sprinkled everywhere it's noise. Delete it in nearly every case.
    - "deliberately"/"intentionally"/"carefully"/"thoughtfully": adverbs about the author's mental state rather than the thing. In a design doc every recorded choice is already deliberate, and the explanation that follows does the work. Keep one only when the reader would otherwise suspect an accident and no explanation follows ("the file is deliberately empty").
6. {hedging} Hedging is the worst offender. The original commits: "saves lives", "could double".
7. Inflated diction. Puffed-up words where plain ones exist: enhance/leverage for improve/use, plus seamlessly, fostering, pivotal, myriad, landscape, realm, empower, journey, tapestry, testament, navigate. The banned words lists below are the fuller reference.
8. Sentence sprawl. One over-long sentence stacking clauses, chained with "so", "which", "but", and "and", each extending or qualifying the last. Write one idea per sentence. When a draft sentence joins two thoughts, work out what the reader needs from it and write that, instead of splitting at the join. Keep the join only when the connection itself is the point.
9. {artifact_agent} In the sloppy passage, the commitment "has reshaped the landscape" and "continues to empower". Really, people reached a commitment. In narrative prose this habit often comes stacked with two others, as in "Your tests shaped the ones that landed":
    - Oblique reference instead of naming. The object is pointed at through a relative clause or metaphor ("the ones that landed") instead of being named ("our new tests").
    - Narrative compression into a single transitive clause. A who-did-what story (I read your tests, adapted them, committed mine) is flattened into "X verbed Y". The result sounds polished, like an aphorism, because it discards the actors and the order of events. It is common as a sentence-final flourish.

    Rewrite as the actual events with the actual actors: "I took your tests as inspiration and added some updates based on these changes."
10. {forced_symmetry} The original's list varies its forms.
11. {teaser_pivot} It is a sibling of tell 3.
12. Minimizing "just". Using it as a casual softener ("resets just that kata", "it's just a wrapper", "just works"). Be frugal with it. Usually delete it. When the restriction genuinely matters, "only" is plainer.
13. Rhetorical wrap-up. A rhetorical question as a closing flourish.
14. {restatement} The original says it once, in four words. Everything a lead summary says reappears, with more detail, in the sentences that follow. Delete it and nothing is lost:

    > ~~Failures are visible now too.~~ A startup failure used to print to the server log and leave a half-booted dialog that looked ready. It now raises, the user gets an error toast and a red status dot, and the dialog stays editable.

    The mirror form is the closing sentence that summarizes the paragraph or piece it ends ("LLMs can now use the module with far fewer tokens", ending a paragraph whose second sentence said so). It is the taught essay shape, and the strongest LLM habit of the lot. End on the last fact. The same disease occurs within a sentence ("editing needs no kernel: cards echo through the outbound queue, which is kernel-independent", where the final clause restates the opening). Its listy form puts a category phrase, a colon, then a parallel list unpacking it ("it should see what you have been doing: the cells you ran, what they printed, the plots you drew, the errors you hit"). Cut whichever side of the colon says less. Ask whether deleting the phrase removes any information from the document. If not, delete it. Prefer the shorter phrasing of the same fact: "nothing new needs specifying", not "there is nothing new to learn and nothing new to specify".
15. {decoration} Decorative bold and italics count too. Use them VERY sparingly in the body of a paragraph.
16. {splices} Avoid em dashes entirely. Colons and semicolons should be rare in normal prose.
17. Monotone rhythm. Topic sentence, elaboration, example, wrap-up, paragraph after paragraph. The reader's eyes glaze over. Mix it up. Real writing is lumpy. Some sections run long because they need to. Others are two sentences because that's all there is to say.
18. {false_depth}
19. {recipient_subject} As in tell 9, the actor vanishes. Here the artifact moves from performing the action to receiving it.
20. {explaining_known} Tell 14 is repeating yourself. This is repeating the reader.
21. {decorative_verbs}
22. Explanation colons. A colon gluing an assertion to its explanation, both halves full clauses ("the address layer has no semantic gaps: every failure is a verification failure"). A colon is for introducing a list, an example, or a definition. When the second half explains the first, rebuild the sentence around that relation: "the address layer has no semantic gaps because every failure is a verification failure". (Tell 2 is the label form of this, where the left half is a stub rather than a clause.) These accumulate one defensible instance at a time in dense technical prose, until every sentence has the same claim-colon-reason shape.
23. {undefined_jargon} It is tell 20's twin. Where tell 20 repeats what the audience knows, this tell assumes what it doesn't. The two tells are one audience judgment. {audience_judgment}
24. {appraisal_preamble} Where tell 2 announces with a label, this tell advertises with a compliment. Deliver content, never advertise it.
25. {over_structuring} It is the document-scale form of tell 10's symmetry habit.
26. {consequence_glue}

Tells 9 and 19 are two faces of one device linguists call agent defocusing: grammar that pushes the true actor out of the subject seat (the passive is the third face). The positive rule is Williams's characters-and-actions principle: make the doer the subject and the deed the verb. A tool subject with a mechanical verb ("the parser rejects malformed input") is not defocusing. The tool really is that event's actor, though its verb must still pass tell 21. The tell fires when a person's deed is narrated with the person missing. Tell 21 is the neighbor rather than another face. There, no person exists, and the verb rather than the subject seat is what goes wrong.

Tells 1, 2, 11, 13, and 24, along with tell 5's noting fillers, are all metadiscourse: text about the text rather than about the subject. Openers advertise the piece, labels advertise the fact, pivots advertise excitement, closers advertise closure, preambles advertise importance. Signposting earns its place at document scale (a table of contents, an abstract), the same boundary tell 14 draws for summaries.

{new_tells}

## Banned words

{plain_words}

These are statistically overrepresented in AI output. Replace or delete on sight:

- **Kill on sight:** seamless, streamline, empower, foster, pivotal, delve, utilize, leverage (verb), facilitate, elucidate, embark, endeavor, encompass, multifaceted, tapestry, "a testament to", paradigm, synergy, holistic, catalyze, juxtapose, nuanced (as filler), realm, landscape (metaphorical), navigate (metaphorical), shape/shaped (as loose jargon), myriad, plethora, minted (metaphorical, e.g. "minted fresh ids"), land/landed/lands (metaphorical), -bearing suffixes such as load-bearing and text-bearing
- **Suspicious in clusters** (remove most of them): robust, comprehensive, cutting-edge, innovative, enhance, elevate, optimize, intricate, profound, resonate, underscore, harness, cultivate, bolster, cornerstone, game-changer, invariant

{hidden_words}

Much of the clarity core above is also codified in ASD-STE100: one idea per sentence, active voice with the doer as subject, one meaning per term, and plain words over inflated ones (utilize->use is a literal STE substitution). Do not adopt its register. STE is voiceless and choppy by design, built for non-native mechanics under time pressure, and it would fail the standard the Economist passage sets. Borrow the discipline, not the sound. That sound is correct in reference prose. write-docs covers that register.

{formatting}

## What good prose sounds like

Good writing has a voice. You read it and someone is there. They have opinions. They're occasionally wrong. They'll make a joke in the middle of a technical explanation and it works.

The sentences aren't all the same length. Most are short. An occasional longer one earns its length by carrying a single connected thought too big to split. That variation is what keeps a reader moving. AI can't do it. Every sentence comes out the same mid-length, the same mid-energy.

Say what you mean. "This is broken," not "there may be some areas for potential improvement." Say "use," not "utilize." If you can swap in a different topic and the paragraph still reads fine, you haven't said anything yet. Get specific. Not "improves developer productivity" but "saves me twenty minutes every deploy."

This module also provides `check_prose`. It sends text and these rules to a separate model for review. Do not run it unless the user asks for a prose check.
'''

from ._writing import fill, charter
__doc__ = fill(__doc__)

__all__ = ['check_prose']

_CHARTER = charter('prose', '9 and 21', 'tells 20 and 23')


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
