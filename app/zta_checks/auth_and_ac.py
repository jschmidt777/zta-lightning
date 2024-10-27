"""Check for authentication and access controls."""

from app.audit_reporter import AuditReporter
from app.domain_models import Device, User


class AuthAndACCheck:
    """Authentication and Access control check."""

    def __init__(self, devices: list[Device], user_data: list[User]):
        """
        Initialize with a list of Device objects and User data.

        :param devices: A list of Device objects to check.
        :param user_data: A list of User objects representing users in the network.

         Example auth configuration format:
            "auth":{
                "enabled": True,
                "aaa_server": "192.168.1.100",
                "acl"(OPTIONAL): {Allow: [Host3], Deny: [Host4]},
                "assigned_user"(OPTIONAL): "user1"
            }
        """
        self._devices = devices
        self._user_data = user_data
        self._aaa_server = self._get_aaa_server_ip()

    def _is_auth_enabled(self, device_config: dict) -> bool:
        """Check if authentication is enabled on the device.

        :param device_config: the device configuration
        :return: boolean indicating if auth is enabled
        """
        return device_config.get("auth", {}).get("enabled", False)

    def _has_centralized_aaa_server(self, device_config: dict) -> bool:
        """Check if the device points to the centralized AAA server.

        :param device_config: the device configuration
        :return: boolean indicating if the device has the correct centralized AAA server
        """
        return device_config.get("auth", {}).get("aaa_server") == self._aaa_server

    def _has_access_controls(self, device: Device, users: list[User]) -> bool:
        """Check if the device has appropriate access controls.

        :param device: the device
        :param users: the users
        :return: boolean indicating if the devices has appropriate access controls
        """
        device_type = device.device_type
        device_config = device.configuration

        if device_type == "host":
            # only one non-admin user is assigned to this host
            assigned_user = device_config.get("auth", {}).get("assigned_user", "")
            matching_user = next((user for user in users if user.username == assigned_user), None)

            # assigned user matches the device
            if not matching_user or len(matching_user.devices) > 1:
                return False

        elif device_type == "server":
            # server access must be governed by an ACL
            acl = device_config.get("auth", {}).get("acl", {})
            if not acl:
                return False

            # each user accessing the server complies with the ACL
            for user in users:
                if device.hostname in user.devices:
                    acl_status = acl.get("Allow", []) and user.username in acl["Allow"]
                    if not acl_status:
                        return False

        else:
            # only admin users should have access
            for user in users:
                if device.hostname in user.devices and "admin" not in user.roles:
                    return False

        return True

    def _get_aaa_server_ip(self) -> str:
        """Retrieve the IP address of the centralized AAA server."""
        for device in self._devices:
            if "AAA" in device.configuration.get("services", []):
                return device.ip_address
        return ""

    def run_auth_and_ac_checks(self, audit_reporter: AuditReporter) -> None:
        """Run all Authentication and Access control checks for each device and report on results.

        :param audit_reporter: the audit reporter
        :return: None
        """

        for device in self._devices:
            device_config = device.configuration
            is_auth_enabled = self._is_auth_enabled(device_config)
            has_centralized_aaa_server = self._has_centralized_aaa_server(device_config)
            has_access_controls = self._has_access_controls(device, self._user_data)
            compliant = all((is_auth_enabled, has_centralized_aaa_server, has_access_controls))

            audit_reporter.add_result(
                device.hostname,
                "Auth and AC",
                compliant,
                f"Device has auth enabled: {is_auth_enabled}. \n"
                f"Device has expected centralized AAA server ({self._aaa_server}): {has_centralized_aaa_server}. \n"
                f"Device has required access controls (One user per host | server w/ ACL | network devices admin only): "
                f"{has_access_controls}",
            )
