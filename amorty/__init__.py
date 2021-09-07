# -*- coding: utf-8 -*-

"""amorty"""

from amorty.loan import Annuity, StraightLine
from amorty.loan_format import TableFormat, ExcelFormat

__all__ = ['Annuity', 'StraightLine', 'TableFormat', 'ExcelFormat']

__version__ = '0.1.1'
