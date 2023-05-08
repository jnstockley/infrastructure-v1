from playwright.sync_api import Page, expect


def test_service_up(page: Page):
    response = page.goto("http://172.245.131.22:81", wait_until="domcontentloaded")

    assert response.ok

    page.wait_for_load_state("networkidle")

    expect(page.get_by_text("Login")).to_have_text("Login to your account")
