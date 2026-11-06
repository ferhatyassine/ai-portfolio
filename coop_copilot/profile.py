"""Your profile = your REAL experiences. The copilot never writes anything that is not in here."""
import json
from pathlib import Path

from .skills import find_skills


def load_profile(path):
    p = json.loads(Path(path).read_text(encoding="utf-8"))
    for e in p.get("experiences", []):
        blob = " ".join(str(e.get(k, "")) for k in ("title", "situation", "task", "action", "result", "skills"))
        e["_skills"] = sorted(set(find_skills(blob)) | {s.lower() for s in e.get("skills", [])})
    p["_skills"] = sorted(set(find_skills(" ".join(p.get("skills", []))))
                          | {s.lower() for s in p.get("skills", [])}
                          | {s for e in p.get("experiences", []) for s in e["_skills"]})
    return p
