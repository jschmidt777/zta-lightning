"""Unit tests for Least Privilege."""

import unittest
from unittest.mock import Mock
from app.domain_models import Device, User
from app.audit_reporter import AuditReporter
from app.zta_checks.least_privilege import LeastPrivilegeCheck


class TestLeastPrivilegeCheck(unittest.TestCase):

    def setUp(self):
        """Set up mock device configurations for the tests."""

        self.router_data = {
            "hostname": "Router1",
            "ip_address": "192.168.1.101",
            "device_type": "router",
            "configuration": {
                "roles": ["admin"],
                "auth": {"acl": {"allow": ["user1"]}}
            }
        }

        self.server_data = {
            "hostname": "Server1",
            "ip_address": "192.168.1.102",
            "device_type": "server",
            "configuration": {
                "roles": ["user"],
                "auth": {"acl": {"allow": ["user2"]}}
            }
        }

        self.user1_data = {"username": "user1", "roles": ["admin"], "devices": ["Router1"]}
        self.user2_data = {"username": "user2", "roles": ["user"], "devices": ["Server1"]}

        self.router = Device(self.router_data)
        self.server = Device(self.server_data)

    def test_least_privilege_compliance_router_user(self):
        """Test compliance of user permission to router based on roles."""
        checker = LeastPrivilegeCheck([self.router], [User(self.user1_data)])
        mock_reporter = Mock(AuditReporter)
        checker.run_least_privilege_check(mock_reporter)
        mock_reporter.add_result.assert_called_with(
            "Router1",
            "Least Privilege",
            True,
            "Device has proper permissions for users: True."
        )

    def test_least_privilege_compliance_server_user(self):
        """Test compliance of user permission to server based on roles."""
        checker = LeastPrivilegeCheck([self.server], [User(self.user2_data)])
        mock_reporter = Mock(AuditReporter)
        checker.run_least_privilege_check(mock_reporter)
        mock_reporter.add_result.assert_called_with(
            "Server1",
            "Least Privilege",
            True,
            "Device has proper permissions for users: True."
        )

    def test_least_privilege_non_compliance(self):
        """Test non-compliant user permission."""
        non_compliant_user = User({"username": "user3", "roles": ["user"], "devices": ["Router1"]})
        checker = LeastPrivilegeCheck([self.router], [non_compliant_user])
        mock_reporter = Mock(AuditReporter)
        checker.run_least_privilege_check(mock_reporter)
        mock_reporter.add_result.assert_called_with(
            "Router1",
            "Least Privilege",
            False,
            "Device has proper permissions for users: False."
        )


if __name__ == "__main__":
    unittest.main()
