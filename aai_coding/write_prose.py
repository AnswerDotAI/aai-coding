r'''How to write narrative prose that reads as though a person wrote it: read before writing blog posts, essays, announcements, tutorials and explanatory guides, or anything else with the author's voice. write-docs covers reference prose.

# Writing Prose That Doesn't Sound Like AI

The standard for narrative prose, including talks, is The Economist's. For voiceless reference prose (docstrings, READMEs, API docs, PR descriptions, commit messages, messages to co-workers), use write-docs. Both ban the same slop.

Here is a passage from The Economist:

> No form of emissions reduction, though, can quickly bend the current trajectory.[1][2] Endurance is what remains.[3][14] Making air conditioning more efficient, cheap and widespread[10] saves lives[6] and fits well with other policy goals, like making clean electricity cheap to produce and consume.[7] Ten years ago a commitment to phase out the fluorinated gases in cooling systems was reached in Kigali, the capital of Rwanda.[8][9] There is scope for extra international efforts to improve the machinery that uses them.[7][19] This could double the cooling benefit of phasing out the gases.[6]

Each sentence says one thing in plain English and stops. It carries no byline and needs none. Plainness does the work without selling anything or telling readers what to take away.

Write like that.

Here is the same passage rewritten as sloppily as possible:

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
8. Sentence sprawl. One over-long sentence stacking clauses, chained with "so", "which", "but", and "and", each extending or qualifying the last. Splitting it does not fix it. Work out what the reader needs, then write that from scratch. Keep a join only when the connection itself is the point.
9. {artifact_agent} In the sloppy passage, the commitment "has reshaped the landscape" and "continues to empower". Really, people reached a commitment. In narrative prose, "Your tests shaped the ones that landed" often combines this habit with two others:
    - Oblique reference instead of naming. A relative clause or metaphor ("the ones that landed") points at the object instead of naming it ("our new tests").
    - Narrative compression into a single transitive clause. Compressing the story (I read your tests, adapted them, committed mine) into "X verbed Y" discards actors and event order. That gives it an aphorism's polish, often as a sentence-final flourish.

    Rewrite as the actual events with the actual actors: "I took your tests as inspiration and added some updates based on these changes."
10. {forced_symmetry} The original's list varies its forms.
11. {teaser_pivot} It is a sibling of tell 3.
12. Minimizing "just". Using it as a casual softener ("resets just that kata", "it's just a wrapper", "just works"). Be frugal with it. Usually delete it. When the restriction genuinely matters, "only" is plainer.
13. Rhetorical wrap-up. A rhetorical question as a closing flourish.
14. {restatement} The original says it once, in four words. A lead summary repeats facts the following sentences give in more detail. Delete it and nothing is lost:

    > ~~Failures are visible now too.~~ A startup failure used to print to the server log and leave a half-booted dialog that looked ready. It now raises, the user gets an error toast and a red status dot, and the dialog stays editable.

    A closing sentence can repeat its paragraph or piece: "LLMs can now use the module with far fewer tokens" repeats that paragraph's second sentence. This taught essay shape is the strongest LLM habit of the lot. End on the last fact. Within a sentence, "editing needs no kernel: cards echo through the outbound queue, which is kernel-independent" repeats its opening in the final clause. The list form names a category then unpacks it in a parallel list: "it should see what you have been doing: the cells you ran, what they printed, the plots you drew, the errors you hit". Cut whichever side of the colon says less. If deleting a phrase removes no information from the document, delete it. Prefer "nothing new needs specifying" to "there is nothing new to learn and nothing new to specify".
15. {decoration} Decorative bold and italics count too. Use them VERY sparingly in the body of a paragraph.
16. {tacked_on} Avoid em dashes entirely. Colons and semicolons should be rare in normal prose.
17. Monotone rhythm. Repeating topic sentence, elaboration, example, wrap-up makes readers glaze over. Mix it up. Real writing is lumpy. Some sections need length. Others need only two sentences.
18. {false_depth}
19. {recipient_subject} As in tell 9, the actor vanishes. Here the artifact moves from performing the action to receiving it.
20. {explaining_known} Tell 14 is repeating yourself. This is repeating the reader.
21. {decorative_verbs}
22. Explanation colons. A colon joins an assertion to its explanation as two full clauses ("the address layer has no semantic gaps: every failure is a verification failure"). A colon is for introducing a list, an example, or a definition. Rebuild an explanation around that relation: "the address layer has no semantic gaps because every failure is a verification failure". Tell 2's label form has a stub on the left, not a clause. In dense technical prose, individually defensible instances accumulate until every sentence has the same claim-colon-reason pattern.
23. {undefined_jargon} Tell 20 repeats what the audience knows. This tell assumes what it doesn't. Both are one audience judgment. {audience_judgment}
24. {appraisal_preamble} Where tell 2 announces with a label, this tell advertises with a compliment. Deliver content, never advertise it.
25. {over_structuring} It is the document-scale form of tell 10's symmetry habit.
26. {consequence_glue}

Tells 9 and 19 are two forms of what linguists call agent defocusing, as is the passive: grammar pushes the true actor out of the subject position. Williams's characters-and-actions principle says to make the doer the subject and the deed the verb. The tell fires when a person's deed is narrated with the person missing. A tool really performs the event in "the parser rejects malformed input". Its mechanical verb must still pass tell 21, but it isn't hiding a person's deed. Tell 21 concerns the verb, with no person to be hidden.

Tells 1, 2, 11, 13 and 24, and tell 5's noting fillers, are metadiscourse: text about the text rather than its subject. Openers advertise the piece, labels the fact, pivots excitement, closers closure, preambles importance. Signposting earns its place at document scale (a table of contents, an abstract), the same boundary tell 14 draws for summaries.

{new_tells}

## Banned words

{plain_words}

{banned_words}

Remove most of these when they cluster: cutting-edge, innovative, elevate, intricate, profound, resonate, underscore, harness, cultivate, bolster, cornerstone, game-changer.

{hidden_words}

ASD-STE100 codifies active voice with the doer as subject, one meaning per term, and plain words over inflated ones (utilize->use is a literal STE substitution).

{formatting}

## What good prose sounds like

Good writing has a voice. You hear someone with opinions, someone occasionally wrong who can make a joke work in a technical explanation.

Most sentences are short. An occasional longer one earns its length with a single connected thought too big to split. Variation keeps readers moving. AI can't do it. AI writes the same mid-length, mid-energy sentence.

Say what you mean. "This is broken," not "there may be some areas for potential improvement." A paragraph that still reads fine after swapping in a different topic says nothing. Get specific. Not "improves developer productivity" but "saves me twenty minutes every deploy."

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
