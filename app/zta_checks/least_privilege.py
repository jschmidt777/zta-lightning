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
            for user in self._user_data:
                user_roles = user.roles
                if device.device_type == "host":
                    if user.username == device.configuration.get("allowed_user"):
                        compliant.append(True)
                    else:
                        compliant.append(False)
                else:
                    if user.username in device.configuration.get("auth", {}).get("acl", {}).get("allow", []):
                        compliant.append(True)
                    else:
                        compliant.append(False)

                allowed_roles = device.configuration.get("roles", [])
                if any(role in user_roles for role in allowed_roles):
                    compliant.append(True)
                else:
                    compliant.append(False)

            compliant = all(compliant)
            audit_reporter.add_result(
                device.hostname,
                "Least Privilege",
                compliant,
                f"Device has proper permissions for users: {compliant}."
            )
