import numpy as np
import itertools as it

import Date_Calculations as dc
import Checks


def single_debit(value, date, end_date, open_date = 'start_date', frequency=1):
    if open_date == 'start_date':
        open_date = date

    total_days = dc.number_of_days(start_date=open_date, end_date=date)
    transactions = np.zeros(total_days + 1)
    transactions[-1] = value

    return transactions

def daily_debit(value, start_date, end_date, open_date = 'start_date', frequency=1):
    if open_date == 'start_date':
        open_date = start_date

    total_days = dc.number_of_days(start_date=open_date, end_date=end_date)
    start_day = dc.number_of_days(start_date=open_date, end_date=start_date)
    transactions = np.zeros(total_days+1)

    for index in range(start_day, total_days+1, frequency):
        transactions[index] = value

    return transactions


def weekly_debit(value, start_date, end_date, open_date = 'start_date', frequency=1):
    return daily_debit(value, start_date, end_date, open_date = open_date, frequency= 7*frequency)


def monthly_debit(value, start_date, end_date, open_date='start_date', frequency=1):
    if open_date == 'start_date':
        open_date = start_date

    total_days = dc.number_of_days(start_date= open_date, end_date= end_date)
    start_day = dc.number_of_days(start_date= open_date, end_date= start_date)
    sy, sm, sd = dc.date_spliter(start_date)
    transactions = np.zeros(total_days + 1)

    index = start_day
    i = 1
    while index <= total_days:
        transactions[index] = value
        new_date = np.datetime64(f'{sy:04d}-{sm:02d}') + np.timedelta64(i*frequency, 'M')
        index = dc.number_of_days(start_date= open_date, end_date= new_date) + sd-1
        if sd > len(dc.days_to_month_end(new_date)[0]):
            nd = len(dc.days_to_month_end(new_date)[0])
            index += nd - sd
        i += 1
    return transactions


def yearly_debit(value, start_date, end_date, open_date = 'start_date', frequency=1):
    return monthly_debit(value, start_date, end_date, open_date = open_date, frequency= 12*frequency)


def total_debit(open_date, *debits):                     #args in form [type, value, start, end, frequency]
    style = {'daily':daily_debit, 'weekly':weekly_debit,
             'monthly':monthly_debit, 'yearly':yearly_debit,
             'single':single_debit}
    total_transactions = []

    for debit in debits:
        if len(debit) == 3:                     #single day debits only require start date and have no frequency
            debit = debit + [debit[2]] + [0]

        if (Checks.valid_date(debit[2]) == False
                or Checks.valid_date(debit[3]) == False
                or Checks.valid_date(open_date) == False):
            return 'Invalid date'
        if (Checks.valid_range(open_date, debit[2]) == False
                or Checks.valid_range(open_date, debit[3]) == False
                or Checks.valid_range(debit[2], debit[3]) == False):
            return 'Invalid date range'

        transactions = style[debit[0]](debit[1], debit[2], debit[3],
                                       open_date= open_date, frequency= debit[4])
        total_transactions = list(map(sum,
                                      it.zip_longest(total_transactions, transactions,fillvalue=0)))
    return np.array(total_transactions).view(dtype=float)



daily1 = ['daily', 10, '2026-01-02', '2026-01-07',1]
daily2 = ['single', 10, '2026-01-03']
print(total_debit('2026', daily1,daily2))