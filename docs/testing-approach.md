# Testing Approach and Assumptions

## Reliable automation

The original flaky login style is corrected by using a fresh browser context per test, stable accessibility/test-ID locators, and explicit assertions that wait for a business-ready UI state. The suite avoids arbitrary sleep calls. CI is often slower than a local laptop because of shared runners, network latency, lower resources, rendering timing, viewport changes, and external identity-provider behavior.

## Multi-tenant security

Seeing the text "Company2" is not sufficient proof of tenant isolation. This approach verifies the active tenant in the UI, checks the tenant ID attached to the created project, and makes an API request using Company2's credentials that must return `403` or `404` for Company1's project. Fresh browser contexts avoid cookie and local-storage leakage.

## Authentication and 2FA

Production security must not be weakened for automation. Test accounts should use an approved non-production MFA mechanism, such as a controlled identity-provider account or test OTP service. Passwords, tokens, BrowserStack keys, and personal data belong in a secret manager and CI secrets.

## BrowserStack strategy

Use a small, risk-based device matrix nightly to manage execution time and cost. Retain a trace, screenshot, video, console logs, and failed API response only for failures. Playwright covers web and responsive mobile-web testing. If the product has a native Android/iOS app, use Appium with BrowserStack App Automate for app-specific checks.

## Requirements to clarify

1. Is mobile native, responsive web, or both?
2. Which browser, device, operating-system, and version combinations are supported?
3. How are tenants separated—subdomain, database, or tenant header?
4. What test environment, reset strategy, roles, and MFA automation approach are available?
5. Are project creation and search eventually consistent or asynchronous?
6. What reporting, parallelism, test-duration, and release-gate expectations apply?
