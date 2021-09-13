"""The main entry point."""

import argparse
from typing import List, Type, Union

from amorty.loan import Annuity, StraightLine
from amorty.loan_format import ExcelFormat, TableFormat


def main() -> None:
    """Run application."""
    args = get_arguments()
    headers = get_headers()
    loan_method = set_loan_method(args.method)
    loan = loan_method(args.amount, args.period, args.rate, args.date)
    format_type = set_format(args.format)
    formatter = format_type(loan.create_loan(), headers)
    formatter.write()


def get_headers() -> List[str]:
    """Returns a list of headers."""
    return ["Date", "Days", "Principal", "Interest", "Payment", "Balance"]


def get_arguments():
    """Parse the arguments."""
    parser = create_parser()
    return parser.parse_args()


def set_loan_method(method: str) -> Union[Type["Annuity"], Type["StraightLine"]]:
    """Set type of the loan."""
    annuity_methods = ("a", "ann", "annuity")
    straight_line_methods = ("s", "straight-line", "str", "sl")
    if method in annuity_methods:
        return Annuity
    elif method in straight_line_methods:
        return StraightLine
    raise AttributeError(f"Invalid method option: {method}")


def set_format(format_name: str) -> Union[Type["TableFormat"], Type["ExcelFormat"]]:
    """Set output format."""
    if format_name == "table":
        return TableFormat
    elif format_name == "excel":
        return ExcelFormat
    raise AttributeError(f"Invalid format option: {format}")


def create_parser():
    """Creates a parser object."""
    parser = argparse.ArgumentParser(description="Loan amortization tools")
    parser.add_argument(
        "-a",
        "--amount",
        required=True,
        type=float,
        help="Loan amount",
    )

    parser.add_argument(
        "-p",
        "--period",
        required=True,
        type=int,
        help="Loan period in months",
    )

    parser.add_argument(
        "-r",
        "--rate",
        required=True,
        type=float,
        help="Annual interest rate",
    )

    parser.add_argument(
        "-d",
        "--date",
        required=True,
        type=str,
        help='Start date of the loan in format "yyyy-mm-dd"',
    )

    parser.add_argument(
        "-m",
        "--method",
        default="annuity",
        type=str,
        help="Amortization methods (annuity, straight-line)",
    )

    parser.add_argument(
        "-f",
        "--format",
        type=str,
        default="table",
        help="The amortization schedule output format (table, excel)",
    )
    return parser


if __name__ == "__main__":
    main()
