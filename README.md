# Amorty

[![Github Actions Status](https://github.com/IlyaKhramtsov/amorty/workflows/Python%20CI/badge.svg)](https://github.com/IlyaKhramtsov/amorty/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


**Amorty** is a command line interface (CLI) utility for accurate loan calculation and creating amortization schedule. You can output both **straight-line** and **annuity** method of amortization schedules.
> **Amorty builds a loan repayment schedule taking into account Russian specifics.**
> If the payment date falls on a day off (Saturday, Sunday) or a non-working holiday, then the corresponding amount of debt on the loan is repaid on the next working day after it.

Amotry uses the **Actual / Actual** method when calculating interest payments.
> The Actual/Actual method uses the actual number of days in each month and year.
 
 #### Methods for Amortization Schedule
> An amortization schedule is a table that provides the periodic payment information for an amortizing loan

Amorty has two methods to amortize a loan. Different methods lead to different amortization schedules. 

***Straight-line***

*Straight-Line* amortization is a simple method of loan repayment. In this process, the same amount is paid toward the principal each month, but the amount paid toward interest decreases over time with the outstanding balance of the loan. This type of amortization pays down the loan more quickly,  but requires higher payments on the front end. 

***Annuity***

Amortization of an annuity loan is a method in which you pay a fixed monthly amount consisting of interest and repayment of the principal. The monthly amount remains unchanged throughout the entire loan term.

Initially, most of your payments will go towards paying interest, but as the amount of your debt decreases, the interest decreases and more goes towards paying off principal.

## Installation

```bash
>>> pip install --user --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ amorty
```

## Usage


### As CLI tool

```bash
$ amorty -a 1000 -p 5 -r 20 -d 2020-05-15 -m annuity
==========  =====  ===========  ==========  =========  =========
Date          Day    Principal    Interest    Payment    Balance
==========  =====  ===========  ==========  =========  =========
2020-06-15     31       193.17       16.94     210.11     806.83
2020-07-15     30       196.88       13.23     210.11     609.95
2020-08-17     33       199.11       11.00     210.11     410.84
2020-09-15     29       203.60        6.51     210.11     207.24
2020-10-15     30       207.24        3.40     210.63       0.00
==========  =====  ===========  ==========  =========  =========
```
```bash
>>> amorty -a 1000 -p 5 -r 20 -d 2019-10-23 -m straight-line
==========  =====  ===========  ==========  =========  =========
Date          Day    Principal    Interest    Payment    Balance
==========  =====  ===========  ==========  =========  =========
2019-11-25     33       200.00       18.08     218.08     800.00
2019-12-23     28       200.00       12.27     212.27     600.00
2020-01-23     31       200.00       10.17     210.17     400.00
2020-02-24     32       200.00        6.99     206.99     200.00
2020-03-23     28       200.00        3.06     203.06       0.00
==========  =====  ===========  ==========  =========  =========
```

#### Options:
##### `-a, --amount`
The amount that you want to borrow, which is indicated in your loan agreement.
##### `-p, --period`
An integer number of months for which the loan is taken.
##### `-r, --rate`
Annual interest rate.
##### `-d, --date`
Date on which money is received by the borrower.
##### `-m, --method`
Amortization methods include the 'straight line' and 'annuity'.
##### `-f, --format`
The amortization schedule output format includes 'table' and 'excel'. 
If the "excel" option is selected, the file will be uploaded to the "Downloads" folder with the name loan.xlsx
