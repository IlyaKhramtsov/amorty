import argparse
from loan_calculator.loan import AnnuityLoan, DifferentiatedLoan
from loan_calculator.loan_format import TableFormat, ExcelFormat, PDFFormat


def main():
    args = get_arguments()
    headers = ['Date', 'Day', 'Principal', 'Interest', 'Payment', 'Balance']
    loan_method = set_loan_method(args.method)
    loan = loan_method(args.amount, args.period, args.rate, args.date)
    format_type = set_format(args.format)
    formatter = format_type(loan.create_loan(), headers)
    formatter.write()

def get_arguments():
    """Parse the arguments."""
    parser = create_parser()
    return parser.parse_args()

def set_loan_method(method):
    """Set type of the loan."""
    annuity_methods = ('a', 'ann', 'annuity')
    differentiated_methods = ('d', 'diff', 'different', 'differentiated')
    if method in annuity_methods:
        return AnnuityLoan
    elif method in differentiated_methods:
        return DifferentiatedLoan
    raise AttributeError(f'Invalid method option: {method}')

def set_format(format_name):
    """Set output format"""
    if format_name == 'table':
        return TableFormat
    elif format_name == 'excel':
        return ExcelFormat
    elif format_name == 'pdf':
        return PDFFormat

def create_parser():
    """Creates a parser object"""
    parser = argparse.ArgumentParser(description='Loan amortization tools')
    parser.add_argument(
            '-a',
            '--amount',
            required=True,
            type=float,
            help='loan amount')

    parser.add_argument(
            '-p',
            '--period',
            required=True,
            type=int,
            help='loan period in months')

    parser.add_argument(
            '-r',
            '--rate',
            required=True,
            type=float,
            help='annual interest rate')

    parser.add_argument(
            '-d',
            '--date',
            required=True,
            type=str,
            help='start date of the loan in format "yyyy-mm-dd"')

    parser.add_argument(
            '-m',
            '--method',
            default='annuity',
            type=str,
            help='loan methods (annuity, differentiated)')

    parser.add_argument(
            '-f',
            '--format',
            type=str,
            default='table',
            help='format output (table/excel/pdf)')
    return parser


if __name__ == "__main__":
    main()


