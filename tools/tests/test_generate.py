from corpus import generate, spec


def test_q1_produces_the_expected_volume():
    tickets = generate.build_tickets("q1")
    assert len(tickets) == spec.Q1_TICKET_COUNT


def test_generation_is_deterministic():
    first = generate.build_tickets("q1")
    second = generate.build_tickets("q1")
    assert [t.body for t in first] == [t.body for t in second], (
        "the corpus must regenerate identically or the answer key goes stale"
    )


def test_q2_produces_the_expected_volume():
    assert len(generate.build_tickets("q2")) == spec.Q2_TICKET_COUNT


def test_writes_one_file_per_ticket(tmp_path):
    written = generate.write_corpus("q1", tmp_path)
    assert written == spec.Q1_TICKET_COUNT
    assert len(list(tmp_path.glob("ticket-*.txt"))) == spec.Q1_TICKET_COUNT


def test_subject_survives_an_empty_body():
    """Truncation can leave nothing behind; that must not kill generation."""
    assert generate._subject_from("") == "(no subject)"
    assert generate._subject_from("   \n  ") == "(no subject)"


def test_rendered_ticket_carries_the_header_fields():
    ticket = generate.build_tickets("q1")[0]
    rendered = generate.render(ticket)
    for field in ("Ticket: NUS-", "Date: ", "Channel: ", "Subject: "):
        assert field in rendered, f"rendered ticket is missing {field!r}"


def test_write_corpus_clears_stale_tickets(tmp_path):
    """Regenerating after a count change must not leave orphans behind."""
    (tmp_path / "ticket-9999.txt").write_text("stale", encoding="utf-8")
    generate.write_corpus("q2", tmp_path)
    assert not (tmp_path / "ticket-9999.txt").exists()
