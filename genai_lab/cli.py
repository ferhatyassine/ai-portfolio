"""CLI.  python -m genai_lab.cli redact FILE | summarize FILE [--claude] | compare REF FILE [FILE...]"""
import argparse
import sys
from pathlib import Path

from .evaluate import compare
from .pii import redact
from .summarize import claude_summary, extractive_summary


def main(argv=None):
    ap = argparse.ArgumentParser(prog="genai_lab")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("redact"); p.add_argument("file")
    p = sub.add_parser("summarize"); p.add_argument("file"); p.add_argument("--claude", action="store_true")
    p = sub.add_parser("compare"); p.add_argument("reference"); p.add_argument("candidates", nargs="+")
    a = ap.parse_args(argv)

    if a.cmd == "redact":
        clean, found = redact(Path(a.file).read_text(encoding="utf-8"))
        print(clean)
        print(f"-- redacted: {found or 'nothing found'}", file=sys.stderr)
    elif a.cmd == "summarize":
        text = Path(a.file).read_text(encoding="utf-8")
        print(claude_summary(text) if a.claude else extractive_summary(redact(text)[0]))
    else:
        ref = Path(a.reference).read_text(encoding="utf-8")
        cands = {Path(f).name: Path(f).read_text(encoding="utf-8") for f in a.candidates}
        for name, s in compare(cands, ref):
            print(f"{name:30s} {s}")


if __name__ == "__main__":
    main()
