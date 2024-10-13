"""Exceptions."""


class InvalidDeviceValueError(Exception):
    """Invalid network device value provided."""

    def __init__(self, invalid_value):
        super().__init__(f"Invalid device value: {invalid_value}.")


class InvalidDeviceTypeError(InvalidDeviceValueError):
    """Invalid device type."""

    pass


class InvalidHostnameError(InvalidDeviceValueError):
    """Invlaid hostname."""

    pass


class InvalidIpAddressError(InvalidDeviceValueError):
    """Invalid ip address."""

    pass


class InvalidConfigurationError(InvalidDeviceValueError):
    """Invalid configuration."""

    pass


class InvalidUserValueError(Exception):
    """Invalid user info. value provided."""

    def __init__(self, invalid_value):
        super().__init__(f"Invalid user info. value: {invalid_value}.")


class InvalidUsernameError(InvalidUserValueError):
    """Invalid username."""

    pass


class InvalidUserDevicesError(InvalidUserValueError):
    """Invalid user devices."""

    pass


class InvalidUserRolesError(InvalidUserValueError):
    """Invalid user roles."""

    pass
