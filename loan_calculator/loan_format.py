import xlsxwriter

from abc import ABC, abstractmethod
from tabulate import tabulate


class Format(ABC):

    def __init__(self, loan, header: list[str]) -> None:
        self.loan = loan
        self.header = header

    @abstractmethod
    def write(self):
        pass


class TableFormat(Format):

    def write(self) -> None:
        table = self.loan
        print(
            tabulate(
                table,
                headers=self.header,
                floatfmt=",.2f",
                numalign="right",
                tablefmt="rst"
                )
            )


class PDFFormat:
    pass


class ExcelFormat(Format):

    def write(self):
        loan_details = self.loan
        headers = self.header
        with xlsxwriter.Workbook('loan.xlsx') as workbook:
            ws = workbook.add_worksheet()
            bold_font = workbook.add_format({'bold': True})
            date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})

            for col, header in enumerate(headers):
                ws.write_string(0, col, header, bold_font)

            for row, loan in enumerate(loan_details, start=1):
                ws.write(row, 0, loan.date, date_format)
                ws.write(row, 1, loan.day)
                ws.write(row, 2, loan.principal)
                ws.write(row, 3, loan.interest)
                ws.write(row, 4, loan.payment)
                ws.write(row, 5, loan.balance)

