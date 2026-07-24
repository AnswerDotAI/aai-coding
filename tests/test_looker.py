import pytest

from aai_coding.looker import look, pdf2pngs


def _mk_pdf(path, npages=2):
    "A tiny multi-page PDF drawn with CoreGraphics: page n carries n black bars"
    import Quartz
    from Foundation import NSURL
    ctx = Quartz.CGPDFContextCreateWithURL(NSURL.fileURLWithPath_(str(path)), Quartz.CGRectMake(0, 0, 200, 100), None)
    for n in range(1, npages + 1):
        Quartz.CGPDFContextBeginPage(ctx, None)
        Quartz.CGContextSetRGBFillColor(ctx, 0, 0, 0, 1)
        for i in range(n): Quartz.CGContextFillRect(ctx, Quartz.CGRectMake(20, 10 + 25*i, 160, 12))
        Quartz.CGPDFContextEndPage(ctx)
    Quartz.CGPDFContextClose(ctx)


def test_pdf2pngs(tmp_path):
    pdf = tmp_path/'two.pdf'
    _mk_pdf(pdf)
    out = pdf2pngs(pdf, tmp_path/'pages')
    assert [p.name for p in out] == ['two-1.png', 'two-2.png']
    for p in out: assert p.read_bytes()[:8] == b'\x89PNG\r\n\x1a\n'
    one = pdf2pngs(pdf)                                       # default dest: alongside the PDF
    assert one[0].parent == tmp_path
    assert pdf2pngs(pdf, tmp_path, scale=1)[0].stat().st_size < out[0].stat().st_size
    with pytest.raises(ValueError): pdf2pngs(tmp_path/'missing.pdf')


@pytest.mark.slow
def test_look(tmp_path):
    pdf = tmp_path/'bars.pdf'
    _mk_pdf(pdf, npages=3)
    import asyncio
    res = asyncio.run(look('These are 3 PDF pages, each showing some black horizontal bars. How many bars are on each page? Answer with just the three counts.', pdf))
    assert '3' in res
