"""Build a STAR answer skeleton from YOUR experience that best fits the question.
If nothing in the profile fits, it says so instead of inventing a story."""
import re

from .skills import find_skills

THEMES = {
    "conflict": ["conflict", "disagree", "disagreement", "désaccord"],
    "deadline": ["deadline", "time", "pressure", "échéance"],
    "learning": ["learn", "new", "unfamiliar", "apprendre"],
    "initiative": ["initiative", "without being asked", "proactive"],
    "feedback": ["feedback", "criticism", "rétroaction"],
    "teamwork": ["team", "collaborat", "group", "équipe"],
    "problem": ["problem", "bug", "troubleshoot", "fix", "challenge", "difficult"],
}


def _words(t):
    return set(re.findall(r"[a-zà-ÿ#.+]{3,}", t.lower()))


def _score(question, exp):
    q = _words(question)
    s = 0
    for theme, kws in THEMES.items():
        if any(k in question.lower() for k in kws):
            s += 2 * len(set(exp.get("themes", [])) & {theme})
    s += len(q & _words(exp.get("title", "") + " " + exp.get("situation", "")))
    s += len(set(find_skills(question)) & set(exp["_skills"]))
    return s


def star_answer(question, profile, min_score=2):
    ranked = sorted(profile.get("experiences", []), key=lambda e: _score(question, e), reverse=True)
    if not ranked or _score(question, ranked[0]) < min_score:
        return {"found": False, "message": "No experience in your profile fits this question. "
                "Do not invent one: add a real example to your profile, or answer with a related true story."}
    e = ranked[0]
    return {"found": True, "experience": e["title"],
            "star": {"Situation": e.get("situation", ""), "Task": e.get("task", ""),
                     "Action": e.get("action", ""), "Result": e.get("result", "")},
            "tips": ["Say 'I', not 'we', for your own actions.", "End with a measurable or concrete result.",
                     "Keep it under 90 seconds."]}


def render(ans):
    if not ans["found"]:
        return ans["message"]
    out = [f"Best story: {ans['experience']}"] + [f"{k}: {v}" for k, v in ans["star"].items() if v]
    return "\n".join(out + [""] + [f"- {t}" for t in ans["tips"]])
