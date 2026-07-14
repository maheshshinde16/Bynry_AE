import uuid
import pytest


@pytest.mark.api
def test_create_project_returns_active_project(api_client, company1_user):
    payload = {
        "name": f"api-smoke-{uuid.uuid4().hex[:8]}",
        "description": "Temporary API smoke-test project",
        "team_members": [],
    }
    project_id = None
    try:
        response = api_client.create_project(company1_user["token"], company1_user["tenant"], payload)
        assert response.status == 201, response.text()
        body = response.json()
        project_id = body["id"]
        assert body["name"] == payload["name"]
        assert body["status"] == "active"
    finally:
        if project_id is not None:
            cleanup = api_client.delete_project(company1_user["token"], company1_user["tenant"], project_id)
            assert cleanup.status in (200, 204), cleanup.text()
