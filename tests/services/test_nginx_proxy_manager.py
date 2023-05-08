"""
Test suite to make sure Proxy Manager is working
"""
from dotenv import dotenv_values
from playwright.sync_api import Page, expect
from tests import get_creds

config = dotenv_values(".env")
URL = config["PROXY_MANAGER_URL"]


def test_service_up(page: Page):
    """
    Test to make sure the proxy manager instance page is running
    :param page: The playwright webpage
    """
    response = page.goto(URL, wait_until="domcontentloaded")

    assert response.ok

    page.wait_for_load_state("networkidle")

    expect(page.get_by_text("Login")).to_have_text("Login to your account")


def test_service_login(page: Page):
    """
    Test to make sure we can log into the proxy manager instance using our credentials
    :param page: The playwright webpage
    """
    page.goto(URL, wait_until="domcontentloaded")

    page.wait_for_load_state("networkidle")

    username_textbox = page.get_by_role("textbox", name="Email address")

    password_textbox = page.get_by_role("textbox", name="Password")

    login_button = page.get_by_role("button", name="Sign in")

    creds = get_creds(URL)

    username_textbox.fill(creds["username"])

    password_textbox.fill(creds["password"])

    login_button.click()

    page.wait_for_load_state("networkidle")

    proxy_hosts = page.locator('xpath=//*[@id="dashboard"]/div[2]/div[1]/div/div')

    redirection_hosts = page.locator('xpath=//*[@id="dashboard"]/div[2]/div[2]/div/div')

    streams = page.locator('xpath=//*[@id="dashboard"]/div[2]/div[3]/div/div')

    error_404_hosts = page.locator('xpath=//*[@id="dashboard"]/div[2]/div[4]/div/div')

    expect(proxy_hosts).to_have_text("5 Proxy Hosts")

    expect(redirection_hosts).to_have_text("0 Redirection Hosts")

    expect(streams).to_have_text("0 Streams")

    expect(error_404_hosts).to_have_text("0 404 Hosts")
