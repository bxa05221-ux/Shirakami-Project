from datetime import datetime, timezone

import pytest

from runtime.reality_user_world_clutch import (
    MemoryStatus,
    SemanticObject,
    SemanticType,
    TemporalMemory,
    build_clutch,
    classify_user_statement,
    reopen_frame,
    verify_clutch,
)


def obj(kind, text):
    return SemanticObject.create(
        kind,
        text,
        timestamp=datetime(2026, 9, 29, tzinfo=timezone.utc),
    )


def test_dream_is_not_evidence():
    dream = obj(SemanticType.DREAM, "プロ野球選手になりたい")
    evidence = obj(SemanticType.EVIDENCE, "現在確認された練習環境")
    clutch = build_clutch([evidence], [dream])
    assert clutch.user_world[0].semantic_type is SemanticType.DREAM
    assert clutch.reality[0].semantic_type is SemanticType.EVIDENCE
    assert verify_clutch(clutch, decision_owner="HUMAN").status == "PASS"


def test_past_dream_is_not_current_dream():
    memory = TemporalMemory()
    first = obj(SemanticType.DREAM, "プロ野球選手になりたい")
    second = obj(SemanticType.DREAM, "野球を楽しみたい")
    memory.store(first)
    memory.store(second)
    assert memory.current(SemanticType.DREAM).content == "野球を楽しみたい"
    assert memory.history(SemanticType.DREAM)[0].status is MemoryStatus.HISTORICAL


def test_unknown_presence_is_preserved_as_user_world():
    presence = obj(SemanticType.PRESENCE, "本人にとって重要な象徴的存在")
    clutch = build_clutch([], [presence])
    assert clutch.user_world[0].semantic_type is SemanticType.PRESENCE
    assert clutch.user_world[0].semantic_type is not SemanticType.EVIDENCE


def test_frame_reopening_exposes_unasked_questions():
    review = reopen_frame(
        current_frame="子供の進路選択",
        assumptions=["成功は一つの職業で定義できる"],
        excluded_regions=["本人が将来価値観を変える可能性"],
        unasked_questions=["本人にとって何が大切なのか"],
        triggers=["user_correction"],
    )
    assert review.current_frame == "子供の進路選択"
    assert review.unasked_questions


def test_non_human_decision_owner_fails():
    dream = obj(SemanticType.DREAM, "将来こうなりたい")
    evidence = obj(SemanticType.EVIDENCE, "現在の状況")
    clutch = build_clutch([evidence], [dream])
    result = verify_clutch(clutch, decision_owner="AI")
    assert result.status == "FAIL"
    assert "NON_HUMAN_DECISION_OWNER" in result.violations


def test_automatic_classification_defaults_to_unknown():
    result = classify_user_statement("これは夢かもしれない")
    assert result.semantic_type is SemanticType.UNKNOWN


def test_invalid_side_assignment_is_rejected():
    evidence = obj(SemanticType.EVIDENCE, "事実")
    with pytest.raises(ValueError):
        build_clutch([evidence], [evidence])
