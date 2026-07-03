from scipy import stats

class SeaLevelAnalysis:
    def __init__(self, series):
        """
        Parameters
        ----------
        series : pandas.Series
            Sea level values (mm) indexed by date.
        """
        self.series = series

    def compute_trend(self):
        """
        Compute the long-term linear trend of a sea level time series.

        Returns
        -------
        dict
            Dictionary with 'trend_mm_per_year', 'r_squared', and 'p_value'.
        """
        clean = self.series.dropna()
        years = clean.index.year + (clean.index.month - 1) / 12
        slope, intercept, r_value, p_value, std_err = stats.linregress(years, clean.values)
        return {
            'trend_mm_per_year': slope,
            'r_squared': r_value**2,
            'p_value': p_value
        } # return is a dictionary as specified above

    def seasonal_cycle(self):
        """
        Compute the average seasonal cycle (mean sea level per calendar month).

        Returns
        -------
        pandas.Series
            Mean sea level for each calendar month (index 1-12).
        """
        clean = self.series.dropna()
        return clean.groupby(clean.index.month).mean()

    def plot_seasonal_cycle(self, title="Seasonal Cycle", save_path=None):
        """
        Plot the seasonal cycle of sea level as a bar chart.

        Parameters
        ----------
        title : str
            Plot title.
        save_path : str or None
            If provided, saves the figure to this path.

        Returns
        -------
        matplotlib.axes.Axes
        """
        cycle = self.seasonal_cycle()
        ax = cycle.plot(kind='bar', title=title,
                         xlabel='Month', ylabel='Mean sea level (mm)')
        ax.set_ylim(cycle.min() - 20, cycle.max() + 20)
        if save_path:
            ax.figure.savefig(save_path, dpi=150, bbox_inches='tight')
        return ax
