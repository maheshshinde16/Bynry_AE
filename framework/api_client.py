"""API wrapper that keeps request construction out of tests."""
from playwright.sync_api import APIRequestContext, APIResponse


class ProjectsApiClient:
    def __init__(self, request: APIRequestContext, api_base_url: str) -> None:
        self.request = request
        self.api_base_url = api_base_url.rstrip("/")

    @staticmethod
    def _headers(token: str, tenant_id: str) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": tenant_id,
            "Content-Type": "application/json",
        }

    def create_project(self, token: str, tenant_id: str, payload: dict) -> APIResponse:
        return self.request.post(
            f"{self.api_base_url}/api/v1/projects",
            headers=self._headers(token, tenant_id),
            data=payload,
        )

    def get_project(self, token: str, tenant_id: str, project_id: int) -> APIResponse:
        return self.request.get(
            f"{self.api_base_url}/api/v1/projects/{project_id}",
            headers=self._headers(token, tenant_id),
        )

    def delete_project(self, token: str, tenant_id: str, project_id: int) -> APIResponse:
        return self.request.delete(
            f"{self.api_base_url}/api/v1/projects/{project_id}",
            headers=self._headers(token, tenant_id),
        )
