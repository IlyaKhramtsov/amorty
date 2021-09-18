import pytest

from amorty.loan import Annuity


@pytest.fixture
def loan():
    return Annuity(amount=1000, period=5, rate=20, date="2021-05-15")


def test_monthly_interest(loan):
    expected = 20 / 1200
    assert loan._calculate_monthly_interest() == pytest.approx(expected, 2)


def test_annuity_payment(loan):
    expected = 210.11
    result = loan.get_annuity_payment()
    assert result == pytest.approx(expected, 2)


def test_payments(loan):
    expected = 1050.99
    amortization = [x for x in zip(*loan.amortize())]
    assert round(sum(amortization[0]), 2) == pytest.approx(expected, 2)


def test_loan(loan):
    interest_expected = 51.10
    principal_expected = 1000
    payment_expected = 1051.10
    total_interest = round(sum([x.interest for x in loan.create_loan()]), 2)
    total_principal = round(sum([x.principal for x in loan.create_loan()]), 2)
    total_payment = round(sum([x.payment for x in loan.create_loan()]), 2)
    assert total_interest == interest_expected
    assert total_principal == principal_expected
    assert total_payment == payment_expected


def test_loan_details(loan):
    assert loan.amount == 1000
    assert loan.period == 5
    assert loan.rate == 20


@pytest.mark.parametrize("expected", [(-1000), ("1000")])
def test_wrong_amount(loan, expected):
    with pytest.raises(ValueError):
        loan.amount = expected


@pytest.mark.parametrize("expected", [(-1), ("24")])
def test_wrong_period(loan, expected):
    with pytest.raises(ValueError):
        loan.period = expected


@pytest.mark.parametrize("expected", [(-10), ("5")])
def test_wrong_rate(loan, expected):
    with pytest.raises(ValueError):
        loan.rate = expected
