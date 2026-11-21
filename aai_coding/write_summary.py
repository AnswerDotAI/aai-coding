r"""How to write summaries that stand alone: read before summarizing a conversation, meeting, PR, paper, or repo change for a human reader.

notation: /why

- scope: long sources (transcript, chat, review, diff, paper); summary = only thing read
- split: `write_docs` = sentences, plain words, fluency; here = content    /clean short prose can pass `write_docs` and still fail completely on content
- goal: source records what was said in order, not the situation model participants held in mind; rebuild situation, write what is now true: decisions, open items, who wants or does what, why    /shortening alone fails
- audience: holds existing situation model (project, people, running argument); update it rather than briefing a stranger or reciting known background
- standard: FOMC minutes (day's meeting → pages): owner per claim; event, reaction, judgment, reason — including unstated reasons constructed so passage stands alone (`"decline unlikely to raise refinancing: current mortgage rates well above weighted average outstanding rate"`)
- register: minutes' discipline, not committee-speak (`"garnered substantial market attention"` ⇒ `write_docs` plain words) or anonymization (`"the manager"`, `"a few participants"` ⇒ real names; `"Sam wants migration delayed until index rebuild ships"`, not `"Concerns were raised about timing"`)    /who holds a position is half the information

## Tells

### Source over situation (1–3)

- 1. Walking source: source order (turn, file, section); order by subject; `"briefing opened with"` / `"toward the end"` ⇒ omit timing (`"turned first to"` fine if agenda was subject-ordered)
- 2. Topics without content: what source is about, not what it says (`"we discussed migration"`, `"PR refactors auth"`, `"explores caching tradeoffs"`, `"covered a range of topics"`) ⇒ specifics or drop    /writable before reading = says nothing
- 3. Pointers to nowhere: references resolving only in source (`"approach discussed earlier"`, `"second reviewer's concern"`, `"drivers mentioned earlier"`, `"see Section 3"`) ⇒ name it; every reference must resolve inside summary

### Missing owners, status, reasons, or proportion (4–7)

- 4. Ownerless claims: blurs fact, position, own guess (`"economy is seen as resilient"` ⇒ `"Desk survey respondents see..."`; `"Some concerns were raised"` hides who and what); paper: authors' findings vs citations vs own view; PR: code behavior vs description claims vs reviewer suspicions; mark own inferences
- 5. No status: thread without state (decided, dropped, open; PR: merged, blocked, awaiting review) or unowned task (`"question was raised whether repo poses risk"` ⇒ `"manager noted repo stability matters"`); left open ⇒ state open (`"undecided"` = status)
- 6. Dropped why: conclusion without reason (`"refinancing not expected to rise"` omits mortgage-rate reason); reasons let readers verify logic and spot expiry; scattered across turns, PR comments, paper intro/discussion    /gathering them = most of the work, lost first
- 7. Space by bulk: length tracks source bulk, not impact (20-min survey-wording digression ⇒ omit; 2-line decisive exchange gets half a clause; 1000-line mechanical rename burying 1-line behavior change); weight by situation impact

### Reader knowledge mismatch (8–9)

- 8. Assumes you read it: fails without source beside it (`"the recent announcement"` ⇒ `"Fannie Mae and Freddie Mac may expand mortgage portfolios"`); readers may never open or have forgotten source; must work a week later without it    /stand alone = name what source introduced, not known background
- 9. Buried lede: biggest change last because last in source (announcement and MBS yield move saved for end) ⇒ lead with largest change

## Science

- Kintsch & van Dijk (1978): gist built via deletion, generalization (covering statements), construction (absent statements, e.g. mortgage-rate reason); gist persists as details fade
- Brown & Day (1983): novices and default LLMs use copy-delete (tell 1: source order, keep/drop, roughly original words); generalizing and constructing are hard (college students constructed covering statements ~half the time)
- van Dijk & Kintsch (1983): exact words fade in minutes, sentences in days; situation model (text joined to prior knowledge) persists

## Pre-send check (SummEval; Fabbri et al., 2021)

dimension|criterion|failing tells
-|-|-
Relevance|picks what matters|2, 6, 7
Consistency|supported by source, or marked as yours|4, 5
Coherence|reads as one situation, not fragments|1, 3, 9
Fluency|`write_docs`|—

- standalone (tell 8): check separately    /no literature metric: evaluators keep source open beside summary and miss it
"""

__all__ = []
