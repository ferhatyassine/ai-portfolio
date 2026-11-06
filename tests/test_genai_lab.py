from genai_lab import redact, has_pii, score, compare, extractive_summary


def test_redacts_common_pii():
    t = "Mail jane.doe@example.com or call 613-555-0142. SIN 123 456 789, postal K1A 0B1."
    clean, found = redact(t)
    assert "jane.doe" not in clean and "555-0142" not in clean and "123 456 789" not in clean
    assert {"EMAIL", "PHONE", "SIN", "POSTAL"} <= set(found)


def test_clean_text_untouched():
    assert not has_pii("Generative AI needs human review.")


def test_score_identical_is_perfect():
    s = score("the model needs review", "the model needs review")
    assert s["rouge1_f"] == 1.0 and s["key_term_coverage"] == 1.0


def test_compare_ranks_closer_summary_first():
    ref = "Humans must review AI output for accuracy."
    rows = compare({"good": "Humans review AI output for accuracy.", "bad": "Cats like warm boxes."}, ref)
    assert rows[0][0] == "good"


def test_extractive_summary_shorter_than_source():
    text = ("AI tools help teams. AI tools need review. Review keeps AI tools accurate. "
            "The weather was nice. Teams document AI tools.")
    assert len(extractive_summary(text, 2)) < len(text)
