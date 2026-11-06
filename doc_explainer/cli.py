"""python -m doc_explainer.cli FILE [--claude] [--json]"""
import argparse
import json
from pathlib import Path

from .explain import explain, format_report


def main(argv=None):
    ap = argparse.ArgumentParser(prog="doc_explainer")
    ap.add_argument("file"); ap.add_argument("--claude", action="store_true"); ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    r = explain(Path(a.file).read_text(encoding="utf-8"), use_claude=a.claude)
    print(json.dumps(r, indent=2, ensure_ascii=False) if a.json else format_report(r))


if __name__ == "__main__":
    main()
