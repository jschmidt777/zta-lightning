"""Check for continuous logging and monitoring."""

from app.audit_reporter import AuditReporter
from app.domain_models import Device


class LoggingCheck:
    """Continuous logging and monitoring check."""

    def __init__(self, devices: list[Device]):
        """
        Initialize with a list of Device objects.

        :param devices: A list of Device objects to check.

        Example logging configuration format:
        "logging":{
            "enabled": True,
            "log_server": "192.168.1.100",
            "logging_levels": ["INFO", "WARNING", "ERROR", "FATAL"]
        }
        """

        self._devices = devices
        self._log_server = self._get_logging_server_ip()

    def _is_logging_enabled(self, device_config: dict) -> bool:
        """Check if logging is enabled on the device.

        :param device_config: the device configuration
        :return: boolean indicating if logging is enabled
        """
        return device_config.get("logging").get("enabled")

    def _has_centralized_logging_server(self, device_config: dict) -> bool:
        """Check if the device is pointing to the centralized logging server.

        :param device_config: the device configuration
        :return: boolean indicating if the device is sending logs to the centralized logging server
        """
        return device_config.get("logging").get("log_server") == self._log_server

    def _has_required_logging_levels(self, device_config: dict, device_type: str) -> bool:
        """Check if the device is logging the required levels based on its type.

        :param device_config: the device configuration
        :param device_type: the device type
        :return: boolean indicating if the device has the required logging level
        """
        required_levels = self._get_required_logging_levels(device_type)
        return all(level in device_config.get("logging").get("log_events") for level in required_levels)

    def _get_required_logging_levels(self, device_type: str) -> list[str]:
        """Get the required logging levels based on the device type.
        Routers, switches, firewalls, and servers need INFO, WARNING, ERROR, and FATAL.
        Hosts only need INFO and WARNING.

        :param device_type: a device type
        :return: list of levels of logging required
        """
        if device_type in ["router", "switch", "firewall", "server"]:
            return ["INFO", "WARNING", "ERROR", "FATAL"]
        elif device_type == "host":
            return ["INFO", "WARNING"]
        return []

    def _get_logging_server_ip(self) -> str:
        """Retrieve the centralized logging server ip address from devices.

        :return: the ip address of the central logging server
        """
        for device in self._devices:
            if "AAA" in device.configuration.get("services", []):
                return device.ip_address

    def run_logging_checks(self, audit_reporter: AuditReporter) -> None:
        """Run all Logging checks for each device and report on results.

        :param audit_reporter: the audit reporter.
        :return: None
        """

        for device in self._devices:
            device_config = device.configuration
            is_logging_enabled = self._is_logging_enabled(device_config)
            has_centralized_logging_server = self._has_centralized_logging_server(device_config)
            has_required_logging_levels = self._has_required_logging_levels(device_config, device.device_type)
            compliant = all((is_logging_enabled, has_centralized_logging_server, has_required_logging_levels))

            audit_reporter.add_result(
                device.hostname,
                "Logging",
                compliant,
                f"Device has logging enabled: {is_logging_enabled}. \n"
                f"Device has expected centralized logging server ({self._log_server}): {has_centralized_logging_server}. \n"
                f"Device has required logging level (hosts: INFO, WARNING | all others: INFO, WARNING, ERROR, FATAL): "
                f"{has_required_logging_levels}.",
            )
