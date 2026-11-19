"""Short model names and one-shot completion helpers for aai-coding's LLM agents, over fastllm.

`models` maps short names to full `'vendor/model'` specs (built from `fastllm.types`).
`ask` runs a one-shot completion: pass a short name or any full spec, and get the response text back.
"""

__all__ = ['models', 'response_text', 'ask']

from fastllm.acomplete import acomplete
from fastllm.chat import contents, mk_msgs
from fastllm.types import (haik, sonn, opus, fable, luna, terra, sol, astra, flashlite, flash, hydrogen, neon, carbon, argon,
    muse, muse_contrib, qwenplus, qwen, minimax, kimi, glmflash, glm, dsflash)

models = dict(haiku=f'anthropic/{haik}', sonnet=f'anthropic/{sonn}', opus=f'anthropic/{opus}', fable=f'anthropic/{fable}',
    luna=f'openai/{luna}', terra=f'openai/{terra}', sol=f'openai/{sol}', astra=f'openai/{astra}',
    flashlite=f'gemini/{flashlite}', flash=f'gemini/{flash}', hydrogen=f'gemini/{hydrogen}', neon=f'gemini/{neon}',
    carbon=f'gemini/{carbon}', argon=f'gemini/{argon}', muse=f'meta/{muse}', musecontrib=f'meta/{muse_contrib}',
    qwenplus=f'fireworks_ai/{qwenplus}', qwen=f'fireworks_ai/{qwen}', minimax=f'fireworks_ai/{minimax}', kimi=f'fireworks_ai/{kimi}',
    glmflash=f'fireworks_ai/{glmflash}', glm=f'fireworks_ai/{glm}', dsflash=f'fireworks_ai/{dsflash}',
    codexluna=f'codex/{luna}', codexterra=f'codex/{terra}', codexsol=f'codex/{sol}', codexastra=f'codex/{astra}')


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
