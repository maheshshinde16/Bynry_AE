"""Page objects use accessible locators and stable test IDs."""
import re
from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page, timeout_ms: int) -> None:
        self.page = page
        self.timeout_ms = timeout_ms

    def open(self, base_url: str) -> None:
        self.page.goto(f"{base_url.rstrip('/')}/login", wait_until="domcontentloaded")
        expect(self.page.get_by_test_id("login-form")).to_be_visible(timeout=self.timeout_ms)

    def login(self, email: str, password: str) -> None:
        self.page.get_by_label("Email").fill(email)
        self.page.get_by_label("Password").fill(password)
        self.page.get_by_role("button", name="Sign in").click()
        expect(self.page).to_have_url(re.compile(r".*/dashboard(?:\?.*)?$"), timeout=self.timeout_ms)
        expect(self.page.get_by_test_id("dashboard-ready")).to_be_visible(timeout=self.timeout_ms)


class ProjectsPage:
    def __init__(self, page: Page, timeout_ms: int) -> None:
        self.page = page
        self.timeout_ms = timeout_ms

    def open(self) -> None:
        self.page.get_by_role("link", name="Projects").click()
        expect(self.page.get_by_test_id("projects-list")).to_be_visible(timeout=self.timeout_ms)

    def project_card(self, project_id: int):
        return self.page.get_by_test_id(f"project-card-{project_id}")
