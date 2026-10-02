from pathlib import Path


MATOME = Path(__file__).with_name("joumon-matome.yaml")


def test_matome_declares_human_final_authority():
    text = MATOME.read_text(encoding="utf-8")
    assert 'final_decision: "human"' in text
    assert 'production_readiness: false' in text


def test_matome_declares_roundtrip_and_provider_neutrality():
    text = MATOME.read_text(encoding="utf-8")
    assert 'provider_neutral: true' in text
    assert 'required: true' in text
    assert 'Semantic Handoff -> Matome' in text
    assert 'Matome -> Semantic Handoff' in text


def test_matome_declares_runtime_replaceability():
    text = MATOME.read_text(encoding="utf-8")
    assert 'Runtime is replaceable.' in text
    assert 'Runtime同士を直接結合するのではなく、共通Semantic Boundaryを介して接続する。' in text
