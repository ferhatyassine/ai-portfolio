"""Grounding check: does a draft answer claim skills or numbers that are NOT in your profile?
Use it on anything you (or an AI) wrote before saying it in an interview."""
import re

from .skills import find_skills


def check_claims(draft, profile):
    pool = " ".join(
        [" ".join(profile.get("skills", []))] +
        [" ".join(str(v) for k, v in e.items() if not k.startswith("_")) for e in profile.get("experiences", [])])
    ok_nums = set(re.findall(r"\d+(?:[.,]\d+)?", pool))
    unsupported_skills = [s for s in find_skills(draft) if s not in profile["_skills"]]
    unsupported_nums = [n for n in re.findall(r"\d+(?:[.,]\d+)?", draft) if n not in ok_nums]
    flags = ([f"Skill not in your profile: {s}" for s in unsupported_skills]
             + [f"Number not in your profile: {n}" for n in unsupported_nums])
    return {"grounded": not flags, "flags": flags}
