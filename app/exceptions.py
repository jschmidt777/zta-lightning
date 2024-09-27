"""Exceptions."""


class InvalidNetworkDeviceValueError(Exception):
    """Invalid network device value provided."""

    def __init__(self, invalid_value):
        super().__init__(f"Invalid value: {invalid_value}.")


class InvalidDeviceTypeError(InvalidNetworkDeviceValueError):
    """Invalid device type."""

    pass


class InvalidHostnameError(InvalidNetworkDeviceValueError):
    """Invlaid hostname."""

    pass


class InvalidIpAddressError(InvalidNetworkDeviceValueError):
    """Invlaid ip address."""

    pass


class InvalidConfigurationError(InvalidNetworkDeviceValueError):
    """Invalid configuration."""

    pass
