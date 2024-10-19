"""ZTA Lightning
Author: Joe Schmidt"""

from app.audit_reporter import AuditReporter
from app.domain_models import Device, User
from app.zta_checks.auth_and_ac import AuthAndACCheck
from app.zta_checks.logging import LoggingCheck
from app.cli import CLI
from app.client import APIClient


def main():
    """Run the ZTA Lightning application.

    :return: None
    """

    # get configuration details from the user
    # and confirm connection to network appliance
    cli = CLI()
    cli.display_banner()
    cli.display_instructions()
    api_client = APIClient()
    api_client.authenticate()
    api_client.test_connection()

    # with the connection confirmed, start the zta compliance audit
    # by getting device configurations and normalizing the data
    device_data = api_client.get_all_device_data()
    device_data = device_data.get("configurations")
    normalized_device_data = [Device(device) for device in device_data.values()]

    # conduct checks on zta principles and report compliance
    with AuditReporter() as audit_reporter:
        logging_check = LoggingCheck(normalized_device_data)
        logging_check.run_logging_checks(audit_reporter)
        user_data = api_client.get_all_user_info()
        user_data = user_data.get("users")
        normalized_user_data = [User(user) for user in user_data.values()]
        auth_and_ac_check = AuthAndACCheck(normalized_device_data, normalized_user_data)
        auth_and_ac_check.run_auth_and_ac_checks(audit_reporter)

    # create the final audit report
    # todo: add an output to a custom directory in the tool called audit_reports


if __name__ == "__main__":
    main()
