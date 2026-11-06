"""Tiny local web UI (standard library only). Binds to 127.0.0.1: nothing leaves your machine
except, if you tick the box, the REDACTED text sent to Claude.   python -m doc_explainer.web"""
import html
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

from .explain import explain, format_report

PAGE = """<!doctype html><meta charset=utf-8><title>Document explainer</title>
<body style="font-family:system-ui;max-width:720px;margin:2rem auto;padding:0 1rem">
<h1>Explain my document</h1><p>Paste a letter or notice. Personal data is masked first.</p>
<form method=post><textarea name=text rows=12 style="width:100%">{text}</textarea><br>
<label><input type=checkbox name=claude> Use Claude (sends masked text only; needs API key)</label><br>
<button>Explain</button></form><pre style="white-space:pre-wrap;background:#f4f4f4;padding:1rem">{out}</pre>"""


class H(BaseHTTPRequestHandler):
    def _send(self, text="", out=""):
        body = PAGE.format(text=html.escape(text), out=html.escape(out)).encode()
        self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

    def do_GET(self):
        self._send()

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        form = parse_qs(self.rfile.read(n).decode("utf-8"))
        text = form.get("text", [""])[0]
        try:
            out = format_report(explain(text, use_claude="claude" in form))
        except RuntimeError as e:
            out = f"Error: {e}"
        self._send(text, out)


if __name__ == "__main__":
    print("Open http://127.0.0.1:8000")
    HTTPServer(("127.0.0.1", 8000), H).serve_forever()
