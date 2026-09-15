import numpy as np

import Date_Calculations as dc
import Checks


def daily_interest(account_value, percent_APR, days_in_year):
    dAPR = (1+(percent_APR/100))**(1 / days_in_year)
    return account_value * (dAPR-1)

def run_period(start_date, end_date, percent_APR, transactions):
    if (Checks.valid_date(start_date) == False
            or Checks.valid_date(end_date) == False):
        return 'Invalid date'
    if Checks.valid_range(start_date, end_date) == False:
        return 'Invalid date range'

    total_days = dc.number_of_days(start_date, end_date)
    interest_day = [0]
    interest = 0
    account_value = np.zeros(total_days +1)
    account_value[0] = transactions[0]
    month_start = start_date
    year_days = dc.no_days_in_year(start_date)

    while interest_day[-1] <= total_days:
        month_start = dc.days_to_month_end(month_start)[1]
        interest_day.append(dc.number_of_days(start_date, month_start))

    for day in range(1, total_days+1):
        interest += daily_interest(account_value[day-1]+ interest, percent_APR, year_days)
        account_value[day] = account_value[day-1] + transactions[day]
        if day in interest_day:
            account_value[day] += interest
            interest = 0
            year_days = dc.no_days_in_year(dc.day_step(start_date, day))
    return account_value
