"""Short model names and one-shot completion helpers for aai-coding's LLM agents, over fastllm.

`models` maps short names to full `'vendor/model'` specs (copied from solveit's model options).
`ask` runs a one-shot completion: pass a short name or any full spec, and get the response text back.
"""

__all__ = ['models', 'response_text', 'ask']

from fastllm.acomplete import acomplete
from fastllm.chat import contents, mk_msgs

models = dict(sonnet='anthropic/claude-sonnet-5', sonnet46='anthropic/claude-sonnet-4-6', fable='anthropic/claude-fable-5',
    opus='anthropic/claude-opus-4-8', opus46='anthropic/claude-opus-4-6',
    luna='openai/gpt-5.6-luna', terra='openai/gpt-5.6-terra', sol='openai/gpt-5.6-sol',
    flashlite='gemini/models/gemini-3.1-flash-lite', flash='gemini/models/gemini-3.5-flash', gemini='gemini/models/gemini-3.1-pro-preview',
    qwen='fireworks_ai/accounts/fireworks/models/qwen3p7-plus', minimax='minimax/MiniMax-M3',
    kimi='moonshot/kimi-k2.6', kimicode='moonshot/kimi-k2.7-code',
    glm='fireworks_ai/accounts/fireworks/models/glm-5p2', glmfast='fireworks_ai/accounts/fireworks/routers/glm-5p2-fast',
    dsflash='deepseek/deepseek-v4-flash', dspro='deepseek/deepseek-v4-pro',
    codexluna='codex/gpt-5.6-luna', codexterra='codex/gpt-5.6-terra', codexsol='codex/gpt-5.6-sol')


def response_text(res):
    "The visible text of an `acomplete` result: its message's text parts joined (thinking parts skipped)."
    m = contents(res)
    return '' if not m else ''.join(p.text for p in m.content if p.type == 'text' and p.text)


async def ask(
    prompt,  # The user message
    model='sonnet',  # A `models` short name, or any full 'vendor/model' spec
    system=None,  # Optional system prompt
    effort=None,  # Reasoning effort where the model supports it: 'low'/'medium'/'high'
    max_tokens=8192,  # Response cap; fastllm's own defaults are small
    **kw,  # Passed through to `acomplete`
):
    "One-shot completion returning the response text."
    res = await acomplete(mk_msgs([prompt]), models.get(model, model), system=system,
        reasoning_effort=effort, max_tokens=max_tokens, **kw)
    return response_text(res)
