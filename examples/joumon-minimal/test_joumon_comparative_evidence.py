from joumon_provider_contract_poc import run
from joumon_evidence_adapter import to_evidence
from joumon_comparative_evidence import compare

def make_records():
    c,p,results=run()
    return [to_evidence(c.context_id,p.protocol_id,r.runtime_id,r.output,r.metadata) for r in results]

def test_comparison_preserves_all_observations():
    rs=make_records(); view=compare(rs)
    assert len(view.observations)==2
    assert {r.provider for r in view.observations}=={"openai","gemini"}

def test_comparison_requires_common_context_and_protocol():
    rs=make_records()
    bad=rs[1].__class__(rs[1].evidence_id,"other",rs[1].protocol_id,rs[1].runtime_id,rs[1].provider,rs[1].runtime_type,rs[1].mode,rs[1].observed_output)
    try: compare([rs[0],bad])
    except ValueError: pass
    else: raise AssertionError("mismatched Context must be rejected")

def test_comparison_has_no_decision_authority():
    view=compare(make_records())
    assert view.comparison_authority=="non-authoritative"
    assert view.final_decision_authority=="human"

def test_comparison_does_not_rank_observations():
    view=compare(make_records())
    assert not hasattr(view,"winner")
    assert not hasattr(view,"score")
