import pytest, pypdfium2 as pdfium, pyvips

from aai_coding.vision import look, pdf2pngs, _img2png


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


def test_rendered_inputs(tmp_path):
    pdf = tmp_path/'bars.pdf'
    _mk_pdf(pdf)
    first,second = pdf2pngs(pdf, tmp_path/'pages', scale=5)
    selected, = pdf2pngs(pdf, tmp_path/'selected', scale=5, pages=[2])
    a,b,c = [pyvips.Image.new_from_file(p) for p in (first,second,selected)]
    assert (c-b).abs().max() == 0 and c.avg() < a.avg()
    assert (c.width,c.height) == (1000,500)
    for limit,size in ((None,(1000,500)), (125000,(500,250))):
        img = pyvips.Image.new_from_file(_img2png(selected, tmp_path/f'{limit}.png', max_pixels=limit))
        assert (img.width,img.height) == size


@pytest.mark.slow
def test_look(tmp_path):
    pdf = tmp_path/'bars.pdf'
    _mk_pdf(pdf, npages=3)
    svg = tmp_path/'word.svg'
    svg.write_text(r'<svg xmlns="http://www.w3.org/2000/svg" width="200" height="60"><text x="20" y="40" font-family="sans-serif" font-size="24">LOOKER</text></svg>')
    import asyncio
    res = asyncio.run(look('The first 3 images are PDF pages, each showing some black horizontal bars. The last image shows one word. How many bars are on each page, and what is the word? Answer with just the three counts and the word.', pdf, svg))
    assert all(s in res for s in ('1', '2', '3')) and 'LOOKER' in res.upper()
