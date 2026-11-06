"""python -m coop_copilot.cli match OFFER PROFILE | star "QUESTION" PROFILE | check DRAFT PROFILE"""
import argparse
import json
from pathlib import Path

from .grounding import check_claims
from .match import match
from .profile import load_profile
from .star import render, star_answer


def main(argv=None):
    ap = argparse.ArgumentParser(prog="coop_copilot")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("match"); p.add_argument("offer"); p.add_argument("profile")
    p = sub.add_parser("star"); p.add_argument("question"); p.add_argument("profile")
    p.add_argument("--claude", action="store_true"); p.add_argument("--offer")
    p = sub.add_parser("check"); p.add_argument("draft"); p.add_argument("profile")
    a = ap.parse_args(argv)
    prof = load_profile(a.profile)
    if a.cmd == "match":
        r = match(Path(a.offer).read_text(encoding="utf-8"), prof)
        print(f"Coverage: {r['coverage_pct']}%  ({len(r['covered'])}/{len(r['requested'])})")
        for c in r["covered"]:
            print(f"  OK  {c['skill']}  <- {', '.join(c['evidence']) or 'listed skill'}")
        for adv in r["advice"]:
            print("  GAP", adv)
    elif a.cmd == "star":
        ans = star_answer(a.question, prof)
        print(render(ans))
        if a.claude and ans["found"]:
            from .claude_adapter import polish
            offer = Path(a.offer).read_text(encoding="utf-8") if a.offer else ""
            r = polish(a.question, ans, prof, offer)
            print("\n--- Spoken version (Claude) ---\n" + r["text"])
            print("Grounded in your profile." if r["grounded"] else "CHECK BEFORE USING:\n" + "\n".join(r["flags"]))
    else:
        r = check_claims(Path(a.draft).read_text(encoding="utf-8"), prof)
        print("Grounded in your profile." if r["grounded"] else "\n".join(["Check before you say this:"] + r["flags"]))


if __name__ == "__main__":
    main()
