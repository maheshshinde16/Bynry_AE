import pytest
from playwright.sync_api import expect
from framework.pages import LoginPage
from framework.settings import settings


@pytest.mark.ui
@pytest.mark.smoke
def test_company1_user_can_log_in(page, company1_user):
    login = LoginPage(page, settings.ui_timeout_ms)
    login.open(settings.web_base_url)
    login.login(company1_user["email"], company1_user["password"])
    expect(page.get_by_test_id("welcome-message")).to_be_visible()


@pytest.mark.ui
@pytest.mark.tenant_isolation
def test_company2_user_sees_company2_tenant_context(page, company2_user):
    login = LoginPage(page, settings.ui_timeout_ms)
    login.open(settings.web_base_url)
    login.login(company2_user["email"], company2_user["password"])
    expect(page.get_by_test_id("active-tenant")).to_have_text("Company2")
