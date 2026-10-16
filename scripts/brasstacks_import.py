"""Import a Brass Tacks post from the Internet Archive into the site.

Brass Tacks was a Typepad blog (brasstacksblog.typepad.com/brass-tacks) that
no longer exists. This script recovers one post from a Wayback Machine
capture and writes:

  src/content/brasstacks/<slug>.md      post body (verbatim HTML), metadata, comments
  public/brasstacks/<slug>/*            images from the post, and the archival PDF

The post body and comments are copied as published. The only changes are
URL rewrites: images point at the local copies, and links to other Brass
Tacks posts point at /brasstacks/<slug>/ when that post has been imported,
or at the Wayback Machine when it has not.

Usage (run from the repo root):

  python -I scripts/brasstacks_import.py POST_URL CAPTURE_TS [options]

  POST_URL     original URL, e.g.
               https://brasstacksblog.typepad.com/brass-tacks/2012/01/introducing-target-driven-zoning-tdz.html
  CAPTURE_TS   Wayback timestamp of the capture to use, e.g. 20240805000615
               (list captures: https://web.archive.org/cdx/search/cdx?url=<POST_URL>)

Options:
  --comments-page N:TS   also take comments from comment page N, capture TS (repeatable)
  --pdf PATH             use an existing PDF of the archived page
  --render-pdf           print the archived page(s) to PDF with headless Edge
  --archive-dir DIR      also copy the PDF to DIR as "<title> - Brass Tacks.pdf"

After every import, links in previously imported posts are re-resolved, so a
Wayback link becomes a local link once its target post has been imported.
"""

import argparse
import base64
import hashlib
import html
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CONTENT_DIR = REPO / "src" / "content" / "brasstacks"
PUBLIC_DIR = REPO / "public" / "brasstacks"

BLOG_HOST = "brasstacksblog.typepad.com"
POST_URL = r"https?://(?:www\.)?brasstacksblog\.typepad\.com(?::80)?/brass-tacks/(\d{4})/(\d{2})/([^/?#\"']+)\.html"
POST_URL_RE = re.compile(POST_URL)
# A whole link target that is a post, either direct or already wrapped in a
# Wayback URL, with an optional #anchor.
POST_LINK_RE = re.compile(r"(https://web\.archive\.org/web/\d+/)?" + POST_URL + r"(#[^\"]*)?")
# Only attribute values are rewritten; a URL shown as text stays as written.
ATTR_RE = re.compile(r'\b(href|src)="([^"]*)"')


def rewrite_attrs(fragment, fn):
    """Apply fn to every href/src value; fn returns the new value."""
    return ATTR_RE.sub(lambda m: f'{m.group(1)}="{fn(m.group(2))}"', fragment)
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


# ---------------------------------------------------------------- fetching

def wayback(ts, url, mode=""):
    return f"https://web.archive.org/web/{ts}{mode}/{url}"


# Set to a directory to keep every Wayback response on disk, so a batch run
# can be repeated without fetching the same captures again.
CACHE_DIR = None

# The Wayback Machine refuses connections for several minutes from clients
# that request too quickly, so space requests out and back off hard when
# refused.
MIN_INTERVAL = 2.0
_last_request = [0.0]


def pace():
    wait = _last_request[0] + MIN_INTERVAL - time.time()
    if wait > 0:
        time.sleep(wait)
    _last_request[0] = time.time()


def fetch(url, tries=5):
    cached = None
    if CACHE_DIR:
        cached = Path(CACHE_DIR) / hashlib.sha1(url.encode()).hexdigest()
        if cached.exists():
            return cached.read_bytes()
    last = None
    for i in range(tries):
        pace()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "provandal-brasstacks-import/1.0"})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
            if cached:
                cached.parent.mkdir(parents=True, exist_ok=True)
                cached.write_bytes(data)
            return data
        except urllib.error.HTTPError as e:
            if e.code == 404:  # not archived; retrying will not help
                raise RuntimeError(f"not archived: {url}") from e
            last = e
            delay = 60 * (i + 1) if e.code == 429 else 5 * (i + 1)
        except Exception as e:  # refused (rate limited) or a transient error
            last = e
            delay = 60 * (i + 1)
        print(f"  fetch retry in {delay}s: {last}")
        time.sleep(delay)
    raise RuntimeError(f"fetch failed: {url}: {last}")


