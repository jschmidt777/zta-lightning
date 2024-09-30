"""Creates report results."""

from datetime import datetime

import xlsxwriter


class AuditReporter:
    """Context manager to handle creation of an audit report."""

    def __init__(self):
        """Initialize the audit report."""

        current_date = datetime.now().strftime("%Y-%m-%d")
        self.filepath = f"zta_compliance_audit_report_{current_date}.xlsx"
        self.workbook = xlsxwriter.Workbook(self.filepath)
        self.worksheet = self.workbook.add_worksheet()
        self.row = 0

    def __enter__(self):
        """Start the audit report."""
        self.worksheet.write(self.row, 0, "Device")
        self.worksheet.write(self.row, 1, "ZTA Check")
        self.worksheet.write(self.row, 2, "Compliance Status")
        self.worksheet.write(self.row, 3, "Details")
        self.row += 1

        return self

    # todo: add more columns for different zta checks, their status, and details
    def add_result(self, device, zta_check, status, details) -> None:
        """Add a result to the audit report

        :param device: a device name
        :param zta_check: the zta check type
        :param status: the compliance status of the check
        :param details: details about the check
        :return: None
        """
        self.worksheet.write(self.row, 0, device)
        self.worksheet.write(self.row, 1, zta_check)
        self.worksheet.write(self.row, 2, status)
        self.worksheet.write(self.row, 3, details)
        self.row += 1

    def __exit__(self, exc_type, exc_value, traceback):
        """Create the audit report."""
        self.workbook.close()
