import pytest

from aai_coding.harness_docs import llms_txt


def test_llms_txt():
    assert llms_txt('claude').endswith('/llms.txt')
    assert 'openai.com' in llms_txt('codex')
    assert llms_txt('grok') == 'https://docs.x.ai/llms.txt'
    with pytest.raises(KeyError): llms_txt('unknown')
