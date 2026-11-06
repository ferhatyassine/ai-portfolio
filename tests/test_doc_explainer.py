from doc_explainer import explain
from doc_explainer.extract import find_dates, find_amounts, find_actions
from doc_explainer.factguard import check

NOTICE = open("examples/notice.txt", encoding="utf-8").read()


def test_extracts_core_facts():
    assert "March 31, 2026" in find_dates(NOTICE)
    assert "$1,250.00" in find_amounts(NOTICE)
    assert any(a["has_deadline"] for a in find_actions(NOTICE))


def test_french_extraction():
    t = "Vous devez payer 1 250,00 $ avant le 31 mars 2026."
    assert find_dates(t) == ["31 mars 2026"] and find_amounts(t)


def test_pipeline_masks_pii_and_reports():
    r = explain(NOTICE)
    blob = str(r)
    assert "jane.doe@example.com" not in blob and "123 456 789" not in blob and "555-0142" not in blob
    assert r["urgent"] and not r["warnings"]


def test_fact_guard_catches_changed_amount_and_date():
    bad = check("You owe $1,520.00 by April 2, 2026.", NOTICE)
    assert "$1,520.00" in bad and "April 2, 2026" in bad
    assert check("You owe $1,250.00 by March 31, 2026.", NOTICE) == []