# ---------------------------------------------------------------- parsing

def extract_div(doc, start):
    """Return (inner_html, end_index) for the <div ...> that begins at `start`."""
    open_end = doc.index(">", start) + 1
    depth, pos = 1, open_end
    tag = re.compile(r"<(/?)div\b", re.I)
    while depth:
        m = tag.search(doc, pos)
        if not m:
            raise ValueError("unbalanced <div>")
        depth += -1 if m.group(1) else 1
        pos = m.end()
    close_start = doc.rindex("<", 0, pos)
    return doc[open_end:close_start], doc.index(">", pos) + 1


def find_div(doc, pattern, start=0):
    m = re.compile(pattern).search(doc, start)
    return extract_div(doc, m.start())[0] if m else None


def text(fragment):
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def parse_comments(doc):
    comments = []
    for m in re.finditer(r'<div class="comment font-entrybody[^"]*" id="comment-([0-9a-f]+)"', doc):
        cid = m.group(1)
        block, _ = extract_div(doc, m.start())
        content = find_div(block, rf'<div class="comment-content[^"]*" id="comment-{cid}-content"')
        content = re.sub(r"^\s*<span[^>]*>", "", content)
        content = re.sub(r"</span>\s*$", "", content)
        footer = re.search(r'<p class="comment-footer[^"]*">(.*?)</p>', block, re.S).group(1)
        author = text(footer.split("Posted by:", 1)[1].split("|", 1)[0])
        date = text(re.findall(r"<a[^>]*>(.*?)</a>", footer, re.S)[-1])
        comments.append({"id": cid, "author": author, "date": date, "html": clean_html(content)})
    return comments


def parse_post(doc):
    date = re.search(r'<h2 class="date-header">(.*?)</h2>', doc, re.S).group(1).strip()
    month, day, year = date.split("/")
    title = text(re.search(r'<h3 class="entry-header">(.*?)</h3>', doc, re.S).group(1))
    body = find_div(doc, r'<div class="entry-body">')
    more = find_div(doc, r'<div class="entry-more"')
    if more:
        body += "\n" + more
    posted = re.search(r"Posted at ([^<|]+?)\s*<", doc)
    desc = re.search(r'<meta name="description" content="([^"]*)"', doc)
    return {
        "title": title,
        "pubDate": f"{year}-{month}-{day}",
        "postedAt": posted.group(1).strip() if posted else None,
        "description": html.unescape(desc.group(1)) if desc else "",
        "body": clean_html(body),
        "comments": parse_comments(doc),
    }


def clean_html(fragment):
    """Drop indentation and blank lines. Whitespace between tags does not
    render, and a body without blank lines stays a single raw HTML block
    in Markdown, so the markup passes through untouched."""
    lines = [ln.strip() for ln in fragment.replace("\r", "").split("\n")]
    return "\n".join(ln for ln in lines if ln)


# ---------------------------------------------------------------- rewriting

def image_ext(data):
    if data[:4] == b"\x89PNG":
        return ".png"
    if data[:3] == b"GIF":
        return ".gif"
    if data[:2] == b"\xff\xd8":
        return ".jpg"
    return None  # not an image: the archive served an error page


