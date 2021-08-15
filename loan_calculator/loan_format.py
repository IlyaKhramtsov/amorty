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


class ExcelFormat:
    pass

