from pathlib import Path
import yaml

from record_codex_result import main


def test_result_is_recorded_without_changing_authority(tmp_path, monkeypatch, capsys):
    source = tmp_path / "result.yaml"
    output = tmp_path / "recorded.yaml"
    source.write_text(yaml.safe_dump({
        "codex_result": {
            "version": "0.1",
            "source_handoff_id": "SH-HO-20260925-001",
            "status": "completed",
            "result": {
                "changed_paths": ["scripts/example.py"],
                "observations": ["test fixture"],
                "deviations": [],
            },
            "verification": {"status": "passed", "tests": ["pytest"]},
            "commit": "abc123",
            "unresolved": [],
            "authority": {
                "execution_authorized": False,
                "publish_authorized": False,
                "merge_authorized": False,
            },
            "human_gate": {"required": True, "decision": "pending"},
        }
    }, allow_unicode=True), encoding="utf-8")

    monkeypatch.setattr("sys.argv", [
        "record_codex_result.py", str(source), "-o", str(output)
    ])
    assert main() == 0

    recorded = yaml.safe_load(output.read_text(encoding="utf-8"))
    authority = recorded["codex_result"]["authority"]
    assert authority["execution_authorized"] is False
    assert authority["publish_authorized"] is False
    assert authority["merge_authorized"] is False
    assert recorded["codex_result"]["human_gate"]["decision"] == "pending"
    assert "Result does not grant" in capsys.readouterr().out
