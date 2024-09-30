"""Unit tests for LoggingCheck."""

import unittest
from app.zta_checks.logging import LoggingCheck
from app.domain_model import Device


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
        checker = LoggingCheck(self.devices)
        self.assertTrue(checker.is_logging_enabled(self.router.configuration))

        modified_router_data = {
            **self.router_data,
            "configuration": {
                **self.router_data["configuration"],
                "logging": {
                    **self.router_data["configuration"]["logging"],
                    "enabled": False,
                }
            }
        }
        modified_router = Device(modified_router_data)
        self.assertFalse(checker.is_logging_enabled(modified_router.configuration))

    def test_is_logging_enabled_host(self):
        checker = LoggingCheck(self.devices)
        self.assertTrue(checker.is_logging_enabled(self.host.configuration))

        modified_host_data = {
            **self.host_data,
            "configuration": {
                **self.host_data["configuration"],
                "logging": {
                    **self.host_data["configuration"]["logging"],
                    "enabled": False,
                }
            }
        }
        modified_host = Device(modified_host_data)
        self.assertFalse(checker.is_logging_enabled(modified_host.configuration))

    def test_has_centralized_logging_server_router(self):
        checker = LoggingCheck(self.devices)
        self.assertTrue(checker.has_centralized_logging_server(self.router.configuration))

        modified_router_data = {
            **self.router_data,
            "configuration": {
                **self.router_data["configuration"],
                "logging": {
                    **self.router_data["configuration"]["logging"],
                    "log_server": "",
                }
            }
        }
        modified_router = Device(modified_router_data)
        self.assertFalse(checker.has_centralized_logging_server(modified_router.configuration))

    def test_has_centralized_logging_server_host(self):
        checker = LoggingCheck(self.devices)
        self.assertTrue(checker.has_centralized_logging_server(self.host.configuration))

        modified_host_data = {
            **self.host_data,
            "configuration": {
                **self.host_data["configuration"],
                "logging": {
                    **self.host_data["configuration"]["logging"],
                    "log_server": "",
                }
            }
        }
        modified_host = Device(modified_host_data)
        self.assertFalse(checker.has_centralized_logging_server(modified_host.configuration))

    def test_has_required_logging_levels_router(self):
        checker = LoggingCheck(self.devices)
        self.assertTrue(checker.has_required_logging_levels(self.router.configuration, "router"))

        modified_router_data = {
            **self.router_data,
            "configuration": {
                **self.router_data["configuration"],
                "logging": {
                    **self.router_data["configuration"]["logging"],
                    "log_events": ["INFO", "WARNING"],
                }
            }
        }
        modified_router = Device(modified_router_data)
        self.assertFalse(checker.has_required_logging_levels(modified_router.configuration, "router"))

    def test_has_required_logging_levels_host(self):
        checker = LoggingCheck(self.devices)
        self.assertTrue(checker.has_required_logging_levels(self.host.configuration, "host"))

        modified_host_data = {
            **self.host_data,
            "configuration": {
                **self.host_data["configuration"],
                "logging": {
                    **self.host_data["configuration"]["logging"],
                    "log_events": ["INFO"],
                }
            }
        }
        modified_host = Device(modified_host_data)
        self.assertFalse(checker.has_required_logging_levels(modified_host.configuration, "host"))

    def test_run_logging_checks(self):
        checker = LoggingCheck(self.devices)
        results = checker.run_logging_checks()

        router1 = results[0]
        self.assertTrue(router1.compliant)
        self.assertTrue(router1.logging_enabled)
        self.assertTrue(router1.centralized_logging_server)
        self.assertTrue(router1.required_logging_level)

        host1 = results[1]
        self.assertTrue(host1.compliant)
        self.assertTrue(host1.logging_enabled)
        self.assertTrue(host1.centralized_logging_server)
        self.assertTrue(host1.required_logging_level)

        modified_host_data = {
            **self.host_data,
            "configuration": {
                **self.host_data["configuration"],
                "logging": {
                    **self.host_data["configuration"]["logging"],
                    "log_server": "",
                }
            }
        }
        modified_router_data = {
            **self.router_data,
            "configuration": {
                **self.router_data["configuration"],
                "logging": {
                    **self.router_data["configuration"]["logging"],
                    "log_events": ["INFO", "WARNING"],
                }
            }
        }

        modified_host = Device(modified_host_data)
        modified_router = Device(modified_router_data)

        checker = LoggingCheck([modified_router, modified_host, self.log_server])
        results = checker.run_logging_checks()

        router1 = results[0]
        host1 = results[1]
        self.assertFalse(host1.centralized_logging_server)
        self.assertFalse(router1.required_logging_level)


if __name__ == "__main__":
    unittest.main()
