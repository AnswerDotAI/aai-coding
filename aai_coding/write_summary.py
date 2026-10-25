r"""How to write summaries that stand alone: read before summarizing a conversation, meeting, PR, paper, or repo change for a human reader.

# Writing Summaries That Stand Alone

Use these guidelines for any long source: a meeting transcript, chat thread, review discussion, diff or paper. The summary is the only thing the reader will read. Use write-docs for its sentences and this skill for its content.

A source records what was said and in what order. Build a picture of the situation from it, then write what is now true: what was decided, what is open, who is doing what and why. Merely shortening the source does not do that.

Here is a passage from the minutes of a Federal Open Market Committee meeting. The minutes compress a day of committee discussion into a few pages. They set the standard a summary here should default to:

> The manager turned first to an overview of broad market developments during the intermeeting period.[1] Respondents to the Open Market Desk Survey of Market Expectations (Desk survey) continued to see the economy as resilient[4] and again marked up their forecasts for real gross domestic product (GDP) growth in 2026, while their expectations for headline personal consumption expenditures (PCE) inflation and the unemployment rate were little changed. Market- and survey-based policy rate expectations were likewise little changed. Market-based measures of policy rate expectations indicated one to two 25 basis point rate cuts this year, and the median modal path of the federal funds rate, as given in the Desk survey, continued to indicate expectations of two 25 basis point rate cuts this year.
>
> The manager turned next to Treasury market developments and market-based measures of inflation compensation. Shorter-term Treasury yields were little changed, while longer-term yields rose a few basis points on net; the Treasury curve steepened slightly as a result. Near-term inflation compensation continued to decline amid lower-than-expected consumer price index (CPI) readings, lower energy prices, and lower-than-anticipated pass-through of tariffs to customers; forward rates suggested that near-term inflation would stabilize close to current levels for the rest of the year. Model-based measures of short-term inflation expectations also declined some over the intermeeting period, with forward rates suggesting further modest declines over the course of this year. The Treasury market continued to function well amid low volatility. In light of the growing portion of Treasury securities that is financed using repos, the manager noted the importance of the stability of the repo market for the continued smooth functioning of the Treasury market.[5]
>
> The recent announcement that Fannie Mae and Freddie Mac may increase their mortgage investment portfolios[8] garnered substantial market attention and was followed by a notable decline in mortgage-backed securities yields relative to those on comparable-maturity Treasury yields.[9] Still, the manager observed that the decline was unlikely to result in a material increase in mortgage refinancing because current mortgage rates are well above the weighted average rate of outstanding mortgages.[6]

Every claim has an owner. Survey respondents see the economy as resilient. Market-based measures indicate one to two cuts. The manager notes the importance of repo stability. The last paragraph gives the event, market reaction, manager's judgment and its reason. Current mortgage rates sit well above the average rate on outstanding mortgages, making refinancing unlikely to rise. Nobody stated that reason aloud in the meeting. The writer added it to make the passage stand alone.

Write like that.

Here is the same briefing, summarized the way summaries usually fail:

> The manager's briefing covered a range of topics, including survey results, Treasury market developments, and a recent announcement.[2] The briefing opened with the Desk survey.[1] Overall, the economy is seen as resilient, and growth forecasts were marked up again,[4] while expectations for inflation and unemployment were little changed. A considerable portion of the discussion concerned the survey itself, with an extended exchange about response rates and whether the questions on rate expectations should be reworded; participants explored several possibilities and the topic generated substantial engagement before the group moved on.[7]
>
> The briefing then turned to Treasury markets.[1] Shorter-term yields were little changed while longer-term yields rose somewhat, and near-term inflation compensation continued to decline, which was attributed to a number of factors.[4] Model-based measures moved in a manner consistent with the drivers mentioned earlier.[3] The question was raised of whether the repo market posed any risk to Treasury market functioning.[5] Attention then shifted to the recent announcement,[8] which had attracted considerable market interest; the resulting yield moves were viewed by some as significant,[4] although refinancing is not expected to increase materially.[6]
>
> Toward the end of the briefing,[1] it was noted that the announcement in question was that Fannie Mae and Freddie Mac may increase their mortgage investment portfolios, news which had been followed by a notable decline in mortgage-backed securities yields relative to comparable-maturity Treasuries.[9]

Do NOT summarize like that. Its mostly clean prose, short sentences and lack of banned words would pass write-docs. A summary can pass every sentence-level rule and still fail completely through its choice of content.

The numbers below match the [bracketed] markers in both passages. Paired markers show failing and working versions of the same thing. Tell 7 has no good-sample marker: omitting the twenty-minute methodology discussion is the fix. The real minutes never mention it.

1. Walking the source: following its order, turn by turn through a conversation, file by file through a diff, section by section through a paper. Order by subject, not by when things were said. The minutes' "turned first to" follows the briefing's agenda, a valid spine of subjects. "The briefing opened with" and "toward the end of the briefing" instead record timing the reader never needed.

2. Topics without content: "we discussed the migration", "this PR refactors the auth module", "the paper explores tradeoffs in caching". Each names what the source is about and shares nothing it says. A sentence you could have written before reading the source tells the reader nothing about it. Cash every topic out in specifics or drop it.

3. Pointers to nowhere: a reference that resolved during the conversation resolves to nothing in the summary. "The approach discussed earlier", "the second reviewer's concern", "the drivers mentioned earlier" and "see Section 3" all do this. Name the thing instead. Every reference must resolve inside the summary itself.

4. Claims with no owner: fact, someone's position and the summarizer's guess become indistinguishable. "The economy is seen as resilient" hides who sees it. The minutes name survey respondents. For a paper, the cases are the authors' finding, work they cite and the summarizer's opinion. For a PR, they are what code does, what its description promises and what a reviewer suspects. Vague hedges fail too: "Some concerns were raised" hides both who raised them and which concerns. Give every claim its owner. Mark your own inferences as yours.

5. No status: reporting a thread without its current state (decided, dropped, open; for a PR, merged, blocked, awaiting review). A task with nobody named as doing it has the same gap. "The question was raised" says nothing about the outcome. The minutes commit to one: the manager noted that repo stability matters. When the source left something open, say it is open. An honest "undecided" is status too.

6. The why dropped: a conclusion survives without its reason. "Refinancing is not expected to increase materially" loses the reason retained in the minutes: current mortgage rates sit well above the average rate on outstanding mortgages. Reasons let readers check the logic and notice when it stops applying. They are scattered across conversation turns, PR review comments, and a paper's introduction and discussion. Lazy summaries lose reasons first because gathering them is most of the work of summarizing.

7. Space by bulk: space in the summary tracks the size of the source material instead of how much it matters. The twenty-minute methodology digression that changed nothing gets the longest stretch. The two-line exchange that changed everything gets half a clause. In a PR summary, the thousand-line mechanical rename dominates while the one-line behavior change hides at the bottom. Weight each item by how much it changed the situation.

8. Assumes you read it: the summary needs its source beside it. "The recent announcement" works only for readers who know what happened that week. Readers may never open the source. Even one who did has probably forgotten it. A summary must still work a week later with the source gone. Standing alone means naming what the source introduced, not reciting background the reader already holds.

9. Buried lede: the biggest change comes last because the source reached it last. The minutes lead the announcement paragraph with the announcement and market reaction. Put the largest change first, where the reader cannot miss it.

The tells form three families. In 1-3, the summarizer writes from the source rather than from what it describes. In 4-7, the picture lacks owners, status, reasons or proportions. Tells 8 and 9 misjudge what the reader already holds.

The first family has fifty years of science behind it. Kintsch and van Dijk (1978) showed that readers build a text's gist by deleting what does not matter, generalizing lists into a covering statement and constructing statements absent from the text. Memory converges on that gist as details fade. This is one of the field's most replicated results.

Brown and Day (1983) found that novices use only deletion. Their copy-delete is tell 1: following source order, keeping or dropping bits, copying them in roughly the original words. It is every summarizer's default, human or LLM. The operations that make a summary worth reading are hard. Even college students in their data usually failed to construct a covering statement absent from the source. The minutes' mortgage because-clause, present in no transcript, shows that constructed statement.

Van Dijk and Kintsch's later work explains the other two families. Readers retain a situation model by joining the text to existing knowledge. Exact words fade within minutes, sentences within days (van Dijk and Kintsch, 1983). A transcript holds no such model. The situation lived in the participants' heads. This makes raw transcripts hard work to read. Rebuild that situation from the source, then write what is true, who wants what and why, what is decided and what is open.

Readers already hold their own situation model: the project, people and running argument. A summary updates that model rather than describing the situation for a stranger. Each tell makes the update fail. Readers can neither trust an ownerless claim nor follow a pointer to nowhere. Background they already hold updates nothing.

Before sending, read the draft once against the summarization literature's four settled evaluation dimensions (SummEval; Fabbri et al., 2021):

- Relevance: the summary picks what matters.
- Consistency: every statement is supported by the source, or marked as the summarizer's own.
- Coherence: the summary reads as one situation rather than a pile of fragments.
- Fluency: write-docs covers it.

Most tells are one of these dimensions failing in a specific way. Relevance suffers in tells 2, 6 and 7, consistency in tells 4 and 5, coherence in tells 1, 3 and 9.

The literature has no reader dimension or score for whether a summary stands alone. Evaluators judge with the source open beside it, a protocol that cannot see tell 8. Check that separately.

Copy the minutes' discipline, not their register: an owner for every claim, a reason with every judgment, and context needed to understand an event. Leave the committee-speak. "Garnered substantial market attention" survives in the Fed's pages because institutions write that way. A summary for a colleague has no such requirement. write-docs' plain-word rules apply.

Leave the anonymization as well. The minutes say "the manager" and "a few participants" because committee politics require it. Your reader wants names. Who holds a position is half the information. "Sam wants the migration delayed until the index rebuild ships" updates the reader's picture. "Concerns were raised about timing" does not.

When you add a new tell to this skill, add a marked instance of it to the sloppy passage. Where a paired good version exists, add a marker to the minutes passage too.
"""
