def create_api_finding(client):
    owner = client.post(
        "/owners",
        json={
            "display_name": "Maya Johnson",
            "email": "maya.johnson@county.example",
            "department": "County IT",
            "role": "AI assurance operator",
        },
    ).json()
    system = client.post(
        "/systems",
        json={
            "system_name": "Public Benefits Chatbot",
            "department_owner": "Health and Human Services",
            "business_purpose": "Answers public benefits questions.",
            "public_facing": True,
            "rights_impacting": True,
            "uses_pii": True,
            "deployment_environment": "pilot",
            "risk_tier": "high",
            "approval_status": "under_review",
        },
    ).json()
    assessment = client.post(
        "/assessments",
        json={
            "system_id": system["id"],
            "assessment_type": "AI assurance baseline",
            "initiated_by": "Maya Johnson",
        },
    ).json()
    finding = client.post(
        "/findings",
        json={
            "system_id": system["id"],
            "assessment_id": assessment["id"],
            "scanner_name": "manual-review",
            "scanner_version": "0.1.0",
            "domain": "security",
            "severity": "high",
            "confidence": "medium",
            "title": "Prompt injection vulnerability",
            "description": "Unsafe instruction override was observed.",
            "evidence_summary": "Prompt and response demonstrate override behavior.",
            "remediation": "Add prompt injection tests and tool gating.",
            "owner_id": owner["id"],
            "score_impact": {"security": -8},
            "actor": "Maya Johnson",
        },
    ).json()
    return system, assessment, finding


def test_api_route_smoke_flow(client):
    health = client.get("/health")
    assert health.status_code == 200

    system, assessment, finding = create_api_finding(client)

    assert client.get("/systems").status_code == 200
    assert client.get(f"/systems/{system['id']}").status_code == 200
    assert client.get("/assessments").status_code == 200
    assert client.get(f"/assessments/{assessment['id']}").status_code == 200
    assert client.get("/findings").status_code == 200
    assert client.get(f"/findings/{finding['id']}").status_code == 200

    transition = client.post(
        f"/findings/{finding['id']}/transition",
        json={"status": "under_review", "actor": "Maya Johnson"},
    )
    assert transition.status_code == 200
    assert transition.json()["status"] == "under_review"

    evidence = client.post(
        "/evidence",
        json={
            "finding_id": finding["id"],
            "evidence_type": "prompt",
            "title": "Prompt evidence",
            "raw_text": "Ignore previous instructions.",
            "content_type": "text/plain",
            "created_by": "Maya Johnson",
        },
    )
    assert evidence.status_code == 201
    assert client.get("/evidence").status_code == 200
    assert client.get(f"/evidence/{evidence.json()['id']}").status_code == 200

    retest = client.post(
        f"/findings/{finding['id']}/retest",
        json={"initiated_by": "Maya Johnson", "notes": "Ready to validate."},
    )
    assert retest.status_code == 201
    assert client.get(f"/retests/{retest.json()['id']}").status_code == 200
    assert (
        client.patch(
            f"/retests/{retest.json()['id']}",
            json={"status": "passed", "actor": "Maya Johnson"},
        ).status_code
        == 200
    )

    airb = client.post(
        "/airb-reviews",
        json={
            "system_id": system["id"],
            "assessment_id": assessment["id"],
            "review_status": "pending",
            "actor": "Maya Johnson",
        },
    )
    assert airb.status_code == 201
    assert client.get("/airb-reviews").status_code == 200
    assert (
        client.patch(
            f"/airb-reviews/{airb.json()['id']}",
            json={
                "review_status": "under_review",
                "decision_notes": "Board review started.",
                "actor": "Maya Johnson",
            },
        ).status_code
        == 200
    )

    audit_events = client.get("/audit-events")
    assert audit_events.status_code == 200
    assert len(audit_events.json()) >= 6


def test_patch_finding_rejects_direct_status_mutation(client):
    _, _, finding = create_api_finding(client)
    response = client.patch(
        f"/findings/{finding['id']}",
        json={"status": "closed", "actor": "Maya Johnson"},
    )
    assert response.status_code == 422


def test_system_creation_accepts_target_configuration_and_validates_options(client):
    response = client.post(
        "/systems",
        json={
            "system_name": "Internal RAG Assistant",
            "department_owner": "County Manager",
            "business_purpose": "Answers policy questions from approved county documents.",
            "deployment_environment": "pilot",
            "risk_tier": "moderate",
            "approval_status": "under_review",
            "target_type": "rag_endpoint",
            "target_location": "http://internal-api:8000/rag/chat",
            "authentication_type": "api_key",
            "authentication_reference": "County Manager test API key record",
            "assessment_method": "hybrid",
            "scanner_compatible": ["prompt_injection", "rag_integrity"],
            "manual_review_only": False,
            "uploaded_artifact_supported": True,
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["target_type"] == "rag_endpoint"
    assert payload["target_location"] == "http://internal-api:8000/rag/chat"
    assert payload["scanner_compatible"] == ["prompt_injection", "rag_integrity"]

    invalid = client.post(
        "/systems",
        json={
            "system_name": "Invalid Target",
            "department_owner": "County IT",
            "business_purpose": "Invalid target type should fail validation.",
            "target_type": "network_scan",
        },
    )
    assert invalid.status_code == 422
