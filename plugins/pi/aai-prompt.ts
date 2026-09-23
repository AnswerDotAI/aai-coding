import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

const QUESTION_NOTICE =
	"This looks like a question. Answer it directly, before and instead of any further work. Most questions need no tool call.";
const READ_NOTICE =
	"This prompt appears to ask you to read something. Read the target in full before answering.";
const APPROVAL_NOTICE =
	"This bare approval covers exactly what was explicitly agreed. Ask before doing anything whose approval is uncertain.";
const BTW_NOTICE =
	"This prompt begins with `BTW ` and is a side request. Answer it first, then resume unfinished work unless the user cancels it.";
const CAVEAT_NOTICE =
	"The user sent a bare apostrophe because the previous reply ended with an unnecessary caveat. State the concrete blocker, complete routine work, or withdraw an unsupported concern.";

export function promptNotices(prompt: string): string[] {
	const notices: string[] = [];
	if (prompt.trimEnd().endsWith("?")) notices.push(QUESTION_NOTICE);
	if (prompt.toLowerCase().includes("please read")) notices.push(READ_NOTICE);
	if (["go", "ok"].includes(prompt.toLowerCase().trim().replace(/[.!]+$/, ""))) notices.push(APPROVAL_NOTICE);
	if (prompt.startsWith("BTW ")) notices.push(BTW_NOTICE);
	if (prompt.trim() === "'") notices.push(CAVEAT_NOTICE);
	return notices;
}

export default function aaiPrompt(pi: ExtensionAPI) {
	pi.on("before_agent_start", (event) => {
		const notices = promptNotices(event.prompt);
		if (!notices.length) return;
		return {
			message: {
				customType: "aai-prompt-notice",
				content: notices.join("\n"),
				display: false,
			},
		};
	});
}
