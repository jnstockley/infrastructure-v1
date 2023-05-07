"""
Test suite to make sure all home assistant instances are working
"""
import pytest
from playwright.sync_api import Page, expect
from dotenv import dotenv_values


config = dotenv_values(".ha_env")
URLS = config["URLS"].split(", ")


@pytest.mark.parametrize("ha_service_up", URLS, indirect=True)
def test_service_up(page: Page, ha_service_up):
    """
    Test to make sure the home assistant instance page is running
    :param page: The Playwright webpage
    :param ha_service_up: Fixture to test multiple URLs while re-using code
    """
    username = ha_service_up.get_by_role("textbox", name="Username")

    password = page.get_by_role("textbox", name="Password")

    login_button = page.get_by_role("button", name="LOGIN")

    expect(username).to_be_visible()

    expect(password).to_be_visible()

    expect(login_button).to_be_visible()


@pytest.mark.parametrize("ha_login", URLS, indirect=True)
def test_service_login(page: Page, ha_login):
    """
    Test to make sure we can log into the home assistance instance using our credentials
    :param page: The Playwright webpage
    :param ha_login: Creds returned from the ha_login fixture for the specified instance
    """
    username_textbox = page.get_by_role("textbox", name="Username")

    password_textbox = page.get_by_role("textbox", name="Password")

    login_button = page.get_by_role("button", name="LOGIN")

    username_textbox.fill(ha_login["username"])

    password_textbox.fill(ha_login["password"])

    login_button.click()

    authentication_desc = page.get_by_text("Authenticator app")

    expect(authentication_desc).to_be_visible()

    totp_textbox = page.get_by_role("textbox", name="Two-factor Authentication Code")

    totp_textbox.fill(ha_login["totp"])

    login_button = page.get_by_role("button", name="LOGIN")

    login_button.click()

    page.wait_for_load_state("networkidle")

    user_full_name = page.get_by_text("Jack Stockley")

    expect(user_full_name).to_have_text("Jack Stockley")
