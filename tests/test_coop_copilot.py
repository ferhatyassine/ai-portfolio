from coop_copilot import match, load_profile, star_answer, check_claims

P = load_profile("examples/profile.example.json")
OFFER = open("examples/offer.txt", encoding="utf-8").read()


def test_match_reports_covered_and_honest_gaps():
    r = match(OFFER, P)
    covered = {c["skill"] for c in r["covered"]}
    assert {"python", "sql", "git"} <= covered
    assert "docker" in r["gaps"] and "generative ai" in r["gaps"]
    assert 0 < r["coverage_pct"] < 100


def test_star_uses_own_experience():
    a = star_answer("Tell me about a disagreement in your team", P)
    assert a["found"] and "database" in a["experience"].lower()


def test_star_refuses_to_invent():
    a = star_answer("Describe leading a 50-person Kubernetes migration", P)
    assert a["found"] is False


def test_grounding_flags_invented_claims():
    r = check_claims("I used Docker and cut load time by 80% on AWS.", P)
    assert not r["grounded"] and any("docker" in f.lower() for f in r["flags"])
    assert check_claims("I used SQL to compare two designs.", P)["grounded"]


class _FakeClient:
    def __init__(self, text):
        self.messages = self
        self._t = text

    def create(self, **kw):
        assert "STRICT RULES" in kw["system"]
        return type("M", (), {"content": [type("B", (), {"text": self._t})()]})()


def test_claude_adapter_passes_grounded_and_flags_invented():
    from coop_copilot.claude_adapter import polish
    a = star_answer("Tell me about a disagreement in your team", P)
    good = polish("q", a, P, client=_FakeClient("I used SQL to compare two designs with my team."))
    assert good["grounded"]
    bad = polish("q", a, P, client=_FakeClient("I used Docker and improved speed by 80%."))
    assert not bad["grounded"] and bad["flags"]
