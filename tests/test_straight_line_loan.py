import pytest

from amorty.loan import StraightLine


@pytest.fixture
def loan():
    return StraightLine(amount=5000, period=5, rate=20, date="2021-05-15")


def test_calculate_principal(loan):
    """ """
    assert round(loan._calculate_principal(), 2) == 1000


def test_loan(loan):
    interest_expected = 252.60
    principal_expected = 5000
    payment_expected = 5252.60
    total_interest = round(sum([x.interest for x in loan.create_loan()]), 2)
    total_principal = round(sum([x.principal for x in loan.create_loan()]), 2)
    total_payment = round(sum([x.payment for x in loan.create_loan()]), 2)
    assert total_interest == interest_expected
    assert total_principal == principal_expected
    assert total_payment == payment_expected
