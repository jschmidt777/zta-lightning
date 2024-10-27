"""Client for interacting with the configured network appliance."""

import getpass
import os
from typing import Any

import urllib3
from dotenv import load_dotenv

import requests

JSON = dict[str, Any] | None
JWT = str | None

load_dotenv()

VERIFY_SSL = os.getenv("VERIFY_SSL", "True").lower() in ["true", "1"]

if not VERIFY_SSL:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class APIClient:
    """Client to interact with the network appliance."""

    def __init__(self):
        """Initialize the client."""
        self._token: JWT = None
        self._base_url: str | None = None

    def authenticate(self) -> tuple[JWT, str] | None:
        """Authenticate with the appliance server and obtain an access token to run a ZTA compliance audit.

        :return: a JavaScript Web Token (str)
        """

        base_url = input("Enter the AAA/NMS appliance url:") or "https://localhost:443"
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")

        auth_url = f"{base_url}/auth"
        auth_data = {"username": username, "password": password}

        try:
            response = requests.post(auth_url, json=auth_data, verify=VERIFY_SSL)
            response.raise_for_status()
            token = response.json().get("token")
            print("Authentication successful!")
            self._token = token
            self._base_url = base_url
        except requests.exceptions.HTTPError as err:
            print(f"Authentication failed: {err}")
            print("Response:", response.json())
            return None

    def test_connection(self) -> JSON:
        """Test the connection by accessing the config of machine the user is authenticating on.

        :return: a JSON response of the config
        """
        if self._token:
            device = "AdminMachine"
            protected_url = f"{self._base_url}/device/{device}/config"
            headers = {"Authorization": f"Bearer {self._token}"}
            try:
                response = requests.get(protected_url, headers=headers, verify=VERIFY_SSL)
                response.raise_for_status()
                config = response.json().get("configuration")
                print(f"Successfully accessed {device} configuration.")
                return config
            except requests.exceptions.HTTPError as err:
                print(f"Failed to access test connection config: {device} Error was: {err}")
                try:
                    print("Response:", response.json())
                except ValueError:
                    print("No JSON response received.")
                return None
        else:
            print(
                "Authentication failed: Please ensure you have proper credentials to your "
                "network appliance and try again."
            )

    def get_all_device_data(self) -> JSON:
        """Get all device configurations for compliance checks.

        :return: JSON of all device configuration data
        """
        if self._token:
            protected_url = f"{self._base_url}/device/configs"
            headers = {"Authorization": f"Bearer {self._token}"}
            try:
                response = requests.get(protected_url, headers=headers, verify=VERIFY_SSL)
                response.raise_for_status()
                device_configs = response.json()
                print(f"Successfully accessed device configurations for compliance checking.")
                return device_configs
            except requests.exceptions.HTTPError as err:
                print(f"Failed to access device configs. Error was: {err}")
                try:
                    print("Response:", response.json())
                except ValueError:
                    print("No JSON response received.")
                return None

    def get_all_user_info(self) -> JSON:
        """Get all user info. for compliance checks.

        :return: JSON of all user info. data
        """
        if self._token:
            protected_url = f"{self._base_url}/users/data"
            headers = {"Authorization": f"Bearer {self._token}"}
            try:
                response = requests.get(protected_url, headers=headers, verify=VERIFY_SSL)
                response.raise_for_status()
                device_configs = response.json()
                print(f"Successfully accessed user info. for compliance checking.")
                return device_configs
            except requests.exceptions.HTTPError as err:
                print(f"Failed to access user info. Error was: {err}")
                try:
                    print("Response:", response.json())
                except ValueError:
                    print("No JSON response received.")
                return None
