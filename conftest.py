import os
import pytest
from playwright.sync_api import sync_playwright
from framework.api_client import ProjectsApiClient
from framework.settings import settings


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chromium")
    parser.addoption("--device", action="store", default="desktop")


@pytest.fixture(scope="session")
def browser_name(request):
    return request.config.getoption("--browser")


@pytest.fixture
def page(browser_name, request):
    device = request.config.getoption("--device")
    viewport = {"width": 390, "height": 844} if device == "mobile-web" else {"width": 1440, "height": 900}
    with sync_playwright() as p:
        browser = getattr(p, browser_name).launch(headless=True)
        context = browser.new_context(
            viewport=viewport,
            is_mobile=device == "mobile-web",
            has_touch=device == "mobile-web",
        )
        current_page = context.new_page()
        current_page.set_default_timeout(settings.ui_timeout_ms)
        try:
            yield current_page
        finally:
            context.close()
            browser.close()


@pytest.fixture
def api_client():
    with sync_playwright() as p:
        request_context = p.request.new_context()
        try:
            yield ProjectsApiClient(request_context, settings.api_base_url)
        finally:
            request_context.dispose()


@pytest.fixture
def company1_user():
    return {
        "tenant": "company1",
        "email": os.environ["COMPANY1_EMAIL"],
        "password": os.environ["COMPANY1_PASSWORD"],
        "token": os.environ.get("COMPANY1_API_TOKEN", ""),
    }


@pytest.fixture
def company2_user():
    return {
        "tenant": "company2",
        "email": os.environ["COMPANY2_EMAIL"],
        "password": os.environ["COMPANY2_PASSWORD"],
        "token": os.environ.get("COMPANY2_API_TOKEN", ""),
    }
