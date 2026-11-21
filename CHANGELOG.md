<!-- do not remove -->

## 0.1.1

### New Features

- Replace theory with understand skill, tighten skills and prompts, fix harness truncation regex, and exit 0 on safecmd defer ([#47](https://github.com/AnswerDotAI/aai-coding/issues/47))
- Add Antigravity swarm guard hook requiring fork=coordinator for workers, rename kernel rule to GEMINI.md, extend writing rules ([#46](https://github.com/AnswerDotAI/aai-coding/issues/46))
- agy ([#43](https://github.com/AnswerDotAI/aai-coding/issues/43))
- Rewrite prompts and writing guides in plain active imperative voice; note clikernel has no workspace or writable-root restriction ([#42](https://github.com/AnswerDotAI/aai-coding/issues/42))
- Set exhash journal/author env defaults for Claude Code and MCP sessions ([#39](https://github.com/AnswerDotAI/aai-coding/issues/39))
- Unify Claude and Codex on per-agent clikernel exec/create workflow, show slopometer advice in slop hook ([#38](https://github.com/AnswerDotAI/aai-coding/issues/38))
- Add SubagentStart fork hook, quote last request in air nudge, share writing-guide text via `_writing`, fix slopometer JSON unpacking ([#37](https://github.com/AnswerDotAI/aai-coding/issues/37))
- Replace Codex vision agents with single tool-free fastllm requests, adding model/effort/`max_tokens` options and cost reporting ([#36](https://github.com/AnswerDotAI/aai-coding/issues/36))
- Replace looker with vision skill providing look and transcribe agents ([#35](https://github.com/AnswerDotAI/aai-coding/issues/35))
- Add claudesub command to run headless Claude child sessions from a compacted parent transcript ([#34](https://github.com/AnswerDotAI/aai-coding/issues/34))
- Drop llmdojo dependency: remove dojo bootstrap and drop-sentinel hook, add own kernel/startup.py ([#33](https://github.com/AnswerDotAI/aai-coding/issues/33))
- Replace dojo bootstrap gate with skill startup steps, port looker to pypdfium2/pyvips with SVG support, add prompt shortcuts . ; , ([#32](https://github.com/AnswerDotAI/aai-coding/issues/32))
- Update clikernel tool names in setup docs and harness messages ([#29](https://github.com/AnswerDotAI/aai-coding/pull/29)), thanks to [@ncoop57](https://github.com/ncoop57)
- Document public and team workspace setup ([#26](https://github.com/AnswerDotAI/aai-coding/pull/26)), thanks to [@jph00](https://github.com/jph00)
- Add starter workspace setup and use aidialog for notebook workflows ([#25](https://github.com/AnswerDotAI/aai-coding/pull/25)), thanks to [@jph00](https://github.com/jph00)
- Add `problem_finding` pyskill and bare-backtick prompt notice ([#17](https://github.com/AnswerDotAI/aai-coding/pull/17)), thanks to [@ncoop57](https://github.com/ncoop57)

### Bugs Squashed

- Load kernel startup tools in every directory ([#40](https://github.com/AnswerDotAI/aai-coding/pull/40)), thanks to [@jph00](https://github.com/jph00)
- Fixed macscript path in looker.py ([#30](https://github.com/AnswerDotAI/aai-coding/pull/30)), thanks to [@kafkasl](https://github.com/kafkasl)


## 0.1.0

### New Features

- Drop the post-compaction doc-state reset from the hooks ([#22](https://github.com/AnswerDotAI/aai-coding/pull/22)), thanks to [@jph00](https://github.com/jph00)
- Add kernel-free notebook editing guidance for Codex ([#20](https://github.com/AnswerDotAI/aai-coding/pull/20)), thanks to [@jph00](https://github.com/jph00)
- Add hybrid codex mode using native tools with a quiet clikernel for Python, alongside the existing kernel-centric setup ([#18](https://github.com/AnswerDotAI/aai-coding/issues/18))
- Document claude-slop hook in SETUP.md ([#16](https://github.com/AnswerDotAI/aai-coding/pull/16)), thanks to [@ncoop57](https://github.com/ncoop57)
- Keep post-compact doc-state on synthetic resume via boundary timestamp; add bare-quote caveat prompt ([#15](https://github.com/AnswerDotAI/aai-coding/issues/15))
- add slopometer scoring hook for assistant messages, expand write_docs tells and banned words ([#12](https://github.com/AnswerDotAI/aai-coding/issues/12))
- Split reference prose into new write-docs skill, narrow write-prose to narrative ([#11](https://github.com/AnswerDotAI/aai-coding/issues/11))
- Add `write_summary` pyskill for summaries that stand alone ([#10](https://github.com/AnswerDotAI/aai-coding/pull/10)), thanks to [@ncoop57](https://github.com/ncoop57)
- Add appraisal preamble tell and metadiscourse rule to prose skill; tighten sysp closing-caveat ban and cite ASD-STE100 ([#9](https://github.com/AnswerDotAI/aai-coding/issues/9))
- Add claude-air and drop-sentinel hooks ([#8](https://github.com/AnswerDotAI/aai-coding/issues/8))
- Require verified doc keys for doced() declarations and update resume/skill guidance ([#7](https://github.com/AnswerDotAI/aai-coding/issues/7))
- Added naur discussion skill ([#6](https://github.com/AnswerDotAI/aai-coding/pull/6)), thanks to [@kafkasl](https://github.com/kafkasl)
- Consolidate prompt_submit hooks to emit a single JSON object; prose and punctuation cleanup across style docs ([#5](https://github.com/AnswerDotAI/aai-coding/issues/5))
- Add llms.py completion helper, migrate check_prose to fastllm, and extend prose tells ([#3](https://github.com/AnswerDotAI/aai-coding/issues/3))
- docs: replace skillOverrides with disableBundledSkills flag ([#1](https://github.com/AnswerDotAI/aai-coding/pull/1)), thanks to [@kafkasl](https://github.com/kafkasl)

### Bugs Squashed

- The bash guard's 2>&1 message no longer suggests a redirect ([#23](https://github.com/AnswerDotAI/aai-coding/pull/23)), thanks to [@jph00](https://github.com/jph00)
