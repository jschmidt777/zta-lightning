"""Unit tests for LoggingCheck."""

import unittest

from app.zta_checks.logging import LoggingCheck
from app.domain_models import Device


class TestLoggingCheck(unittest.TestCase):

    def setUp(self):
        """Set up mock device configurations for the tests.

        Device is immutable so changes are made to the configurations in the tests
        to make new Device objects for testing.
        """
        self.router_data = {
            "hostname": "Router1",
            "ip_address": "192.168.1.101",
            "device_type": "router",
            "configuration": {
                "logging": {
                    "enabled": True,
                    "log_server": "192.168.1.100",
                    "log_events": ["INFO", "WARNING", "ERROR", "FATAL"],
                }
            },
        }

        self.host_data = {
            "hostname": "Host2",
            "ip_address": "192.168.1.102",
            "device_type": "host",
            "configuration": {
                "logging": {
                    "enabled": True,
                    "log_server": "192.168.1.100",
                    "log_events": ["INFO", "WARNING"],
                }
            },
        }

        self.log_server_data = {
            "hostname": "ApplianceServer",
            "ip_address": "192.168.1.100",
            "device_type": "server",
            "configuration": {
                "services": ["AAA"],
                "logging": {
                    "enabled": True,
                    "log_server": "192.168.1.100",
                    "log_events": ["INFO", "WARNING", "ERROR", "FATAL"],
                },
            },
        }

        self.router = Device(self.router_data)
        self.host = Device(self.host_data)
        self.log_server = Device(self.log_server_data)
        self.devices = [self.router, self.host, self.log_server]

    def test_is_logging_enabled_router(self):
        """Test that the router has logging enabled."""
        checker = LoggingCheck(self.devices)
        self.assertTrue(checker._is_logging_enabled(self.router.configuration))

        modified_router_data = {
            **self.router_data,
            "configuration": {
                **self.router_data["configuration"],
                "logging": {
                    **self.router_data["configuration"]["logging"],
                    "enabled": False,
                },
            },
        }
        modified_router = Device(modified_router_data)
        self.assertFalse(checker._is_logging_enabled(modified_router.configuration))

    def test_is_logging_enabled_host(self):
        """Test that the host has logging enabled."""
        checker = LoggingCheck(self.devices)
        self.assertTrue(checker._is_logging_enabled(self.host.configuration))

        modified_host_data = {
            **self.host_data,
            "configuration": {
                **self.host_data["configuration"],
                "logging": {
                    **self.host_data["configuration"]["logging"],
                    "enabled": False,
                },
            },
        }
        modified_host = Device(modified_host_data)
        self.assertFalse(checker._is_logging_enabled(modified_host.configuration))

    def test_has_centralized_logging_server_router(self):
        """Test that the router has a centralized logging server."""
        checker = LoggingCheck(self.devices)
        self.assertTrue(checker._has_centralized_logging_server(self.router.configuration))

        modified_router_data = {
            **self.router_data,
            "configuration": {
                **self.router_data["configuration"],
                "logging": {
                    **self.router_data["configuration"]["logging"],
                    "log_server": "",
                },
            },
        }
        modified_router = Device(modified_router_data)
        self.assertFalse(checker._has_centralized_logging_server(modified_router.configuration))

    def test_has_centralized_logging_server_host(self):
        """Test that the host has a centralized logging server."""
        checker = LoggingCheck(self.devices)
        self.assertTrue(checker._has_centralized_logging_server(self.host.configuration))

        modified_host_data = {
            **self.host_data,
            "configuration": {
                **self.host_data["configuration"],
                "logging": {
                    **self.host_data["configuration"]["logging"],
                    "log_server": "",
                },
            },
        }
        modified_host = Device(modified_host_data)
        self.assertFalse(checker._has_centralized_logging_server(modified_host.configuration))

    def test_has_required_logging_levels_router(self):
        """Test that the router has the required logging level."""
        checker = LoggingCheck(self.devices)
        self.assertTrue(checker._has_required_logging_levels(self.router.configuration, "router"))

        modified_router_data = {
            **self.router_data,
            "configuration": {
                **self.router_data["configuration"],
                "logging": {
                    **self.router_data["configuration"]["logging"],
                    "log_events": ["INFO", "WARNING"],
                },
            },
        }
        modified_router = Device(modified_router_data)
        self.assertFalse(checker._has_required_logging_levels(modified_router.configuration, "router"))

    def test_has_required_logging_levels_host(self):
        """Test that the host has the required logging level."""
        checker = LoggingCheck(self.devices)
        self.assertTrue(checker._has_required_logging_levels(self.host.configuration, "host"))

        modified_host_data = {
            **self.host_data,
            "configuration": {
                **self.host_data["configuration"],
                "logging": {
                    **self.host_data["configuration"]["logging"],
                    "log_events": ["INFO"],
                },
            },
        }
        modified_host = Device(modified_host_data)
        self.assertFalse(checker._has_required_logging_levels(modified_host.configuration, "host"))


if __name__ == "__main__":
    unittest.main()
