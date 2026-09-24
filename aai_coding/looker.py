"""Answer questions about images, SVGs, and PDFs by asking a separate codex process to look at them, which keeps large files out of this session. Use it to verify rendered output: PDFs, SVGs, screenshots, captured windows.

`look` sends the images to a fresh, ephemeral gpt-6-sol thread whose only context is the checker charter, your question, and the images, and returns its answer. It renders each PDF page to a PNG with `pdf2pngs`, and SVGs at their own size. It sends every image as a PNG on a white background, scaled down to at most one megapixel. It reads the formats libvips reads, including TIFF, WebP, HEIC and GIF. `pdf2pngs` renders with pypdfium2 and is independently useful wherever a PDF needs to become images (no CLI tools, no permissions, no size limit worries in *your* context). Needs `openai-codex` (workspace installs have it). `macscript.word.win_pic` is one producer of window captures to check."""
from pathlib import Path
import pypdfium2 as pdfium, pyvips

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


def _img2png(path, dest):
    "Convert the image at `path` to png `dest` on a white background, at most one megapixel, returning `dest`"
    # Loading from bytes skips libvips' filename cache, which returns stale images for files changed since an earlier load.
    img = pyvips.Image.new_from_buffer(path.read_bytes(), '')
    if img.hasalpha(): img = img.flatten(background=255)
    if (n := img.width * img.height) > 1e6: img = img.resize((1e6 / n) ** 0.5)
    img.write_to_file(dest)
    return dest


def pdf2pngs(path, dest_dir=None, scale=2):
    "Render each page of the PDF at `path` as `<stem>-<n>.png` in `dest_dir` (default: alongside), returning the paths"
    p = Path(path).expanduser().resolve()
    d = Path(dest_dir).expanduser() if dest_dir else p.parent
    d.mkdir(parents=True, exist_ok=True)
    out = []
    for n, page in enumerate(pdfium.PdfDocument(p), 1):
        bm = page.render(scale=scale, prefer_bgrx=True, rev_byteorder=True)
        out.append(d/f'{p.stem}-{n}.png')
        pyvips.Image.new_from_memory(bm.buffer, bm.width, bm.height, 4, 'uchar')[:3].write_to_file(out[-1])
    return out

async def look(
    question,  # What to check; be specific, and say what the images are
    *paths,  # Image, SVG, and/or PDF files (PDFs are rasterized per page)
    model='gpt-6-sol',
    effort='medium',  # Codex reasoning effort: 'none'/'minimal'/'low'/'medium'/'high'/'xhigh'
    scale=2,  # Rasterization scale for PDF pages
):
    "Answer `question` about the files at `paths` via an isolated codex thread. Needs `openai-codex`."
    from tempfile import TemporaryDirectory
    from openai_codex import AsyncCodex, LocalImageInput, Sandbox, TextInput
    from openai_codex.api import ReasoningEffort
    with TemporaryDirectory() as td:
        pages = []
        for i, p in enumerate(Path(o).expanduser() for o in paths):
            pages += pdf2pngs(p, Path(td)/str(i), scale=scale) if p.suffix.lower() == '.pdf' else [p]
        imgs = [_img2png(p, Path(td)/f'{i}.png') for i, p in enumerate(pages)]
        async with AsyncCodex() as cx:
            th = await cx.thread_start(model=model, sandbox=Sandbox.read_only, ephemeral=True, base_instructions=_CHARTER)
            res = await th.run([TextInput(question), *(LocalImageInput(str(f)) for f in imgs)], effort=ReasoningEffort(effort))
    return res.final_response
