import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as dates

matplotlib.use('agg')
matplotlib.style.use('ggplot')

def plot(df, title: str, minor_ticks, major_ticks):
    """Plot dataframe with title and ticks specification."""
    ax = df.plot(x_compat=True)           
    # set ticks
    ax.set_xticks(minor_ticks, minor=True)
    ax.xaxis.set_ticks(major_ticks, minor=False)
    ax.xaxis.set_major_formatter(dates.DateFormatter('%Y'))
    plt.gcf().autofmt_xdate(rotation=0, ha="center") 
    # other formatting
    plt.legend(loc="lower left")
    ax.set_title(title, loc='left', fontdict = {'fontsize': 11})
    return ax    

    
def plot_long(df, title, start=2005, end=2020, left_offset=1):
    """Plot starting 2005."""
    df = df[df.index>=str(start)]
    minor_ticks = pd.date_range(str(start-left_offset), str(end), freq='YS')
    major_ticks = pd.date_range(str(start), str(end), freq='5YS') 
    return plot(df, title, minor_ticks, major_ticks)

def save(filename):
    plt.savefig(filename)
