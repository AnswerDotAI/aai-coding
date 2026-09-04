<!-- do not remove -->

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
