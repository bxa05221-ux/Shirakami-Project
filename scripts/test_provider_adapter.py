from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from provider_adapter import ProviderAdapter, RuntimeRequest, RuntimeResult


class FakeProvider(ProviderAdapter):
    @property
    def provider_name(self):
        return "fake"

    def execute(self, request):
        return RuntimeResult(
            handoff_id=request.handoff_id,
            trace_id=request.trace_id,
            execution_id=request.execution_id,
            provider=self.provider_name,
            output={"ok": True},
            protocol_ids=request.protocol_ids,
            evidence_ids=request.evidence_ids,
        )


class AlternateProvider(ProviderAdapter):
    @property
    def provider_name(self):
        return "alternate"

    def execute(self, request):
        return RuntimeResult(
            handoff_id=request.handoff_id,
            trace_id=request.trace_id,
            execution_id=request.execution_id,
            provider=self.provider_name,
            output={"ok": False, "provider_specific": True},
            protocol_ids=request.protocol_ids,
            evidence_ids=request.evidence_ids,
        )


def request():
    return RuntimeRequest(
        handoff_id="SH-001",
        trace_id="TR-001",
        execution_id="EX-001",
        project="demo",
        objective="adapter test",
        protocol_ids=("P-001",),
        evidence_ids=("E-001",),
        verification_scope="unit",
        input_data={"message": "hello"},
        runtime_target="fake",
    )


def test_provider_is_replaceable():
    result = FakeProvider().execute(request())
    assert result.provider == "fake"
    assert result.handoff_id == "SH-001"
    assert result.protocol_ids == ("P-001",)
    assert result.evidence_ids == ("E-001",)


def test_provider_swap_preserves_lineage_and_authority():
    providers = [FakeProvider(), AlternateProvider()]
    results = [provider.execute(request()) for provider in providers]

    assert [result.provider for result in results] == ["fake", "alternate"]
    assert [(result.handoff_id, result.trace_id, result.execution_id, result.protocol_ids, result.evidence_ids)
            for result in results] == [
                ("SH-001", "TR-001", "EX-001", ("P-001",), ("E-001",)),
                ("SH-001", "TR-001", "EX-001", ("P-001",), ("E-001",)),
            ]

    for provider, result in zip(providers, results):
        provider.validate_result(result)
        assert result.execution_authorized is False
        assert result.publish_authorized is False
        assert result.merge_authorized is False
        assert result.human_gate_required is True


def test_provider_result_has_no_authority():
    result = FakeProvider().execute(request())
    FakeProvider().validate_result(result)
    assert result.execution_authorized is False
    assert result.publish_authorized is False
    assert result.merge_authorized is False
    assert result.human_gate_required is True


@pytest.mark.parametrize(
    "field",
    ["execution_authorized", "publish_authorized", "merge_authorized"],
)
def test_authority_cannot_cross_provider_boundary(field):
    values = {
        "handoff_id": "SH-001",
        "trace_id": "TR-001",
        "execution_id": "EX-001",
        "provider": "fake",
        "output": {},
        "protocol_ids": ("P-001",),
        "evidence_ids": ("E-001",),
    }
    values[field] = True
    result = RuntimeResult(**values)
    with pytest.raises(ValueError, match="authority"):
        FakeProvider().validate_result(result)


def test_human_gate_cannot_be_removed():
    values = {
        "handoff_id": "SH-001",
        "trace_id": "TR-001",
        "execution_id": "EX-001",
        "provider": "fake",
        "output": {},
        "protocol_ids": ("P-001",),
        "evidence_ids": ("E-001",),
        "human_gate_required": False,
    }
    result = RuntimeResult(**values)
    with pytest.raises(ValueError, match="human_gate_required"):
        FakeProvider().validate_result(result)
