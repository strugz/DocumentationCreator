#!/usr/bin/env python3
"""Render the Mermaid diagrams of a document folder to PNG for the Word export.

Usage:
    python tools/render_mermaid.py output/<mode>/<slug> [--port 8765]

The script starts a small web server on localhost and prints a URL. Open that URL in
any browser: the page renders every Mermaid block with Mermaid from the jsDelivr CDN
and sends each PNG back. The PNGs are written to <folder>/assets/diagrams/<key>.png,
where <key> is the first 16 hex characters of the SHA-1 of the block source.
tools/md_to_docx.js embeds an image when its key matches, so re-run this script after
a diagram changes. The server stops by itself when every diagram is saved.
"""
import argparse
import hashlib
import json
import re
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

MERMAID_URL = "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"
FENCE = re.compile(r"^\s*(```|~~~)(.*)$")


def blocks(folder):
    """Yield (key, source) for every Mermaid block in NN-*.md and INDEX.md."""
    seen = set()
    for f in sorted(folder.glob("*.md")):
        if not re.match(r"^(\d\d-.*|INDEX)\.md$", f.name):
            continue
        lines = f.read_text(encoding="utf-8").split("\n")
        i = 0
        while i < len(lines):
            m = FENCE.match(lines[i])
            if not m:
                i += 1
                continue
            lang, body = m.group(2).strip(), []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith(m.group(1)):
                body.append(lines[i])
                i += 1
            i += 1
            if lang == "mermaid":
                src = "\n".join(body).strip()
                key = hashlib.sha1(src.encode("utf-8")).hexdigest()[:16]
                if key not in seen:
                    seen.add(key)
                    yield key, src


PAGE = """<!doctype html><html><head><meta charset="utf-8"><title>Render diagrams</title>
<script src="%(mermaid)s"></script>
<style>body{font-family:Arial,sans-serif;margin:24px}#log{white-space:pre-wrap}</style></head>
<body><h1>Rendering diagrams</h1><div id="log"></div><div id="work"></div>
<script>
const JOBS = %(jobs)s;
const log = (m) => { document.getElementById("log").textContent += m + "\\n"; };
mermaid.initialize({ startOnLoad: false, theme: "default", securityLevel: "loose",
  htmlLabels: false, flowchart: { htmlLabels: false, useMaxWidth: false },
  sequence: { useMaxWidth: false }, er: { useMaxWidth: false }, gantt: { useMaxWidth: false },
  fontFamily: "Arial, sans-serif" });
async function toPng(svgText) {
  const doc = new DOMParser().parseFromString(svgText, "image/svg+xml");
  const svg = doc.documentElement;
  const vb = (svg.getAttribute("viewBox") || "0 0 800 600").split(/[\\s,]+/).map(Number);
  const w = Math.ceil(vb[2]), h = Math.ceil(vb[3]);
  svg.setAttribute("width", w); svg.setAttribute("height", h); svg.removeAttribute("style");
  const data = new XMLSerializer().serializeToString(svg);
  const img = new Image();
  img.src = "data:image/svg+xml;base64," + btoa(unescape(encodeURIComponent(data)));
  await img.decode();
  const c = document.createElement("canvas"); c.width = w * 2; c.height = h * 2;
  const g = c.getContext("2d"); g.fillStyle = "#ffffff"; g.fillRect(0, 0, c.width, c.height);
  g.scale(2, 2); g.drawImage(img, 0, 0, w, h);
  return await new Promise((r) => c.toBlob(r, "image/png"));
}
(async () => {
  let ok = 0;
  for (const [i, job] of JOBS.entries()) {
    try {
      const { svg } = await mermaid.render("d" + i, job.src);
      const png = await toPng(svg);
      await fetch("/save/" + job.key, { method: "POST", body: png });
      ok++; log("saved " + job.key);
    } catch (e) {
      log("FAILED " + job.key + ": " + e);
      await fetch("/fail/" + job.key, { method: "POST", body: String(e) });
    }
  }
  log("done: " + ok + " of " + JOBS.length);
  await fetch("/done", { method: "POST", body: "" });
})();
</script></body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--port", type=int, default=8765)
    a = ap.parse_args()
    folder = Path(a.folder)
    out = folder / "assets" / "diagrams"
    out.mkdir(parents=True, exist_ok=True)
    jobs = [{"key": k, "src": s} for k, s in blocks(folder)]
    keep = {j["key"] for j in jobs}
    for old in out.glob("*.png"):
        if old.stem not in keep:
            old.unlink()
    page = (PAGE % {"mermaid": MERMAID_URL,
                    "jobs": json.dumps(jobs).replace("</", "<\\/")}).encode("utf-8")
    failed = []

    class H(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(page)

        def do_POST(self):
            body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            parts = self.path.strip("/").split("/")
            if parts[0] == "save" and len(parts) == 2 and re.fullmatch(r"[0-9a-f]{16}", parts[1]):
                (out / (parts[1] + ".png")).write_bytes(body)
            elif parts[0] == "fail":
                failed.append(f"{parts[-1]}: {body.decode('utf-8', 'replace')}")
            self.send_response(204)
            self.end_headers()
            if parts[0] == "done":
                threading.Thread(target=srv.shutdown).start()

    srv = ThreadingHTTPServer(("127.0.0.1", a.port), H)
    print(f"{len(jobs)} diagrams. Open http://127.0.0.1:{a.port}/ in a browser.", flush=True)
    srv.serve_forever()
    print(f"saved {len(jobs) - len(failed)} of {len(jobs)} to {out}")
    for f in failed:
        print("FAILED", f)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
