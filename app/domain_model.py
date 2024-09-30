"""Domain model for device."""

import ipaddress
from typing import Any

from app.exceptions import (
    InvalidDeviceTypeError,
    InvalidHostnameError,
    InvalidIpAddressError,
    InvalidConfigurationError,
)

JSON = dict[str, Any] | None

DEVICE_TYPES = ["host", "server", "switch", "router", "firewall"]


class Device:
    """A device on the network."""

    def __init__(self, device: JSON):
        hostname = device.get("hostname")
        ip_address = device.get("ip_address")
        device_type = device.get("device_type")
        configuration = device.get("configuration")

        if device_type not in DEVICE_TYPES:
            raise InvalidDeviceTypeError(device_type)
        self._device_type = device_type

        if len(hostname) > 100:
            raise InvalidHostnameError(hostname)
        self._hostname = hostname

        try:
            ipaddress.IPv4Network(ip_address)
        except ipaddress.AddressValueError:
            raise InvalidIpAddressError(ip_address)
        self._ip_address = ip_address

        if not isinstance(configuration, dict):
            raise InvalidConfigurationError("configuration is invalid.")
        self._configuration = configuration

    @property
    def device_type(self) -> DEVICE_TYPES:
        """Return the device type."""
        return self._device_type

    @property
    def ip_address(self) -> str:
        """Return the ip address."""
        return self._ip_address

    @property
    def hostname(self) -> str:
        """Return the hostname."""
        return self._hostname

    @property
    def configuration(self) -> dict:
        """Return the configuration."""
        return self._configuration

    def __str__(self):
        """Return the string representation of the Device."""
        return f"Device(Hostname: {self.hostname}, IP Address: {self.ip_address}, Type: {self.device_type})"
