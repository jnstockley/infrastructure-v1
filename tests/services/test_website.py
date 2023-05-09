"""
Test suite to make sure my website is working
"""
from dotenv import dotenv_values
from playwright.sync_api import Page, expect

config = dotenv_values(".env")
URL = config["WEBSITE_URL"]


def test_service_up(page: Page):
    """
    Test to make sure my website is running
    :param page: The playwright webpage
    """
    response = page.goto(URL, wait_until="domcontentloaded")

    page.wait_for_load_state("networkidle")

    assert response.ok

    menu = page.get_by_role("navigation")

    expect(menu).to_contain_text("Home")

    expect(menu).to_contain_text("Courses")

    expect(menu).to_contain_text("Education")

    expect(menu).to_contain_text("Experience")

    expect(menu).to_contain_text("Projects")
