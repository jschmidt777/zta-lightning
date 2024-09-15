"""ZTA Lightning
Author: Joe Schmidt"""

import getpass
from typing import Optional, Any

import requests

from cli import display_banner


def authenticate(base_url) -> Optional[str]:
    """Authenticate with the appliance server and obtain an access token to run a ZTA compliance audit.

    :param base_url: the url of the network appliance server
    :return: a JavaScript Web Token (str)
    """
    # todo: add more initial configuration instructions
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    auth_url = f"{base_url}/auth"
    auth_data = {"username": username, "password": password}

    try:
        response = requests.post(auth_url, json=auth_data)
        response.raise_for_status()
        token = response.json().get("token")
        print("Authentication successful!")
        return token
    except requests.exceptions.HTTPError as err:
        print(f"Authentication failed: {err}")
        print("Response:", response.json())
        return None


def test_connection(base_url, token) -> Optional[dict[str, Any]]:
    """Test the connection by accessing the config of machine the user is authenticating on.

    :param base_url: the url of the network appliance server
    :param token: a JavaScript Web Token (str)
    :return: a JSON response of the config
    """
    # todo: use this kind of pattern as the basis for the api client
    device = "AdminMachine"
    protected_url = f"{base_url}/device/{device}/config"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(protected_url, headers=headers)
        response.raise_for_status()
        config = response.json().get("configuration")
        print(f"Successfully accessed {device} configuration: {config}")
        return config
    except requests.exceptions.HTTPError as err:
        print(f"Failed to access test connection config: {device} Error was: {err}")
        try:
            print("Response:", response.json())
        except ValueError:
            print("No JSON response received.")
        return None


def main():
    """Run the zta-lightning application.

    :return: None
    """
    # todo: add this as part of the initial configuration of the tool (setting a url)
    # todo: configure https (create self signed cert on appliance, etc.)
    base_url = "http://localhost:5000"
    display_banner()
    token = authenticate(base_url)
    if token:
        test_connection(base_url, token)
        # todo: add in cli usage
    else:
        print(
            "Authentication failed: Please ensure you have proper credentials to your "
            "network appliance server and try again."
        )


if __name__ == "__main__":
    main()
