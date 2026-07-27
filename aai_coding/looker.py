"""Answer questions about images and PDFs via an isolated codex checker, without loading them into your own context (macOS-only). Use it to verify rendered output: PDFs, screenshots, captured windows.

`look` sends the images to a fresh, ephemeral gpt-5.6-luna thread whose only context is the checker charter, your question, and the images, and returns its answer. `pdf2pngs` is the pure-Quartz page renderer it uses, independently useful wherever a PDF needs to become images (no CLI tools, no permissions, no size limit worries in *your* context). Needs `openai-codex` and PyObjC (workspace installs have both). `mdhtml2docx.word.win_pic` is one producer of window captures to check."""
from pathlib import Path
import Quartz
from Foundation import NSURL

__all__ = ['pdf2pngs', 'look']

_CHARTER = ('You are a visual checker. The turn contains questions followed by one or more images; '
    'PDF pages arrive as one image per page, in order.\n'
    '- Answer exactly the questions asked. Nothing else.\n'
    '- Be concise and factual: report what is visible, not what you infer or expect. '
    'If asked about text, quote it verbatim.\n'
    '- If something asked about is not visible, absent, or illegible, say so plainly.\n'
    '- Mention anything clearly anomalous (error dialogs, repair banners, blank pages) '
    'even if not asked, in one sentence.\n'
    '- Never guess. If an image is unreadable, report that as your answer.')


def _png(img, path):
    "Write CGImage `img` as png to `path`, returning it"
    dst = Quartz.CGImageDestinationCreateWithURL(NSURL.fileURLWithPath_(str(path)), 'public.png', 1, None)
    Quartz.CGImageDestinationAddImage(dst, img, None)
    if not Quartz.CGImageDestinationFinalize(dst): raise ValueError(f'could not write png to {path}')
    return path



def pdf2pngs(path, dest_dir=None, scale=2):
    "Render each page of the PDF at `path` as `<stem>-<n>.png` in `dest_dir` (default: alongside), returning the paths"
    p = Path(path).expanduser().resolve()
    pdf = Quartz.CGPDFDocumentCreateWithURL(NSURL.fileURLWithPath_(str(p)))
    if pdf is None: raise ValueError(f'not a readable PDF: {p}')
    d = Path(dest_dir).expanduser() if dest_dir else p.parent
    d.mkdir(parents=True, exist_ok=True)
    cs = Quartz.CGColorSpaceCreateDeviceRGB()
    out = []
    for n in range(1, Quartz.CGPDFDocumentGetNumberOfPages(pdf) + 1):
        page = Quartz.CGPDFDocumentGetPage(pdf, n)
        r = Quartz.CGPDFPageGetBoxRect(page, Quartz.kCGPDFMediaBox)
        w, h = int(r.size.width*scale), int(r.size.height*scale)
        ctx = Quartz.CGBitmapContextCreate(None, w, h, 8, 0, cs, Quartz.kCGImageAlphaPremultipliedLast)
        Quartz.CGContextSetRGBFillColor(ctx, 1, 1, 1, 1)
        Quartz.CGContextFillRect(ctx, Quartz.CGRectMake(0, 0, w, h))
        Quartz.CGContextScaleCTM(ctx, scale, scale)
        Quartz.CGContextDrawPDFPage(ctx, page)
        fp = _png(Quartz.CGBitmapContextCreateImage(ctx), d/f'{p.stem}-{n}.png')
        out.append(fp)
    return out

async def look(
    question,  # What to check; be specific, and say what the images are
    *paths,  # Image and/or PDF files (PDFs are rasterized per page)
    model='gpt-5.6-luna',
    effort='medium',  # Codex reasoning effort: 'none'/'minimal'/'low'/'medium'/'high'/'xhigh'
    scale=2,  # Rasterization scale for PDF pages
):
    "Answer `question` about the files at `paths` via an isolated codex thread. Needs `openai-codex`."
    from tempfile import TemporaryDirectory
    from openai_codex import AsyncCodex, LocalImageInput, Sandbox, TextInput
    from openai_codex.api import ReasoningEffort
    with TemporaryDirectory() as td:
        imgs = []
        for p in map(Path, paths):
            if p.suffix.lower() == '.pdf': imgs += pdf2pngs(p, td, scale=scale)
            else: imgs.append(p)
        async with AsyncCodex() as cx:
            th = await cx.thread_start(model=model, sandbox=Sandbox.read_only, ephemeral=True, base_instructions=_CHARTER)
            res = await th.run([TextInput(question), *(LocalImageInput(str(i)) for i in imgs)], effort=ReasoningEffort(effort))
    return res.final_response
