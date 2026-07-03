import pandas as pd
import numpy as np


def load_station_series(filepath):
    """
    Load and clean a PSMSL RLR monthly sea level file.

    Parameters
    ----------
    filepath : str
        Path to the raw PSMSL .rlrdata.txt file.

    Returns
    -------
    pandas.DataFrame
        Indexed by date (mid-month convention, day=15), with columns:
        'sea_level_mm' (float, NaN for missing months) and
        'interpolated_flag' (int, 0 = observed, 1 = interpolated).
        The decision are better explained in the README file
    """
    df = pd.read_csv(filepath, sep=';', header=None,
                      names=['date_decimal', 'sea_level_mm', 'interpolated_flag', 'missing_days'])

    df['sea_level_mm'] = df['sea_level_mm'].replace(-99999, np.nan) 

    df['year'] = df['date_decimal'].astype(int)
    df['month'] = np.floor((df['date_decimal'] - df['year']) * 12).astype(int) + 1
    df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=15)) #day is setted at 15 a previous trial with 1 individuated
    #some errors since the sampling is done at half of each month

    return df[['date', 'sea_level_mm', 'interpolated_flag', 'missing_days']].set_index('date')