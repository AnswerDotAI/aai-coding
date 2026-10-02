r"""How to write summaries that stand alone: read before summarizing a conversation, meeting, PR, paper, or repo change for a human reader.

# Writing Summaries That Stand Alone

Use these guidelines to summarize any long source: a meeting transcript, a chat thread, a review discussion, a diff or a paper. The summary is the only thing the reader will read. Use write-docs for its sentences and this skill for what they say.

A source records what was said, in the order it was said. The reader wants to know what is now true: what was decided, what is still open, who is doing what and why. A good summarizer builds a picture of the situation from the source and writes from that picture. A bad one shortens the source.

Here is a passage from the minutes of a Federal Open Market Committee meeting. The minutes compress a day of committee discussion into a few pages. They set the standard a summary here should default to:

> The manager turned first to an overview of broad market developments during the intermeeting period.[1] Respondents to the Open Market Desk Survey of Market Expectations (Desk survey) continued to see the economy as resilient[4] and again marked up their forecasts for real gross domestic product (GDP) growth in 2026, while their expectations for headline personal consumption expenditures (PCE) inflation and the unemployment rate were little changed. Market- and survey-based policy rate expectations were likewise little changed. Market-based measures of policy rate expectations indicated one to two 25 basis point rate cuts this year, and the median modal path of the federal funds rate, as given in the Desk survey, continued to indicate expectations of two 25 basis point rate cuts this year.
>
> The manager turned next to Treasury market developments and market-based measures of inflation compensation. Shorter-term Treasury yields were little changed, while longer-term yields rose a few basis points on net; the Treasury curve steepened slightly as a result. Near-term inflation compensation continued to decline amid lower-than-expected consumer price index (CPI) readings, lower energy prices, and lower-than-anticipated pass-through of tariffs to customers; forward rates suggested that near-term inflation would stabilize close to current levels for the rest of the year. Model-based measures of short-term inflation expectations also declined some over the intermeeting period, with forward rates suggesting further modest declines over the course of this year. The Treasury market continued to function well amid low volatility. In light of the growing portion of Treasury securities that is financed using repos, the manager noted the importance of the stability of the repo market for the continued smooth functioning of the Treasury market.[5]
>
> The recent announcement that Fannie Mae and Freddie Mac may increase their mortgage investment portfolios[8] garnered substantial market attention and was followed by a notable decline in mortgage-backed securities yields relative to those on comparable-maturity Treasury yields.[9] Still, the manager observed that the decline was unlikely to result in a material increase in mortgage refinancing because current mortgage rates are well above the weighted average rate of outstanding mortgages.[6]

Every claim in it has an owner. Survey respondents see the economy as resilient. Market-based measures indicated one to two rate cuts. The manager noted the importance of repo stability. The last paragraph reports an event, the market's reaction and the manager's judgment, with the reason for that judgment attached. Refinancing is unlikely to rise because current mortgage rates sit well above the average rate on outstanding mortgages. No one stated that reason aloud in the meeting. The writer added it so that the passage would stand on its own.

Write like that.

Here is the same briefing, summarized the way summaries usually fail:

> The manager's briefing covered a range of topics, including survey results, Treasury market developments, and a recent announcement.[2] The briefing opened with the Desk survey.[1] Overall, the economy is seen as resilient, and growth forecasts were marked up again,[4] while expectations for inflation and unemployment were little changed. A considerable portion of the discussion concerned the survey itself, with an extended exchange about response rates and whether the questions on rate expectations should be reworded; participants explored several possibilities and the topic generated substantial engagement before the group moved on.[7]
>
> The briefing then turned to Treasury markets.[1] Shorter-term yields were little changed while longer-term yields rose somewhat, and near-term inflation compensation continued to decline, which was attributed to a number of factors.[4] Model-based measures moved in a manner consistent with the drivers mentioned earlier.[3] The question was raised of whether the repo market posed any risk to Treasury market functioning.[5] Attention then shifted to the recent announcement,[8] which had attracted considerable market interest; the resulting yield moves were viewed by some as significant,[4] although refinancing is not expected to increase materially.[6]
>
> Toward the end of the briefing,[1] it was noted that the announcement in question was that Fannie Mae and Freddie Mac may increase their mortgage investment portfolios, news which had been followed by a notable decline in mortgage-backed securities yields relative to comparable-maturity Treasuries.[9]

Do NOT summarize like that. Its prose is mostly clean, with no banned words and short sentences. Nothing in it would trip write-docs. A summary can pass every sentence-level rule and still fail completely. This one fails because of what it chose to say.

The numbers below refer to the [bracketed] markers in both passages. Where a number appears in each, the two markers show the failing and the working version of the same thing. Tell 7 has no marker in the minutes because its working version is an absence. The real minutes give the methodology chatter no space at all.

1. Walking the source: the summary follows the source's own order, turn by turn through a conversation, file by file through a diff, section by section through a paper. Order by subject instead. A spine of subjects is fine. The minutes have one, since "turned first to" follows the briefing's agenda. What fails is the clock. "The briefing opened with" and "toward the end of the briefing" record when things were said. The reader never needed to know that.

2. Topics without content: "we discussed the migration", "this PR refactors the auth module", "the paper explores tradeoffs in caching". Each names what the source is about and shares nothing it says. A sentence you could have written before reading the source tells the reader nothing about it. Cash every topic out in specifics or drop it.

3. Pointers to nowhere: a reference that resolved during the conversation resolves to nothing in the summary. "The approach discussed earlier", "the second reviewer's concern", "the drivers mentioned earlier" and "see Section 3" all do this. Name the thing instead. Every reference must resolve inside the summary itself.

4. Claims with no owner: the reader cannot tell whether a statement is a fact, someone's position, or the summarizer's own guess. "The economy is seen as resilient" leaves the reader asking who sees it. In the minutes, survey respondents do. For a paper, the three cases are the authors' finding, a work they cite, and the summarizer's opinion. For a PR, they are what the code does, what the description promises, and what a reviewer suspects. Vague hedges are the same failure. "Some concerns were raised" hides both who raised them and which concerns they were. Give every claim its owner. Mark your own inferences as yours.

5. No status: a thread is reported but its current state is not. The missing state might be decided, dropped or still open. For a PR it might be merged, blocked or awaiting review. A task with nobody named as doing it has the same gap. "The question was raised" is this tell. The reader never learns what became of the question. The minutes commit to an outcome, in which the manager noted that repo stability matters. When the source left something open, say it is open. An honest "undecided" is status too.

6. The why dropped: the conclusion survives but its reason does not. "Refinancing is not expected to increase materially" keeps the what and loses the why. The minutes keep both. Their reason is that current mortgage rates sit well above the average rate on outstanding mortgages. With the reason in hand, the reader can check the logic and notice when it stops applying. Reasons are scattered through every source: across turns in a conversation, across review comments in a PR, across the introduction and discussion of a paper. Gathering them is most of the work of summarizing. That is why lazy summaries lose them first.

7. Space by bulk: space in the summary tracks the size of the source material instead of how much it matters. The twenty-minute methodology digression that changed nothing gets the longest stretch. The two-line exchange that changed everything gets half a clause. In a PR summary, the thousand-line mechanical rename dominates while the one-line behavior change hides at the bottom. Weight each item by how much it changed the situation.

8. Assumes you read it: the summary only makes sense next to the source. "The recent announcement" means something only to a reader who already knows what happened that week. The reader may never open the source. Even one who did has probably forgotten it. A summary must still work a week later with the source gone. Standing alone means naming what the source introduced. It does not mean reciting background the reader already holds.

9. Buried lede: the biggest change arrives in the final sentence because that is where the source got to it. The minutes' paragraph on the announcement leads with the announcement and its market reaction. Put the largest change first, where the reader cannot miss it.

The tells fall into three families. In tells 1-3, the summarizer writes from the source instead of from what the source describes. In tells 4-7, the picture reaches the reader with a piece missing: its owners, its status, its reasons or its proportions. Tells 8 and 9 come from a wrong guess about what the reader already holds.

The first family has fifty years of science behind it. Kintsch and van Dijk (1978) showed that readers build the gist of a text with three operations: delete what does not matter, generalize lists into a covering statement, and construct statements that were never in the text. Memory then converges on that gist as details fade. This is one of the most replicated results in the field.

Brown and Day (1983) found that novice summarizers use only the first operation. They called the result copy-delete: run through the source in order, keep or drop each bit, and copy the kept bits in roughly their original words. That is tell 1. It is every summarizer's default, human or LLM. The operations that make a summary worth reading are the hard ones. In Brown and Day's data, even college students usually failed to construct a covering statement where the source lacked one. The mortgage paragraph in the minutes is that hard move done well. The because-clause appears in no transcript. The writer constructed it.

Van Dijk and Kintsch's later work explains the other two families. What a reader keeps from a text is a model of the situation it describes, built by joining the text to what the reader already knows. The exact words fade within minutes, the sentences within days (van Dijk and Kintsch, 1983). A transcript holds no such model. The situation lived in the participants' heads. That is why raw transcripts are so much work to read. The summarizer's job is to rebuild the situation from the source and write from it: what is true, who wants what and why, what is decided and what is open.

The reader already holds a situation model of their own: the project, the people, the running argument. A summary is an update to that model, not a description for a stranger. Each tell is a way the update fails to apply. The reader can't trust a claim with no owner or follow a pointer to nowhere. Background they already hold updates nothing.

Before sending, read the draft once against the four dimensions the summarization-evaluation literature settled on (SummEval; Fabbri et al., 2021):

- Relevance: the summary picks what matters.
- Consistency: every statement is supported by the source, or marked as the summarizer's own.
- Coherence: the summary reads as one situation rather than a pile of fragments.
- Fluency: write-docs covers it.

Most tells are one of these dimensions failing in a specific way. Relevance suffers in tells 2, 6 and 7, consistency in tells 4 and 5, coherence in tells 1, 3 and 9.

The literature has no dimension for the reader. No score asks whether a summary stands alone, because evaluators judge it with the source open beside it. That protocol cannot see tell 8. Check for it separately.

Copy the minutes' discipline, not their register. Take their habits: an owner for every claim, a reason with every judgment, context wherever the reader needs it to make sense of an event. Leave the committee-speak. "Garnered substantial market attention" survives in the Fed's pages because institutions write that way. A summary for a colleague has no such requirement. write-docs' rules on plain words apply to summaries too.

Leave the anonymization as well. The minutes say "the manager" and "a few participants" because committee politics require it. Your reader wants names. Who holds a position is half the information. "Sam wants the migration delayed until the index rebuild ships" updates the reader's picture. "Concerns were raised about timing" does not.

When you add a new tell to this skill, add a marked instance of it to the sloppy passage. Where a paired good version exists, add a marker to the minutes passage too.
"""
