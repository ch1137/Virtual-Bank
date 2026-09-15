import numpy as np
import pandas as pd


def number_of_days(start_date, end_date):
    days = np.arange(f'{start_date}', f'{end_date}', dtype='datetime64[D]')
    return len(days)


def days_to_month_end(start_date):
    start_year = pd.to_datetime(f'{start_date}').year
    start_month = pd.to_datetime(f'{start_date}').month
    end_date = np.datetime64(f'{start_year:04d}-{start_month:02d}') + np.timedelta64(1, 'M')
    days = np.arange(f'{start_date}', f'{end_date}', dtype='datetime64[D]')
    return days, end_date


def no_days_in_year(start_date):
    start_year = pd.to_datetime(f'{start_date}').year
    days_in_year = number_of_days(start_date=start_year,
                                    end_date=start_year + 1)
    return days_in_year


def day_step(start_date, delta):
    return np.datetime64(f'{start_date}') + np.timedelta64(int(delta), 'D')


def date_spliter(date):
    y = pd.to_datetime(f'{date}').year
    m = pd.to_datetime(f'{date}').month
    d = pd.to_datetime(f'{date}').day
    return y, m, d

def date_merger(y, m, d= 1):
    ymd = np.datetime64(f'{y:04d}-{m:02d}-{d:02d}')
    ym = np.datetime64(f'{y:04d}-{m:02d}')
    return ymd, ym