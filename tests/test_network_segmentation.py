"""Unit tests for Network Segmentation."""

import unittest
from unittest.mock import Mock
from app.domain_models import Device
from app.audit_reporter import AuditReporter
from app.zta_checks.network_segmentation import NetworkSegmentationCheck


class TestNetworkSegmentationChecker(unittest.TestCase):

    def setUp(self):
        """Set up mock device configurations for the tests."""

        self.router_data = {
            "hostname": "Router1",
            "ip_address": "192.168.1.101",
            "device_type": "router",
            "configuration": {
                "network_segmentation": {"allowed_segments": ["192.168.1.0/24"]},
            },
        }

        self.host_data = {
            "hostname": "Host1",
            "ip_address": "192.168.1.102",
            "device_type": "host",
            "configuration": {"connected_to": {"device": "Router1"}, "allowed_segments": ["192.168.1.0/24"]},
        }

        self.non_compliant_host_data = {
            "hostname": "Host2",
            "ip_address": "192.168.1.103",
            "device_type": "host",
            "configuration": {"connected_to": {"device": "Router1"}, "allowed_segments": ["10.0.0.0/24"]},
        }

        self.router = Device(self.router_data)
        self.host = Device(self.host_data)
        self.non_compliant_host = Device(self.non_compliant_host_data)

    def test_is_segment_allowed_with_valid_ip_subnet(self):
        checker = NetworkSegmentationCheck([self.router])
        result = checker._is_segment_allowed("192.168.1.0/24", ["192.168.1.0/24", "10.0.0.0/24"])
        self.assertTrue(result)

    def test_is_segment_allowed_with_vlan_id(self):
        checker = NetworkSegmentationCheck([self.router])
        result = checker._is_segment_allowed("10", ["10", "20"])
        self.assertTrue(result)

    def test_is_segment_allowed_with_invalid_vlan_id(self):
        checker = NetworkSegmentationCheck([self.router])
        result = checker._is_segment_allowed("30", ["10", "20"])
        self.assertFalse(result)

    def test_run_network_segmentation_checks_compliant_host(self):
        checker = NetworkSegmentationCheck([self.router, self.host])
        mock_reporter = Mock(AuditReporter)
        checker.run_network_segmentation_checks(mock_reporter)
        mock_reporter.add_result.assert_called_with(
            "Host1",
            "Network Segmentation",
            True,
            "Device has proper network segmentation (network device | proper VLANs/Subnets, host and servers | proper VLAN and connected device): True.",
        )

    def test_run_network_segmentation_checks_non_compliant_host(self):
        checker = NetworkSegmentationCheck([self.router, self.non_compliant_host])
        mock_reporter = Mock(AuditReporter)
        checker.run_network_segmentation_checks(mock_reporter)
        mock_reporter.add_result.assert_called_with(
            "Host2",
            "Network Segmentation",
            False,
            "Device has proper network segmentation (network device | proper VLANs/Subnets, host and servers | proper VLAN and connected device): False.",
        )


if __name__ == "__main__":
    unittest.main()
