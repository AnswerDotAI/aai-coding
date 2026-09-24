import pytest, pypdfium2 as pdfium

from aai_coding.looker import look, pdf2pngs


def _mk_pdf(path, npages=2):
    "A tiny multi-page PDF drawn with pypdfium2: page n carries n black bars"
    raw = pdfium.raw
    pdf = pdfium.PdfDocument.new()
    for n in range(1, npages + 1):
        page = pdf.new_page(200, 100)
        for i in range(n):
            r = raw.FPDFPageObj_CreateNewRect(20, 10 + 25*i, 160, 12)
            raw.FPDFPageObj_SetFillColor(r, 0, 0, 0, 255)
            raw.FPDFPath_SetDrawMode(r, raw.FPDF_FILLMODE_WINDING, False)
            raw.FPDFPage_InsertObject(page.raw, r)
        page.gen_content()
    pdf.save(path)


def test_pdf2pngs(tmp_path):
    pdf = tmp_path/'two.pdf'
    _mk_pdf(pdf)
    out = pdf2pngs(pdf, tmp_path/'pages')
    assert [p.name for p in out] == ['two-1.png', 'two-2.png']
    for p in out: assert p.read_bytes()[:8] == b'\x89PNG\r\n\x1a\n'
    assert pdf2pngs(pdf, tmp_path, scale=1)[0].stat().st_size < out[0].stat().st_size


@pytest.mark.slow
def test_look(tmp_path):
    pdf = tmp_path/'bars.pdf'
    _mk_pdf(pdf, npages=3)
    svg = tmp_path/'word.svg'
    svg.write_text(r'<svg xmlns="http://www.w3.org/2000/svg" width="200" height="60"><text x="20" y="40" font-family="sans-serif" font-size="24">LOOKER</text></svg>')
    import asyncio
    res = asyncio.run(look('The first 3 images are PDF pages, each showing some black horizontal bars. The last image shows one word. How many bars are on each page, and what is the word? Answer with just the three counts and the word.', pdf, svg))
    assert '3' in res and 'LOOKER' in res.upper()
