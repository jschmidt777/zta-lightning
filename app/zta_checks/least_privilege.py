"""Check for least privilege."""

from app.audit_reporter import AuditReporter
from app.domain_models import Device, User


class LeastPrivilegeCheck:
    """Least privilege check."""

    def __init__(self, devices: list[Device], user_data: list[User]):
        """
        Initialize with a list of Device objects and User data.

        :param devices: A list of Device objects to check.
        :param user_data: A list of User objects representing users in the network.
        """
        self._devices = devices
        self._user_data = user_data

    def run_least_privilege_check(self, audit_reporter: AuditReporter) -> None:
        """Run Least Privilege check for each device and report on results.

        :param audit_reporter: the audit reporter
        :return: None
        """

        for device in self._devices:
            compliant = []
            if device.device_type == "host":
                assigned_user = device.configuration.get("auth", {}).get("assigned_user", "")
                allowed_roles = device.configuration.get("roles", [])
                valid_user = next(u for u in self._user_data if u.username == assigned_user)
                if assigned_user == valid_user.username and any(role in valid_user.roles for role in allowed_roles):
                    compliant.append(True)
                else:
                    compliant.append(False)
            else:
                acl = device.configuration.get("auth", {}).get("acl", {}).get("allow", [])
                valid_users = [user.username for user in self._user_data]
                for user in acl:
                    if user in valid_users:
                        compliant.append(True)
                    else:
                        compliant.append(False)

            compliant = all(compliant)
            audit_reporter.add_result(
                device.hostname, "Least Privilege", compliant, f"Device has proper permissions for users: {compliant}."
            )
