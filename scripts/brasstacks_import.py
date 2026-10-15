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
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CONTENT_DIR = REPO / "src" / "content" / "brasstacks"
PUBLIC_DIR = REPO / "public" / "brasstacks"

BLOG_HOST = "brasstacksblog.typepad.com"
POST_URL = r"https?://(?:www\.)?brasstacksblog\.typepad\.com(?::80)?/brass-tacks/(\d{4})/(\d{2})/([^/?#\"']+)\.html"
POST_URL_RE = re.compile(POST_URL)
# A link to a post, either direct or already wrapped in a Wayback URL.
POST_LINK_RE = re.compile(r"(https://web\.archive\.org/web/\d+/)?" + POST_URL)
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


# ---------------------------------------------------------------- fetching

def wayback(ts, url, mode=""):
    return f"https://web.archive.org/web/{ts}{mode}/{url}"


def fetch(url, tries=4):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "provandal-brasstacks-import/1.0"})
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except Exception as e:  # the Wayback Machine is flaky; back off and retry
            last = e
            time.sleep(3 * (i + 1))
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

def localize_images(body, ts, slug):
    """Download every image hosted on the blog and point the post at the copy."""
    out_dir = PUBLIC_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    asset_re = re.compile(r"https?://(?:www\.)?brasstacksblog\.typepad\.com/\.a/([0-9a-f]+)-(?:pi|\d+wi|\d+si)")
    cache = {}

    def local(asset_id):
        if asset_id not in cache:
            data = None
            for variant in ("pi", "800wi"):  # full size first
                try:
                    data = fetch(wayback(ts, f"https://{BLOG_HOST}/.a/{asset_id}-{variant}", "im_"))
                    break
                except RuntimeError:
                    continue
            if data is None:
                raise RuntimeError(f"image {asset_id} not in the archive")
            ext = ".png" if data[:4] == b"\x89PNG" else ".gif" if data[:3] == b"GIF" else ".jpg"
            (out_dir / f"{asset_id}{ext}").write_bytes(data)
            cache[asset_id] = f"/brasstacks/{slug}/{asset_id}{ext}"
            print(f"  image {asset_id}{ext} ({len(data)} bytes)")
        return cache[asset_id]

    return asset_re.sub(lambda m: local(m.group(1)), body)


def resolve_post_links(fragment, ts="2024"):
    """Point links to other Brass Tacks posts at the local copy if one
    exists, otherwise at the Wayback Machine."""
    imported = {p.stem for p in CONTENT_DIR.glob("*.md")}

    def target(m):
        if m.group(4) in imported:
            return f"/brasstacks/{m.group(4)}/"
        if m.group(1):
            return m.group(0)
        return wayback(ts, m.group(0))

    return POST_LINK_RE.sub(target, fragment)


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
        call("Emulation.setEmulatedMedia", media="screen")
        for i, url in enumerate(urls):
            call("Page.navigate", url=url)
            while json.loads(ws.recv()).get("method") != "Page.loadEventFired":
                pass
            time.sleep(4)  # late images and fonts
            call("Runtime.evaluate", expression="""
                document.getElementById('wm-ipp-base')?.remove();
                const p = document.getElementById('wm-ipp-print');
                if (p) { p.style.display = 'block'; }
                // The theme's page background fills the space below the
                // footer on the last sheet; a desktop print leaves it white.
                document.documentElement.style.background = '#fff';
                document.body.style.background = '#fff';
            """)
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


# ---------------------------------------------------------------- main

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

    m = POST_URL_RE.match(args.post_url)
    if not m:
        sys.exit(f"not a Brass Tacks post URL: {args.post_url}")
    original_url = f"https://{BLOG_HOST}/brass-tacks/{m.group(1)}/{m.group(2)}/{m.group(3)}.html"
    slug = m.group(3)

    print(f"fetching {slug} @ {args.capture_ts}")
    doc = fetch(wayback(args.capture_ts, original_url, "id_")).decode("utf-8")
    post = parse_post(doc)
    page_urls = [wayback(args.capture_ts, original_url)]
    sources = [("Post and first page of comments", page_urls[0])]

    seen = {c["id"] for c in post["comments"]}
    for spec in args.comments_page:
        n, ts = spec.split(":")
        page_url = original_url[: -len(".html")] + f"/comments/page/{n}/"
        page = fetch(wayback(ts, page_url, "id_")).decode("utf-8")
        extra = [c for c in parse_comments(page) if c["id"] not in seen]
        seen.update(c["id"] for c in extra)
        post["comments"] += extra
        page_urls.append(wayback(ts, page_url))
        sources.append((f"Comments page {n}", page_urls[-1]))
        print(f"  comments page {n}: {len(extra)} comments")

    post["body"] = resolve_post_links(localize_images(post["body"], args.capture_ts, slug), args.capture_ts)
    for c in post["comments"]:
        c["html"] = resolve_post_links(c["html"], args.capture_ts)

    pdf_rel = None
    if args.pdf or args.render_pdf:
        (PUBLIC_DIR / slug).mkdir(parents=True, exist_ok=True)
        pdf_path = PUBLIC_DIR / slug / f"{slug}.pdf"
        if args.pdf:
            shutil.copyfile(args.pdf, pdf_path)
        else:
            print("  printing archived page(s) to PDF")
            print_pdf(page_urls, pdf_path)
        pdf_rel = f"/brasstacks/{slug}/{slug}.pdf"
        if args.archive_dir:
            safe = re.sub(r'[<>:"/\\|?*]', "", post["title"])
            dest = args.archive_dir / f"{safe} - Brass Tacks.pdf"
            if not dest.exists():
                shutil.copyfile(pdf_path, dest)
                print(f"  archived {dest}")

    path = write_post(slug, post, original_url, sources, pdf_rel)
    print(f"wrote {path.relative_to(REPO)}: {post['title']} ({post['pubDate']}), "
          f"{len(post['comments'])} comments")
    relink_all()


if __name__ == "__main__":
    main()
