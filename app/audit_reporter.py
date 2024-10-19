"""Creates audit report results."""

from typing import Literal

import xlsxwriter
from datetime import datetime


class AuditReporter:
    """Context manager to handle creation of an audit report."""

    VALID_ZTA_CHECKS = {"Logging", "Auth and AC", "Network Segmentation", "Least Privilege"}
    ZtaCheckType = Literal["Logging", "Auth and AC", "Network Segmentation", "Least Privilege"]

    def __init__(self):
        """Initialize the audit report."""
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.filepath = f"zta_compliance_audit_report_{current_date}.xlsx"
        self.workbook = xlsxwriter.Workbook(self.filepath)
        self.worksheet = self.workbook.add_worksheet()
        self.row = 1
        self.device_rows = {}
        self.col_headers = {}

    def __enter__(self):
        """Start the audit report."""
        self.worksheet.write(0, 0, "Device")
        return self

    def add_result(self, device, zta_check: ZtaCheckType, status, details) -> None:
        """Add or update a result in the audit report for a given device."""

        if zta_check not in self.VALID_ZTA_CHECKS:
            raise ValueError(f"Invalid ZTA Check: '{zta_check}'. Must be one of {self.VALID_ZTA_CHECKS}.")

        if device not in self.device_rows:
            self.device_rows[device] = self.row
            self.worksheet.write(self.row, 0, device)
            self.row += 1

        device_row = self.device_rows[device]

        if zta_check not in self.col_headers:
            col = len(self.col_headers) * 3 + 1
            self.col_headers[zta_check] = col
            self.worksheet.write(0, col, f"{zta_check} - Status")
            self.worksheet.write(0, col + 1, f"{zta_check} - Details")

        col = self.col_headers[zta_check]

        self.worksheet.write(device_row, col, status)
        self.worksheet.write(device_row, col + 1, details)

    def __exit__(self, exc_type, exc_value, traceback):
        """Create the audit report."""
        self.workbook.close()
