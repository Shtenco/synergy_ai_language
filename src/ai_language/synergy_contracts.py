from __future__ import annotations

from typing import Any

from .semantic_trace import SemanticTrace


CONTRACT_ID = "synergy.engineering.requirement-trace/v1"
AUTHORITY = "requirements_semantics"


def requirement_trace_payload(
    trace: SemanticTrace,
    *,
    affected_repositories: list[str],
) -> list[dict[str, Any]]:
    coverage = {item.requirement_id: item for item in trace.coverage()}
    events_by_requirement: dict[str, list] = {
        req.id: [e for e in trace.events if req.id in e.requirement_ids]
        for req in trace.requirements
    }
    payloads: list[dict[str, Any]] = []
    for req in trace.requirements:
        cov = coverage[req.id]
        validation_targets = [
            event.target
            for event in events_by_requirement[req.id]
            if event.tool == "run_command" and event.status == "ok" and event.target
        ]
        change_refs = [
            f"event:{event.index}:{event.tool}:{event.target}"
            for event in events_by_requirement[req.id]
            if event.status == "ok"
        ]
        status_map = {
            "unresolved": "OPEN",
            "addressed": "IMPLEMENTED",
            "implemented": "IMPLEMENTED",
            "verified": "VERIFIED",
        }
        payloads.append(
            {
                "requirement_id": req.id,
                "statement": req.text,
                "affected_repositories": list(affected_repositories),
                "validation_targets": validation_targets,
                "status": status_map.get(cov.status, "OPEN"),
                "change_refs": change_refs,
            }
        )
    return payloads
