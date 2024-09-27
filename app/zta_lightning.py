"""ZTA Lightning
Author: Joe Schmidt"""

from pprint import pprint

from app.reporter import Reporter
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
    reporter = Reporter()
    device_data = api_client.get_all_device_data()
    pprint(device_data)
    # logging_check = LoggingCheck()
    # logging_results = logging_check.run(device_data)
    # reporter.add_results(logging_results)

    # create the final audit report
    # reporter.export_audit()


if __name__ == "__main__":
    main()