def localize_images(body, ts, slug, missing):
    """Download every image hosted on the blog and point the post at the
    copy. Images the archive does not have keep a Wayback URL and are
    appended to `missing`."""
    out_dir = PUBLIC_DIR / slug
    asset_re = re.compile(r"https?://(?:www\.)?brasstacksblog\.typepad\.com/\.a/([0-9a-f]+)-(?:pi|\d+wi|\d+si)")
    cache = {}

    def local(m):
        asset_id = m.group(1)
        if asset_id not in cache:
            data = None
            for variant in ("pi", "800wi"):  # full size first
                try:
                    data = fetch(wayback(ts, f"https://{BLOG_HOST}/.a/{asset_id}-{variant}", "im_"))
                except RuntimeError:
                    continue
                if image_ext(data):
                    break
                data = None
            if data is None:
                missing.append(m.group(0))
                cache[asset_id] = wayback(ts, m.group(0), "im_")
            else:
                out_dir.mkdir(parents=True, exist_ok=True)
                name = asset_id + image_ext(data)
                (out_dir / name).write_bytes(data)
                cache[asset_id] = f"/brasstacks/{slug}/{name}"
                print(f"  image {name} ({len(data)} bytes)")
        return cache[asset_id]

    return rewrite_attrs(body, lambda value: local(m) if (m := asset_re.fullmatch(value)) else value)


def cf_decode(hexstr):
    """Cloudflare email obfuscation: the first byte is an XOR key for the rest."""
    data = bytes.fromhex(hexstr)
    return bytes(b ^ data[0] for b in data[1:]).decode("utf-8")


def restore_emails(fragment):
    """Undo the email obfuscation Typepad's CDN applied to late captures.
    A bare address became <a href="/cdn-cgi/l/email-protection"
    class="__cf_email__" data-cfemail="HEX">[email protected]</a>; a mailto
    link became href="/cdn-cgi/l/email-protection#HEX"."""
    fragment = re.sub(
        r'<(?:a|span)[^>]*class="__cf_email__"[^>]*data-cfemail="([0-9a-f]+)"[^>]*>.*?</(?:a|span)>',
        lambda m: html.escape(cf_decode(m.group(1))), fragment, flags=re.S)
    return re.sub(r'(?:https?://[^"]*)?/cdn-cgi/l/email-protection#([0-9a-f]+)',
                  lambda m: "mailto:" + cf_decode(m.group(1)), fragment)


def link_other_blog_pages(fragment, ts):
    """Any remaining link into the dead blog (archive and category pages)
    goes to the Wayback Machine."""
    blog = re.compile(r"https?://(?:www\.)?brasstacksblog\.typepad\.com\S*")
    return rewrite_attrs(fragment, lambda value: wayback(ts, value) if blog.fullmatch(value) else value)


def resolve_post_links(fragment, ts="2024"):
    """Point links to other Brass Tacks posts at the local copy if one
    exists, otherwise at the Wayback Machine."""
    imported = {p.stem for p in CONTENT_DIR.glob("*.md")}

    def target(value):
        m = POST_LINK_RE.fullmatch(value)
        if not m:
            return value
        if m.group(4) in imported:
            return f"/brasstacks/{m.group(4)}/{m.group(5) or ''}"
        if m.group(1):
            return value
        return wayback(ts, value)

    return rewrite_attrs(fragment, target)


# ---------------------------------------------------------------- output

def yaml_str(s):
    return json.dumps(s, ensure_ascii=False)  # a JSON string is a valid YAML scalar


def yaml_block(s, indent):
    pad = " " * indent
    return "|-\n" + "\n".join(pad + ln for ln in s.split("\n"))


def write_post(slug, post, original_url, sources, pdf):
    lines = ["---",
             f"title: {yaml_str(post['title'])}",
             f"pubDate: {post['pubDate']}"]
    if post["postedAt"]:
        lines.append(f"postedAt: {yaml_str(post['postedAt'])}")
    lines.append(f"description: {yaml_str(post['description'])}")
    lines.append(f"originalUrl: {yaml_str(original_url)}")
    lines.append("sources:")
    for label, url in sources:
        lines += [f"  - label: {yaml_str(label)}", f"    url: {yaml_str(url)}"]
    if pdf:
        lines.append(f"pdf: {yaml_str(pdf)}")
    lines.append("comments:" if post["comments"] else "comments: []")
    for c in post["comments"]:
        lines += [f"  - author: {yaml_str(c['author'])}",
                  f"    date: {yaml_str(c['date'])}",
                  f"    html: {yaml_block(c['html'], 6)}"]
    lines += ["---", "", post["body"], ""]
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    path = CONTENT_DIR / f"{slug}.md"
    path.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    return path


