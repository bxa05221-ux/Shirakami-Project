from joumon_matome_loader import load_matome_mapping


def make_document():
    return {
        "matome": {
            "codename": "JOUMON",
            "version": "0.1",
            "statement": "Connect meaning across replaceable AI runtimes.",
        },
        "purpose": {"primary": ["preserve context", "preserve evidence"]},
        "human_gate": {"input": ["Evidence", "Verification"]},
    }


def test_matome_becomes_protocol_input():
    context, protocol = load_matome_mapping(make_document())
    assert context.context_id.startswith("matome:0.1:JOUMON")
    assert protocol.input_context_id == context.context_id
    assert "preserve context" in make_document()["purpose"]["primary"]


def test_non_joumon_document_is_rejected():
    document = make_document()
    document["matome"]["codename"] = "OTHER"
    try:
        load_matome_mapping(document)
    except ValueError:
        pass
    else:
        raise AssertionError("unsupported Matome must be rejected")
