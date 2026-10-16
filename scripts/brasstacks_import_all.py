"""Import every Brass Tacks post the Wayback Machine has.

Finds all captured posts with one CDX query, picks the most complete capture
of each (most comments; the latest capture breaks ties), adds any archived
extra comment pages, and imports each post with brasstacks_import.py.

Usage (run from the repo root):

  python -I scripts/brasstacks_import_all.py [options]

Options:
  --render-pdf          print each archived page to PDF (slow: about a minute per post)
  --archive-dir DIR     also copy each PDF to DIR as "<title> - Brass Tacks.pdf"
  --own-pdf SLUG=PATH   use a PDF you saved yourself for that post (repeatable)
  --only SLUG           import just this post (repeatable)
  --force               re-import posts that are already imported
  --cache-dir DIR       keep Wayback responses here so reruns are fast
  --report PATH         write a JSON report of what was imported and any gaps
"""

import argparse
import json
import re
import sys
import tempfile
import time
import traceback
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import brasstacks_import as bi  # noqa: E402

CDX = "https://web.archive.org/cdx/search/cdx?"
PAUSE = 45  # seconds between posts, to stay under the archive's rate limit


def all_captures():
    """Every 200 capture under the blog, grouped into posts and comment pages."""
    query = urllib.parse.urlencode({
        "url": f"{bi.BLOG_HOST}/brass-tacks/", "matchType": "prefix", "output": "txt",
        "fl": "timestamp,original,statuscode,length", "filter": "statuscode:200"})
    posts, pages = {}, {}
    for line in bi.fetch(CDX + query).decode().splitlines():
        ts, url, _, length = line.split()
        path = re.sub(r"^https?://[^/]+", "", url).split("?")[0]
        m = re.match(r"/brass-tacks/(\d{4})/(\d{2})/([^/]+)\.html$", path)
        if m and m.group(3) != "index":
            key = (m.group(1), m.group(2), m.group(3))
            posts.setdefault(key, []).append((ts, int(length)))
            continue
        m = re.match(r"/brass-tacks/\d{4}/\d{2}/([^/]+)/comments/page/(\d+)/$", path)
        if m and m.group(2) != "1":
            pages.setdefault(m.group(1), {}).setdefault(int(m.group(2)), []).append((ts, int(length)))
    for caps in posts.values():
        caps.sort()
    return posts, pages


def candidates(caps):
    """Latest, the three largest, and the earliest capture."""
    out = []
    for ts, _ in [caps[-1]] + sorted(caps, key=lambda c: -c[1])[:3] + [caps[0]]:
        if ts not in out:
            out.append(ts)
    return out


def best_capture(url, caps, parse):
    """(timestamp, comment_count, has_more_pages) of the most complete capture."""
    best = None
    for ts in candidates(caps):
        try:
            doc = bi.fetch(bi.wayback(ts, url, "id_")).decode("utf-8", "replace")
            n = len(parse(doc))
        except Exception:
            continue
        score = (n, ts)
        if best is None or score > best[:2]:
            best = (n, ts, 'pager-label">Next' in doc)
    if best is None:
        raise RuntimeError("no capture parses")
    return best[1], best[0], best[2]


def rest(before):
    """Pause between posts, but only if the post went to the network."""
    if bi._last_request[0] != before:
        time.sleep(PAUSE)


def redo_pdfs(imported, args):
    """Re-render archival PDFs without touching the posts. Posts that use a
    PDF you saved yourself (--own-pdf) are never re-rendered."""
    own = {spec.split("=", 1)[0] for spec in args.own_pdf}
    todo = []
    for slug in sorted(imported):
        if slug in own:
            continue
        pdf = bi.PUBLIC_DIR / slug / f"{slug}.pdf"
        if args.only:
            if slug in args.only:
                todo.append(slug)
        elif not pdf.exists() or not bi.pdf_looks_right(pdf):
            todo.append(slug)
    print(f"{len(todo)} PDFs to render: {todo}")
    failed = []
    for slug in todo:
        try:
            bi.render_post_pdf(slug, args.archive_dir)
        except Exception as e:
            print(f"  FAILED {slug}: {e}")
            failed.append(slug)
        time.sleep(PAUSE)
    print(f"\nrendered {len(todo) - len(failed)} of {len(todo)}")
    for slug in failed:
        print(f"  ERROR {slug}: PDF not rendered")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--render-pdf", action="store_true")
    ap.add_argument("--archive-dir", type=Path)
    ap.add_argument("--own-pdf", action="append", default=[], metavar="SLUG=PATH")
    ap.add_argument("--only", action="append", default=[], metavar="SLUG")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--cache-dir", default=str(Path(tempfile.gettempdir()) / "brasstacks-cache"))
    ap.add_argument("--report", type=Path)
    ap.add_argument("--pdfs-only", action="store_true",
                    help="re-render PDFs that are missing or fail the banner check (or --only posts)")
    args = ap.parse_args()

    own_pdfs = dict(spec.split("=", 1) for spec in args.own_pdf)
    imported = {p.stem for p in bi.CONTENT_DIR.glob("*.md")}

    if args.pdfs_only:
        redo_pdfs(imported, args)
        return

    posts, comment_pages = all_captures()  # always fresh: new captures can appear
    bi.CACHE_DIR = args.cache_dir
    print(f"{len(posts)} posts in the archive")
    report = []
    for (y, m, slug), caps in sorted(posts.items()):
        if args.only and slug not in args.only:
            continue
        if slug in imported and not args.force and slug not in args.only:
            print(f"skip {slug} (already imported)")
            continue
        url = f"https://{bi.BLOG_HOST}/brass-tacks/{y}/{m}/{slug}.html"
        entry = {"slug": slug}
        before = bi._last_request[0]
        try:
            ts, n, more = best_capture(url, caps, lambda d: bi.parse_post(d)["comments"])
            pages = []
            for page_no, page_caps in sorted(comment_pages.get(slug, {}).items()):
                page_url = url[: -len(".html")] + f"/comments/page/{page_no}/"
                page_ts, _, _ = best_capture(page_url, sorted(page_caps), bi.parse_comments)
                pages.append((page_no, page_ts))
            entry = bi.import_post(url, ts, pages, pdf=own_pdfs.get(slug),
                                   render_pdf=args.render_pdf and slug not in own_pdfs,
                                   archive_dir=args.archive_dir)
            if more and not pages:
                entry["warning"] = "comments continue on a page the archive does not have"
        except Exception as e:
            traceback.print_exc()
            entry["error"] = f"{type(e).__name__}: {e}"
        report.append(entry)
        rest(before)

    bi.relink_all()
    if args.report:
        args.report.write_text(json.dumps(report, indent=1))
    print(f"\nimported {sum('error' not in r for r in report)} of {len(report)}")
    for r in report:
        for key in ("error", "pdf_error", "warning"):
            if key in r:
                print(f"  {key.upper()} {r['slug']}: {r[key]}")
        for img in r.get("missing_images", []):
            print(f"  MISSING IMAGE {r['slug']}: {img}")


if __name__ == "__main__":
    main()