def relink_all():
    """Re-resolve links in the body and comment HTML of every imported post.
    Frontmatter fields (originalUrl, sources) are left alone: comment HTML
    is the only frontmatter content indented six spaces."""
    for path in CONTENT_DIR.glob("*.md"):
        src = path.read_text(encoding="utf-8")
        _, front, body = src.split("---\n", 2)
        front = "\n".join(resolve_post_links(ln) if ln.startswith("      ") else ln
                          for ln in front.split("\n"))
        new = f"---\n{front}---\n{resolve_post_links(body)}"
        if new != src:
            path.write_text(new, encoding="utf-8", newline="\n")
            print(f"  relinked {path.name}")


# ---------------------------------------------------------------- PDF

PRINT_TRIES = 5

# Resolves to the load state of an archived page. A rate-limited or
# half-loaded page must never be printed: it would look like the original
# but be missing its theme, banner, or images.
PAGE_READY_JS = r"""(async () => {
  const content = !!document.querySelector('.entry-body, #comments-content');
  const styled = [...document.styleSheets].some(s => {
    try { return /styles\.css/.test(s.href || '') && s.cssRules.length > 0; } catch (e) { return false; }
  });
  let banner = false;
  for (const el of [document.getElementById('banner'), document.getElementById('banner-inner'), document.body]) {
    const m = el && getComputedStyle(el).backgroundImage.match(/url\("?(.*?)"?\)/);
    if (m) {
      banner = await new Promise(ok => {
        const img = new Image();
        img.onload = () => ok(img.naturalWidth > 0);
        img.onerror = () => ok(false);
        img.src = m[1];
      });
      break;
    }
  }
  const imgs = [...document.querySelectorAll('.entry-body img, .entry-more img')];
  await Promise.all(imgs.map(i => i.complete ? null : new Promise(ok => { i.onload = i.onerror = ok; })));
  const images = imgs.every(i => i.naturalWidth > 0);
  return JSON.stringify({content, styled, banner, images});
})()"""


def pdf_looks_right(path):
    """True when the first page shows the dark Brass Tacks banner, which
    only renders when the archived page and its theme loaded."""
    import fitz  # PyMuPDF
    doc = fitz.open(path)
    if "can't reach this page" in doc[0].get_text():
        return False
    pix = doc[0].get_pixmap(dpi=30)
    ys = range(int(pix.height * 0.05), int(pix.height * 0.28), 2)
    xs = range(int(pix.width * 0.1), int(pix.width * 0.9), 2)
    dark = sum(1 for y in ys for x in xs if sum(pix.pixel(x, y)) < 150)
    return dark / (len(ys) * len(xs)) > 0.4


