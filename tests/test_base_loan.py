import pytest

from amorty.loan import Loan

def test_create_instance_abstract_class():
    with pytest.raises(TypeError):
        Loan(amount=1000, period=5, rate=5, date='2021-08-01')
