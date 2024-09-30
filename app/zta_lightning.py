"""ZTA Lightning
Author: Joe Schmidt"""

from app.audit_reporter import AuditReporter
from app.domain_model import Device
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
    device_data = api_client.get_all_device_data()
    device_data = device_data.get("configurations")
    normalized_device_data = [Device(device) for device in device_data.values()]
    logging_check = LoggingCheck(normalized_device_data)
    logging_results = logging_check.run_logging_checks()
    # todo: change this use of the context manager for reporting
    with AuditReporter() as audit_reporter:
        for result in logging_results:
            audit_reporter.add_result(
                result.hostname,
                "logging",
                result.compliant,
                f"logging_enabled: {result.logging_enabled}, centralized_logging_server: {result.centralized_logging_server}, required_logging_level: {result.required_logging_level}",
            )

    # create the final audit report
    # todo: add an output to a custom directory in the tool called audit_reports


if __name__ == "__main__":
    main()
