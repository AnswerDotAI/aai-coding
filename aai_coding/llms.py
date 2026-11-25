"""Short model names and one-shot completion helpers for aai-coding's LLM agents, over fastllm.

`models` maps extra short names not in `fastllm.types.model_aliases` to specs accepted by `fastllm.acomplete`.
`ask` runs a one-shot completion: pass a short name or any full spec, and get the response text back.
"""

__all__ = ['models', 'response_text', 'ask']

from fastllm.acomplete import acomplete
from fastllm.chat import contents, mk_msgs

models = dict(haiku='haik', sonnet='sonn', musecontrib='muse_contrib',
    codexluna='codex/luna', codexterra='codex/terra', codexsol='codex/sol', codexastra='codex/astra')


def response_text(res):
    "The visible text of an `acomplete` result: its message's text parts joined (thinking parts skipped)."
    m = contents(res)
    return '' if not m else ''.join(p.text for p in m.content if p.type == 'text' and p.text)


async def ask(
    prompt,  # The user message
    model='sonnet',  # A `fastllm`/`models` short name, or any full 'vendor/model' spec
    system=None,  # Optional system prompt
    effort=None,  # Reasoning effort where the model supports it: 'low'/'medium'/'high'
    max_tokens=8192,  # Response cap; fastllm's own defaults are small
    **kw,  # Passed through to `acomplete`
):
    "One-shot completion returning the response text."
    res = await acomplete(mk_msgs([prompt]), models.get(model, model), system=system,
        reasoning_effort=effort, max_tokens=max_tokens, **kw)
    return response_text(res)
