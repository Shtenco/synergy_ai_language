from ai_language.semantic_trace import build_semantic_trace
from ai_language.synergy_contracts import CONTRACT_ID, requirement_trace_payload


def test_requirement_trace_contract_comes_from_real_semantic_trace(tmp_path):
    trace=build_semantic_trace(
        "Implement feature; validate with tests",
        ["src/a.py","tests/test_a.py"],
        repository_root=tmp_path,
    )
    req=trace.requirements[0]
    trace.record(
        "write_file",
        {"path":"src/a.py","requirement_ids":[req.id]},
        "OK: wrote file",
    )
    trace.record(
        "run_command",
        {"command":"pytest","requirement_ids":[req.id]},
        "OK: tests passed",
    )
    payloads=requirement_trace_payload(
        trace,
        affected_repositories=["Shtenco/synergy_ai_language"],
    )
    assert CONTRACT_ID=="synergy.engineering.requirement-trace/v1"
    assert payloads[0]["requirement_id"].startswith("REQ-")
    assert payloads[0]["status"]=="VERIFIED"
