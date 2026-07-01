{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "48259ee2-a7dd-42a6-a440-f573c3d9ec86",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "\n",
    "\n",
    "def load_station_series(filepath):\n",
    "    \"\"\"\n",
    "    Load and clean a PSMSL RLR monthly sea level file.\n",
    "\n",
    "    Parameters\n",
    "    ----------\n",
    "    filepath : str\n",
    "        Path to the raw PSMSL .rlrdata.txt file.\n",
    "\n",
    "    Returns\n",
    "    -------\n",
    "    pandas.DataFrame\n",
    "        Indexed by date (mid-month convention, day=15), with columns:\n",
    "        'sea_level_mm' (float, NaN for missing months) and\n",
    "        'interpolated_flag' (int, 0 = observed, 1 = interpolated).\n",
    "    \"\"\"\n",
    "    df = pd.read_csv(filepath, sep=';', header=None,\n",
    "                      names=['date_decimal', 'sea_level_mm', 'interpolated_flag', 'missing_days'])\n",
    "\n",
    "    df['sea_level_mm'] = df['sea_level_mm'].replace(-99999, np.nan)\n",
    "\n",
    "    df['year'] = df['date_decimal'].astype(int)\n",
    "    df['month'] = np.floor((df['date_decimal'] - df['year']) * 12).astype(int) + 1\n",
    "    df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=15))\n",
    "\n",
    "    return df[['date', 'sea_level_mm', 'interpolated_flag']].set_index('date')"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python (sltk)",
   "language": "python",
   "name": "sltk-env"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.14.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