def print_pdf(urls, out_path):
    """Print archived pages to one PDF the way a desktop browser saves them:
    screen styles applied (the Typepad theme CSS is media="screen"), the
    Wayback toolbar hidden, and the Wayback provenance line kept on top."""
    import websocket  # websocket-client
    from pypdf import PdfWriter

    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    profile = tempfile.mkdtemp(prefix="bt-edge-")
    proc = subprocess.Popen(
        [EDGE, "--headless=new", "--disable-gpu", f"--remote-debugging-port={port}",
         f"--remote-allow-origins=http://127.0.0.1:{port}", f"--user-data-dir={profile}", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    parts = []
    try:
        for _ in range(100):
            try:
                tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json"))
                break
            except Exception:
                time.sleep(0.2)
        tab = next(t for t in tabs if t["type"] == "page")
        ws = websocket.create_connection(tab["webSocketDebuggerUrl"], timeout=180)
        seq = [0]

        def call(method, **params):
            seq[0] += 1
            ws.send(json.dumps({"id": seq[0], "method": method, "params": params}))
            while True:
                msg = json.loads(ws.recv())
                if msg.get("id") == seq[0]:
                    if "error" in msg:
                        raise RuntimeError(f"{method}: {msg['error']}")
                    return msg.get("result", {})

        call("Page.enable")
        call("Network.enable")
        # Scripts are not needed to print the page and are most of its
        # requests; fewer requests keeps the archive from rate limiting us.
        call("Network.setBlockedURLs", urls=["*.js", "*.js?*"])
        call("Emulation.setEmulatedMedia", media="screen")
        for i, url in enumerate(urls):
            for attempt in range(PRINT_TRIES):
                if attempt:
                    delay = 90 * attempt
                    print(f"  page incomplete ({state}); reloading in {delay}s")
                    time.sleep(delay)
                pace()
                call("Page.navigate", url=url)
                while json.loads(ws.recv()).get("method") != "Page.loadEventFired":
                    pass
                time.sleep(3)  # late fonts
                state = json.loads(call("Runtime.evaluate", expression=PAGE_READY_JS,
                                        awaitPromise=True, returnByValue=True)["result"]["value"])
                if state["content"] and state["styled"] and state["banner"] and state["images"]:
                    break
            else:
                raise RuntimeError(f"archived page never loaded completely: {url} ({state})")
            call("Runtime.evaluate", expression="""{
                document.getElementById('wm-ipp-base')?.remove();
                const p = document.getElementById('wm-ipp-print');
                if (p) { p.style.display = 'block'; }
                // The theme's page background fills the space below the
                // footer on the last sheet; a desktop print leaves it white.
                document.documentElement.style.background = '#fff';
                document.body.style.background = '#fff';
            }""")
            res = call("Page.printToPDF", printBackground=True, displayHeaderFooter=True,
                       paperWidth=8.5, paperHeight=11, marginTop=0.4, marginBottom=0.4,
                       marginLeft=0.4, marginRight=0.4)
            part = Path(profile) / f"part{i}.pdf"
            part.write_bytes(base64.b64decode(res["data"]))
            parts.append(part)
        ws.close()
    finally:
        proc.terminate()
        proc.wait(timeout=30)

    writer = PdfWriter()
    for part in parts:
        writer.append(str(part))
    with open(out_path, "wb") as f:
        writer.write(f)
    shutil.rmtree(profile, ignore_errors=True)
    if not pdf_looks_right(out_path):
        Path(out_path).unlink()
        raise RuntimeError(f"rendered PDF failed the banner check: {urls[0]}")


# ---------------------------------------------------------------- main

def comment_key(c):
    """Sort key for a comment's "MM/DD/YYYY at HH:MM AM" timestamp."""
    try:
        return time.strptime(c["date"], "%m/%d/%Y at %I:%M %p")
    except ValueError:
        return time.gmtime(0)


def import_post(post_url, capture_ts, comment_pages=(), pdf=None, render_pdf=False, archive_dir=None):
    """Import one post. comment_pages is a list of (page_number, capture_ts).
    Returns a summary dict for reporting."""
    m = POST_URL_RE.match(post_url)
    if not m:
        raise ValueError(f"not a Brass Tacks post URL: {post_url}")
    original_url = f"https://{BLOG_HOST}/brass-tacks/{m.group(1)}/{m.group(2)}/{m.group(3)}.html"
    slug = m.group(3)

    print(f"fetching {slug} @ {capture_ts}")
    doc = fetch(wayback(capture_ts, original_url, "id_")).decode("utf-8")
    post = parse_post(doc)
    page_urls = [wayback(capture_ts, original_url)]
    sources = [("Post and first page of comments" if comment_pages else "Post and comments", page_urls[0])]

    seen = {c["id"] for c in post["comments"]}
    for n, ts in comment_pages:
        page_url = original_url[: -len(".html")] + f"/comments/page/{n}/"
        page = fetch(wayback(ts, page_url, "id_")).decode("utf-8")
        extra = [c for c in parse_comments(page) if c["id"] not in seen]
        seen.update(c["id"] for c in extra)
        post["comments"] += extra
        page_urls.append(wayback(ts, page_url))
        sources.append((f"Comments page {n}", page_urls[-1]))
        print(f"  comments page {n}: {len(extra)} comments")
    post["comments"].sort(key=comment_key)  # stable: page order breaks ties

    missing = []
    def fix_links(fragment):
        return link_other_blog_pages(resolve_post_links(fragment, capture_ts), capture_ts)

    post["body"] = fix_links(localize_images(restore_emails(post["body"]), capture_ts, slug, missing))
    for c in post["comments"]:
        c["html"] = fix_links(restore_emails(c["html"]))

    pdf_rel, pdf_error = None, None
    if pdf or render_pdf:
        (PUBLIC_DIR / slug).mkdir(parents=True, exist_ok=True)
        pdf_path = PUBLIC_DIR / slug / f"{slug}.pdf"
        try:
            if pdf:
                shutil.copyfile(pdf, pdf_path)
            else:
                print("  printing archived page(s) to PDF")
                print_pdf(page_urls, pdf_path)
            pdf_rel = f"/brasstacks/{slug}/{slug}.pdf"
        except Exception as e:  # keep the post; the PDF can be re-rendered later
            pdf_error = f"{type(e).__name__}: {e}"
            print(f"  PDF FAILED: {pdf_error}")
    elif (PUBLIC_DIR / slug / f"{slug}.pdf").exists():
        pdf_rel = f"/brasstacks/{slug}/{slug}.pdf"  # re-import keeps the PDF already made
        if pdf_rel and archive_dir:
            safe = re.sub(r'[<>:"/\\|?*]', "", post["title"])
            dest = Path(archive_dir) / f"{safe} - Brass Tacks.pdf"
            if not dest.exists():
                shutil.copyfile(pdf_path, dest)
                print(f"  archived {dest}")

    path = write_post(slug, post, original_url, sources, pdf_rel)
    print(f"wrote {path.relative_to(REPO)}: {post['title']} ({post['pubDate']}), "
          f"{len(post['comments'])} comments")
    return {"slug": slug, "title": post["title"], "pubDate": post["pubDate"],
            "comments": len(post["comments"]), "capture": capture_ts,
            "comment_pages": [list(p) for p in comment_pages],
            "missing_images": missing, "pdf": bool(pdf_rel),
            **({"pdf_error": pdf_error} if pdf_error else {})}


def render_post_pdf(slug, archive_dir=None):
    """Re-render the archival PDF of an imported post from the captures
    recorded in its frontmatter, leaving the post itself untouched."""
    src = (CONTENT_DIR / f"{slug}.md").read_text(encoding="utf-8")
    front = src.split("---\n", 2)[1]
    urls = re.findall(r'^    url: "([^"]+)"', front, re.M)
    title = json.loads(re.search(r"^title: (.*)$", front, re.M).group(1))
    pdf_path = PUBLIC_DIR / slug / f"{slug}.pdf"
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"printing {slug}")
    print_pdf(urls, pdf_path)
    if "\npdf:" not in front:
        body = src.split("---\n", 2)[2]
        front = front.replace("\ncomments:", f'\npdf: "/brasstacks/{slug}/{slug}.pdf"\ncomments:', 1)
        (CONTENT_DIR / f"{slug}.md").write_text(f"---\n{front}---\n{body}", encoding="utf-8", newline="\n")
    if archive_dir:
        safe = re.sub(r'[<>:"/\\|?*]', "", title)
        shutil.copyfile(pdf_path, Path(archive_dir) / f"{safe} - Brass Tacks.pdf")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("post_url")
    ap.add_argument("capture_ts")
    ap.add_argument("--comments-page", action="append", default=[], metavar="N:TS")
    pdf = ap.add_mutually_exclusive_group()
    pdf.add_argument("--pdf", type=Path)
    pdf.add_argument("--render-pdf", action="store_true")
    ap.add_argument("--archive-dir", type=Path)
    args = ap.parse_args()

    pages = [tuple(spec.split(":")) for spec in args.comments_page]
    summary = import_post(args.post_url, args.capture_ts, pages, args.pdf, args.render_pdf, args.archive_dir)
    for url in summary["missing_images"]:
        print(f"  WARNING image not in the archive: {url}")
    relink_all()


if __name__ == "__main__":
    main()
