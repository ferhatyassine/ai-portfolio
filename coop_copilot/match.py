"""Compare a job offer to the profile: what is covered, what is a gap (stated honestly)."""
from .skills import find_skills


def match(offer_text, profile):
    wanted = find_skills(offer_text)
    have = set(profile["_skills"])
    covered, gaps = [], []
    for s in wanted:
        if s in have:
            evidence = [e["title"] for e in profile.get("experiences", []) if s in e["_skills"]]
            covered.append({"skill": s, "evidence": evidence})
        else:
            gaps.append(s)
    pct = round(100 * len(covered) / len(wanted)) if wanted else 0
    return {"requested": wanted, "covered": covered, "gaps": gaps, "coverage_pct": pct,
            "advice": [f"'{g}' is not in your profile: say you are learning it only if true, and name a concrete step."
                       for g in gaps]}
