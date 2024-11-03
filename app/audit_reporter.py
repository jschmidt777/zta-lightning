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
        self._filepath = f"zta_compliance_audit_report_{current_date}.xlsx"
        self._workbook = xlsxwriter.Workbook(self._filepath)
        self._worksheet = self._workbook.add_worksheet()
        self._row = 1
        self._device_rows = {}
        self._col_headers = {}

    def __enter__(self):
        """Start the audit report."""
        self._worksheet.write(0, 0, "Device")
        return self

    def add_result(self, device, zta_check: ZtaCheckType, status, details) -> None:
        """Add or update a result in the audit report for a given device."""

        if zta_check not in self.VALID_ZTA_CHECKS:
            raise ValueError(f"Invalid ZTA Check: '{zta_check}'. Must be one of {self.VALID_ZTA_CHECKS}.")

        if device not in self._device_rows:
            self._device_rows[device] = self._row
            self._worksheet.write(self._row, 0, device)
            self._row += 1

        device_row = self._device_rows[device]

        if zta_check not in self._col_headers:
            col = len(self._col_headers) * 3 + 1
            self._col_headers[zta_check] = col
            self._worksheet.write(0, col, f"{zta_check} - Status")
            self._worksheet.write(0, col + 1, f"{zta_check} - Details")

        col = self._col_headers[zta_check]

        self._worksheet.write(device_row, col, status)
        self._worksheet.write(device_row, col + 1, details)

    def __exit__(self, exc_type, exc_value, traceback):
        """Create the audit report."""
        columns_to_format = ['B', 'E', 'H', 'K']
        for col in columns_to_format:
            self._worksheet.conditional_format(f'{col}2:{col}{len(self._device_rows) + 1}', {
                'type': 'cell',
                'criteria': '==',
                'value': True,
                'format': self._workbook.add_format({'bg_color': '#C6EFCE'})
            })

            self._worksheet.conditional_format(f'{col}2:{col}{len(self._device_rows) + 1}', {
                'type': 'cell',
                'criteria': '==',
                'value': False,
                'format': self._workbook.add_format({'bg_color': '#FFC7CE'})
            })
        print(f"ZTA compliance audit report successfully created: {self._filepath}. Total"
              f" devices processed: {len(self._device_rows)}")
        self._workbook.close()
