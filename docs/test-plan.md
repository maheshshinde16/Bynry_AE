# Test Plan

## Objective

Verify that authorized users can safely access the B2B SaaS application and that a project created within one tenant remains unavailable to every other tenant.

## Risk-based coverage

| Area | Priority | Coverage |
| --- | --- | --- |
| Authentication and role access | Critical | Valid login, invalid login, session expiry, approved MFA strategy |
| Tenant isolation | Critical | API 403/404 behavior, UI absence, fresh-session checks |
| Project lifecycle | Critical | Create through API, UI rendering, project status, cleanup |
| Browser compatibility | High | Chrome, Firefox, Safari/WebKit |
| Responsive mobile web | High | iPhone Safari and Android Chrome viewports/devices |
| API resilience | High | Validation, authorization, rate-limit and transient error handling |
| Accessibility and performance | Medium | Keyboard navigation and key-page timing budgets |

## Entry and exit criteria

Entry criteria: a QA/staging environment is available, dedicated test accounts and tenant IDs are provisioned, secrets are injected through CI, and API behavior is documented.

Exit criteria: critical smoke tests pass; no unresolved critical authentication or tenant-isolation defects exist; and CI artifacts are retained for every failure.

## Test-data policy

- Use dedicated automation tenants and users only.
- Generate a unique project name per run to support parallel execution.
- Never put customer data, production passwords, or tokens in this repository.
- Delete projects created by the suite in `finally`; a scheduled cleanup job is a backup safeguard.

## CI matrix

Pull request: API suite plus Chromium smoke coverage.

Nightly: regression coverage on Chrome, Firefox, WebKit, and a selected BrowserStack desktop/mobile matrix.

Release candidate: complete tenant-isolation, role-permission, integration, and supported-device suite.
