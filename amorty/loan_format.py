import os
from abc import ABC, abstractmethod
from typing import Iterator, List

import xlsxwriter
from tabulate import tabulate

from amorty import utils
from amorty.loan import LoanDetails


class Format(ABC):
    """Abstract class for building different format of loan schedule."""

    def __init__(self, loan: Iterator[LoanDetails], header: List[str]) -> None:
        self.loan = loan
        self.header = header

    @abstractmethod
    def write(self) -> None:
        pass


class TableFormat(Format):
    """Builds a loan schedule in table format."""

    def write(self) -> None:
        """Output the loan amortization schedule in table format to the terminal."""
        table = self.loan
        print(
            tabulate(
                table,
                headers=self.header,
                floatfmt=",.2f",
                numalign="right",
                tablefmt="rst",
            )
        )


class ExcelFormat(Format):
    """Builds a loan schedule in excel format."""

    @utils.show_progress
    def write(self) -> None:
        """Creates and saves the loan amortization schedule in Excel."""
        loan_details = self.loan
        headers = self.header

        home_path = os.path.expanduser("~")
        filename = "loan.xlsx"
        file_path = os.path.join(home_path, "Downloads", filename)

        with xlsxwriter.Workbook(file_path) as workbook:
            ws = workbook.add_worksheet()
            bold_font = workbook.add_format({"bold": True})
            date_format = workbook.add_format({"num_format": "DD.MM.YYYY"})
            money_format = workbook.add_format({"num_format": "#,##0.00"})

            # Iterate over the headers and write it out column by column
            for col, header in enumerate(headers):
                ws.write_string(0, col, header, bold_font)

            # Iterate over the data and write it out row by row
            for row, loan in enumerate(loan_details, start=1):
                ws.write(row, 0, loan.date, date_format)
                ws.write(row, 1, loan.day)
                ws.write(row, 2, loan.principal, money_format)
                ws.write(row, 3, loan.interest, money_format)
                ws.write(row, 4, loan.payment, money_format)
                ws.write(row, 5, loan.balance, money_format)
