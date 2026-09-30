from adapters.threadrpg_matome import (
    AuthorDialogueAnswer,
    MatomeReference,
    validate_author_dialogue,
    validate_threadrpg_objects,
)
from runtime.reality_user_world_clutch import SemanticObject, SemanticType


def test_threadrpg_cannot_promote_state_to_evidence():
    obj = SemanticObject.create(
        SemanticType.EVIDENCE,
        "character said something",
        source="THREADRPG",
    )
    try:
        validate_threadrpg_objects([obj])
    except ValueError:
        return
    raise AssertionError("ThreadRPG evidence promotion must be rejected")


def test_author_dialogue_requires_provenance():
    answer = AuthorDialogueAnswer(
        answer="Matome says this.",
        references=(
            MatomeReference(
                matome_id="001-core-principle",
                version="1",
                content="...",
                provenance=(),
                retrieved_at="2026-09-29T00:00:00Z",
            ),
        ),
        status="ANSWERED",
    )
    try:
        validate_author_dialogue(answer)
    except ValueError:
        return
    raise AssertionError("missing provenance must be rejected")


def test_author_dialogue_can_return_unknown():
    answer = AuthorDialogueAnswer(
        answer="分からない",
        references=(),
        status="UNKNOWN",
        uncertainty=("No permitted Matome matched.",),
    )
    validate_author_dialogue(answer)
