r'''How to write narrative prose that reads as though a person wrote it: read before writing messages to users or colleagues, blog posts, essays, announcements, tutorials and explanatory guides, or anything else with the author's voice. write-docs covers reference prose.

# Writing Prose That Doesn't Sound Like AI

Standard for narrative prose, talks, user/colleague messages: The Economist. Reference prose: `write_docs`.

Good:

> No form of emissions reduction, though, can quickly bend the current trajectory.[1][2] Endurance is what remains.[3][12] Making air conditioning more efficient, cheap and widespread[9] saves lives[5] and fits well with other policy goals, like making clean electricity cheap to produce and consume.[6] Ten years ago a commitment to phase out the fluorinated gases in cooling systems was reached in Kigali, the capital of Rwanda.[7][8] There is scope for extra international efforts to improve the machinery that uses them.[6][8] This could double the cooling benefit of phasing out the gases.[5]

Bad:

> In this piece, we'll dive deep into the fascinating world of cooling![1] 🌡️[13] Here's the thing:[2] emissions reduction alone **isn't going to cut it**. In today's rapidly-warming world,[1] it's not about quick fixes — it's about *endurance*.[3] When it comes to[4] air conditioning, a technology that cools indoor air,[16] one might argue[4] that a comprehensive, holistic approach — making units more efficient, more affordable, and more accessible[9] — could potentially help save countless lives in some cases,[5] while seamlessly aligning with broader policy goals like fostering[6] clean, affordable electricity for all, and also, it's worth noting,[4] building on the pivotal commitment to phase out fluorinated gases that was reached ten years ago in Kigali — the vibrant capital of Rwanda —[7] a commitment that has reshaped the landscape of cooling policy and continues to empower stakeholders[8] across the realm of climate diplomacy.[7]
>
> But here's where it gets really exciting.[2] 🤯 The Kigali deal isn't just a treaty — it's a **game-changer**.[3] Here's what's fascinating:[2] the machinery that leverages[6] these gases gets a myriad of enhancements via this framework,[8] consistent with the glidepath,[16] which could unlock further benefits, and which, honestly,[4] may potentially double the cooling upside of phasing them out, depending on context.[5][7] Getting there is just[10] a matter of commitment. The reason is simple:[7] demand keeps rising, and real progress rides on[17] frameworks like these. Furthermore, as we can see,[4] the journey ahead is a rich tapestry of innovation: the tech we build, the deals we strike, the grids we green[12] — a testament[6] to what we can achieve when we navigate this challenge together. In conclusion:[4] the bottom line?[11] Endurance is the name of the game — in other words, success is all about sticking with it for the long haul.[12] 💪

{markers} Unshown: 14, 15.

1. {throat_clearing}
2. {advertising}
3. {not_x_but_y}
4. {filler} Also cut "As we can see/mentioned earlier"; "One might argue"; "A [comprehensive/holistic/nuanced] approach"->"an approach"; "honest/honestly/to be honest" (nearly always); "deliberately/intentionally/carefully/thoughtfully" (keep only if accident would be suspected, e.g. "deliberately empty").
5. {hedging} Worst offender.
6. Inflated diction: puffed-up words (see Banned).
7. {tacked_on} No em dashes; `;`/`:` rare. Avoid `so/which/but/and` sprawl (join only when connection is the point) and explanation colons joining 2 clauses ("no gaps: every failure..."->"...because...").
8. {agent_defocusing} Pairs with oblique ref ("ones that landed" vs "our new tests") and narrative compression ("Your tests shaped...")->actors/events.
9. {symmetry}
10. Minimizing "just": softener ("just a wrapper/works"). Usually delete; "only" for real restriction.
11. Rhetorical wrap-up: closing question.
12. {restatement} Cut lead summaries, closing recaps (strongest LLM habit; end on last fact), intra-sentence echoes, label+list duplicates (cut weaker side of `:`).
13. {decoration} Body bold/italics: VERY sparingly.
14. Monotone rhythm: topic/elaboration/example/wrap-up loop. Vary length; real writing is lumpy.
15. {false_depth}
16. {audience}
17. {decorative_verbs}

Agent defocusing (8, passive): doer=subject, deed=verb for a person's deed ("parser rejects malformed input" hides no person; check 17). Metadiscourse (1, 2, 11, 4 noting): doc scale only (TOC/abstract), like 12. {new_tells}

## Banned words

{plain_words}
{banned_words}
Clusters: cutting-edge, innovative, elevate, intricate, profound, resonate, underscore, harness, cultivate, bolster, cornerstone, game-changer.
{hidden_words}
ASD-STE100: active voice, doer=subject, 1 meaning/term, plain words.

{formatting}

## Voice and messages

- Voice: opinions, occasional humor; mostly short sentences, occasional earned longer one (AI writes uniform mid-length/energy); specific ("This is broken", "saves 20 min/deploy", not "improves productivity"; cut topic-swappable paras).
- Messages: answer/change first, support after; no softening opener or "happy to help" closer; "I" sparingly for main change/choice ("I added/changed/decided"), not every sentence; direct UI actions ("Clicking `Chat` opens...", not "Chat mode scopes..."); plain UI names ("status circle at top", "unique folders", not "header readiness indicator", "deduplicated parent folders"); no `, and` stacks (7).

`check_prose` checks text via separate model; run only if asked.
'''

from ._writing import fill, charter
__doc__ = fill(__doc__)

__all__ = ['check_prose']

_CHARTER = charter('prose', '8 and 17', 'tell 16')


async def check_prose(
    text,  # The prose to review
    audience,  # Who the text is for, e.g. "the Answer.AI dev team"; tell 16 is judged against this
    model='sol',  # An `llms.models` short name, or any full 'vendor/model' spec
    effort='medium',  # Reasoning effort where the model supports it: 'low'/'medium'/'high'
):
    "Review `text` against the rules above (this module's docstring) using an agent, returning flagged spans or 'Clean'. Only use if specifically asked to use an agent."
    from .llms import ask
    return await ask(f'# Rules\n\n{__doc__}\n\nAUDIENCE: {audience}\n\n# TEXT UNDER REVIEW\n\n{text}',
        model=model, system=_CHARTER, effort=effort)
