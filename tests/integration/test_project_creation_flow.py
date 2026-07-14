import uuid
import pytest
from playwright.sync_api import expect
from framework.pages import LoginPage, ProjectsPage
from framework.settings import settings


@pytest.mark.integration
@pytest.mark.tenant_isolation
def test_project_created_by_api_is_visible_only_to_its_tenant(
    page, api_client, company1_user, company2_user
):
    """Create through API, verify Company1 UI, and deny Company2 API access."""
    payload = {
        "name": f"integration-project-{uuid.uuid4().hex[:8]}",
        "description": "Created by automated integration coverage",
        "team_members": [],
    }
    project_id = None
    try:
        create_response = api_client.create_project(
            company1_user["token"], company1_user["tenant"], payload
        )
        assert create_response.status == 201, create_response.text()
        project_id = create_response.json()["id"]

        login = LoginPage(page, settings.ui_timeout_ms)
        login.open(settings.web_base_url)
        login.login(company1_user["email"], company1_user["password"])
        projects = ProjectsPage(page, settings.ui_timeout_ms)
        projects.open()

        card = projects.project_card(project_id)
        expect(card).to_be_visible()
        expect(card).to_contain_text(payload["name"])
        expect(card).to_have_attribute("data-tenant-id", company1_user["tenant"])

        denied = api_client.get_project(
            company2_user["token"], company2_user["tenant"], project_id
        )
        assert denied.status in (403, 404), "Cross-tenant project access must be denied"
    finally:
        if project_id is not None:
            cleanup = api_client.delete_project(
                company1_user["token"], company1_user["tenant"], project_id
            )
            assert cleanup.status in (200, 204), cleanup.text()
