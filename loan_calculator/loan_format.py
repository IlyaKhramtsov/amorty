from abc import ABC, abstractmethod


class Format(ABC):

    def __init__(self, loan, header):
        self.loan = loan
        self.header = header

    @abstractmethod
    def write(self):
        pass


class TableFormat:
    pass


class PDFFormat:
    pass


class ExcelFormat:
    pass

