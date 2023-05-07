"""
Functions that will be used throughout the test suite
"""

import subprocess

from dotenv import dotenv_values


def get_creds(url: str) -> dict[str, str] | None:
    """
    Uses the bitwarden CLI to get the required credentials for ths specified website
    :param url: The URL to get the credentials for
    :return: A dictionary containing the username, password, and optional totp, which is None if there is no totp
    """
    config = dotenv_values(".env")

    master_password = config["master_password"]

    unlock = subprocess.run(['bw', 'unlock', master_password], stdout=subprocess.PIPE, check=False)\
        .stdout.decode("utf-8")

    if "Your vault is now unlocked!" not in unlock:
        return None

    session = unlock.split("--session")[2]

    username = subprocess.run(['bw', 'get', 'username', url, '--session', session], stdout=subprocess.PIPE,
                              check=False).stdout.decode("utf-8")

    password = subprocess.run(['bw', 'get', 'password', url, '--session', session], stdout=subprocess.PIPE,
                              check=False).stdout.decode("utf-8")

    totp = subprocess.run(['bw', 'get', 'totp', url, '--session', session], stdout=subprocess.PIPE,
                          check=False).stdout.decode("utf-8")

    if "No TOTP available for this login." in totp:
        totp = None

    return {"username": username, "password": password, "totp": totp}
