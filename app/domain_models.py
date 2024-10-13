"""Domain model for device."""

import ipaddress
from typing import Any

from app.exceptions import (
    InvalidDeviceTypeError,
    InvalidHostnameError,
    InvalidIpAddressError,
    InvalidConfigurationError,
    InvalidUserDevicesError,
    InvalidUserRolesError,
    InvalidUsernameError,
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
        return f"Device(Hostname: {self._hostname}, IP Address: {self._ip_address}, Type: {self._device_type})"


class User:
    """A user on the network."""

    def __init__(self, user: JSON):
        username = user.get("username")
        devices = user.get("devices")
        roles = user.get("roles")

        if len(username) > 50:
            raise InvalidUsernameError(username)
        self._username = username

        if len(devices) == 0 or not isinstance(devices, list):
            raise InvalidUserDevicesError(devices)
        self._devices = devices

        if len(roles) == 0 or not isinstance(roles, list):
            raise InvalidUserRolesError(devices)
        self._roles = roles

    @property
    def username(self) -> str:
        """Return the username."""
        return self._username

    @property
    def devices(self) -> list:
        """Return the user devices."""
        return self._devices

    @property
    def roles(self) -> list:
        """Return the user roles."""
        return self._roles

    def __str__(self):
        """Return the string representation of the User."""
        return f"User(Username: {self._username}, Roles: {self._roles})"
