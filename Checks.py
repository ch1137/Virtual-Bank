import numpy as np
print('numpy version', np.__version__)
import pandas as pd
print('pandas version', pd.__version__)


def valid_date(date):
    try:
        pd.to_datetime(date)
        return True
    except:
        return False


def valid_range(start_date, end_date):
    if pd.to_datetime(f'{start_date}') <= pd.to_datetime(f'{end_date}'):
        return True
    else:
        return False