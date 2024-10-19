"""Unit tests for AuthAndACCheck."""

import unittest
from copy import deepcopy
from app.domain_models import Device, User
from app.zta_checks.auth_and_ac import AuthAndACCheck


class TestAuthAndACCheck(unittest.TestCase):
    def setUp(self):
        """Set up the raw data for devices and users.

        Device and User are immutable so get_fresh_objects is used for new object creation."""

        self.host_data = {
            "hostname": "Host1",
            "ip_address": "192.168.1.101",
            "device_type": "host",
            "configuration": {
                "auth": {
                    "enabled": True,
                    "aaa_server": "192.168.1.100",
                    "assigned_user": "user1",
                }
            },
        }

        self.server_data = {
            "hostname": "Server1",
            "ip_address": "192.168.1.102",
            "device_type": "server",
            "configuration": {
                "auth": {
                    "enabled": True,
                    "aaa_server": "192.168.1.100",
                    "acl": {"Allow": ["user2"]},
                }
            },
        }

        self.network_device_data = {
            "hostname": "Router1",
            "ip_address": "192.168.1.103",
            "device_type": "router",
            "configuration": {
                "auth": {
                    "enabled": True,
                    "aaa_server": "192.168.1.100",
                }
            },
        }

        self.aaa_server_data = {
            "hostname": "AAA",
            "ip_address": "192.168.1.100",
            "device_type": "server",
            "configuration": {"services": ["AAA"]},
        }

        self.user1_data = {"username": "user1", "roles": ["user"], "devices": ["Host1"]}
        self.user2_data = {"username": "user2", "roles": ["admin"], "devices": ["Server1"]}
        self.user3_data = {"username": "user3", "roles": ["user"], "devices": ["Router1"]}

    def get_fresh_objects(self):
        """Create fresh Device and User objects."""
        devices = [
            Device(deepcopy(self.host_data)),
            Device(deepcopy(self.server_data)),
            Device(deepcopy(self.network_device_data)),
            Device(deepcopy(self.aaa_server_data)),
        ]
        users = [
            User(deepcopy(self.user1_data)),
            User(deepcopy(self.user2_data)),
            User(deepcopy(self.user3_data)),
        ]
        return devices, users

    def test_auth_enabled(self):
        """Test that authentication is enabled on devices."""
        devices, users = self.get_fresh_objects()
        checker = AuthAndACCheck(devices, users)
        self.assertTrue(checker._is_auth_enabled(devices[0].configuration))
        self.assertTrue(checker._is_auth_enabled(devices[1].configuration))

    def test_has_centralized_aaa_server(self):
        """Test that devices point to the centralized AAA server."""
        devices, users = self.get_fresh_objects()
        checker = AuthAndACCheck(devices, users)
        self.assertTrue(checker._has_centralized_aaa_server(devices[1].configuration))
        self.assertTrue(checker._has_centralized_aaa_server(devices[2].configuration))

    def test_host_access_controls(self):
        """Test that only one non-admin user is assigned to a host."""
        devices, users = self.get_fresh_objects()
        checker = AuthAndACCheck(devices, users)
        self.assertTrue(checker._has_access_controls(devices[0], users))

        non_compliant_user_data = {"username": "user1", "roles": ["user"], "devices": ["Host1", "Host2"]}
        non_compliant_user = User(non_compliant_user_data)

        checker = AuthAndACCheck(devices, [non_compliant_user])
        self.assertFalse(checker._has_access_controls(devices[0], [non_compliant_user]))

    def test_server_acl(self):
        """Test that server access complies with the ACL."""
        devices, users = self.get_fresh_objects()
        checker = AuthAndACCheck(devices, users)
        self.assertTrue(checker._has_access_controls(devices[1], users))

        modified_server_data = deepcopy(self.server_data)
        modified_server_data["configuration"]["auth"]["acl"] = {"Allow": []}
        modified_server = Device(modified_server_data)

        self.assertFalse(checker._has_access_controls(modified_server, users))

    def test_network_device_access_controls(self):
        """Test that only admin users can access network devices."""
        devices, users = self.get_fresh_objects()
        checker = AuthAndACCheck(devices, users)
        self.assertFalse(checker._has_access_controls(devices[2], users))

        compliant_user_data = {"username": "user3", "roles": ["admin"], "devices": ["Router1"]}
        compliant_user = User(compliant_user_data)

        checker = AuthAndACCheck(devices, [compliant_user])
        self.assertTrue(checker._has_access_controls(devices[2], [compliant_user]))


if __name__ == "__main__":
    unittest.main()
