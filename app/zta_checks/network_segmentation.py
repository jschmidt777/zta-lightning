"""Check for network segmentation."""

from ipaddress import IPv4Network

from app.audit_reporter import AuditReporter
from app.domain_models import Device

import ipaddress

VLAN = str
IpSubNet = IPv4Network
Segment = VLAN | IpSubNet


class NetworkSegmentationCheck:
    """Network segmentation check."""

    def __init__(self, devices: list[Device]):
        """
        Initialize with a list of Device objects.

        :param devices: A list of Device objects to check.

        Example segment configuration format:
            Network Device:
            "network_segmentation": {
                "allowed_segments": ["192.168.1.0/24", "10.0.0.0/24"]
            }
            Host or Server:
            "allowed_segments": ["30"]
        """
        self._devices = devices

    def _is_segment_allowed(self, segment: Segment, allowed_segments: list[Segment]) -> bool:
        """Check if a segment (either VLAN ID/Name or IP subnet) is in the allowed segments.

        :param segment: the segment
        :param allowed_segments: the allowed segments
        :return: boolean indicating if the segment is allowed
        """
        try:
            segment_net = ipaddress.ip_network(segment)
            for allowed in allowed_segments:
                try:
                    if segment_net.subnet_of(ipaddress.ip_network(allowed)):
                        return True
                except ValueError:
                    continue
        except ValueError:
            # when not an IP, treat it as a VLAN ID or Name
            return segment in allowed_segments
        return False

    def _check_network_device_segments(self, device_config: dict, device_type: str) -> list[bool]:
        """Check the network device segments for compliance.

        :param device_config: the device configuration
        :param device_type: the device type
        :return: boolean list of what segments are compliant
        """
        compliant_segments = []
        allowed_segments = device_config.get("network_segmentation", {}).get("allowed_segments", [])
        if device_type == "switch":
            vlans = device_config.get("VLANs", [])
            for vlan_id in vlans:
                compliant_segments.append(self._is_segment_allowed(vlan_id, allowed_segments))
        else:
            for segment in allowed_segments:
                compliant_segments.append(self._is_segment_allowed(segment, allowed_segments))
        return compliant_segments

    def _check_host_or_server_segments(self, device_config: dict) -> list[bool]:
        """Check the host or server segments for compliance.

        :param device_config: the device configuration
        :return: boolean list of what segments are compliant
        """
        compliant_segments = []
        allowed_segments = device_config.get("allowed_segments", [])
        connected_network_device_name: str = device_config.get("connected_to").get("device")
        connected_network_device: Device = next(d for d in self._devices if d.hostname == connected_network_device_name)
        compare_segments = connected_network_device.configuration.get("network_segmentation", {}).get(
            "allowed_segments", []
        )
        for segment in allowed_segments:
            segment_valid = segment in compare_segments
            compliant_segments.append(segment_valid)
        return compliant_segments

    def run_network_segmentation_checks(self, audit_reporter: AuditReporter) -> None:
        """Run all Network Segmentation checks for each device and report on results.

        :param audit_reporter: the audit reporter
        :return: None
        """
        for device in self._devices:
            device_config = device.configuration
            device_type = device.device_type
            compliant = []
            network_devices = ["router", "switch", "firewall"]
            if device_type in network_devices:
                result = self._check_network_device_segments(device_config, device_type)
                compliant.extend(result)
            elif device_type == "host" or device_type == "server":
                result = self._check_host_or_server_segments(device_config)
                compliant.extend(result)

            compliant = all(compliant)
            audit_reporter.add_result(
                device.hostname,
                "Network Segmentation",
                compliant,
                f"Device has proper network segmentation "
                f"(network device | proper VLANs/Subnets, "
                f"host and servers | proper VLAN and connected device): {compliant}.",
            )
