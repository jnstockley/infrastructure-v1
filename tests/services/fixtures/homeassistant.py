"""
Contains fixtures for testing multiple home assistance instances
"""
import pytest
from playwright.sync_api import Page, expect
from tests import get_creds


@pytest.fixture
def ha_service_up(page: Page, request):
    """
    Based on the URL, makes sure the page is up
    :param page: The Playwright webpage
    :param request: Contains params which contains the URL
    :return: The Playwright webpage
    """
    url = request.param

    response = page.goto(url, wait_until="domcontentloaded")

    assert response.ok

    page.wait_for_load_state("networkidle")

    title = page.get_by_text("Home Assistant", exact=True)

    expect(title).to_have_text("Home Assistant")

    description = page.get_by_text("You're")

    expect(description).to_contain_text(url)

    return page


@pytest.fixture
def ha_login(page: Page, request):
    """
    Based on the URL, gets the specified credentials, and navigates to login page
    :param page: The Playwright webpage
    :param request: Contains params which contains the URL
    :return: The credentials to log into the specified instance
    """
    url = request.param

    creds = get_creds(url)

    page.goto(url, wait_until="domcontentloaded")

    page.wait_for_load_state("networkidle")

    return creds
