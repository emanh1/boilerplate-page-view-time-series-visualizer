import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')


# Clean data
top = df['value'].quantile(.975)
bot = df['value'].quantile(.025)
df = df[(df['value']>= bot) & (df['value']<=top)]

def draw_line_plot():
    # Draw line plot
    plt.figure(figsize=(32, 10))
    plt.plot(pd.to_datetime(df['date']), df['value'])
    
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019', fontsize=20)
    plt.xlabel('Date', fontsize=20)
    plt.xticks(fontsize=20)
    plt.ylabel('Page Views', fontsize=20)
    plt.yticks(fontsize=20)
    fig = plt.gcf()
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():

    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['date'] = pd.to_datetime(df_bar['date'])
    df_bar['year'] = [d.year for d in df_bar['date']]
    df_bar['month'] = [d.strftime('%B') for d in df_bar['date']]
    # Draw bar plot
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=month_order, ordered=True)
    pivot_df = df_bar.pivot_table(index='year', columns='month', values='value')
    years = pivot_df.index.astype(str)
    months = pivot_df.columns
    bar_width = 0.05
    x = np.arange(len(years))
    fig, ax = plt.subplots(figsize=(15,13))
    for i, month in enumerate(months):
        ax.bar(x+i*bar_width, pivot_df[month], width=bar_width, label=month)
    ax.set_xticks(x + bar_width * (len(months) - 1) / 2)
    ax.set_xticklabels(years)
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.legend(title="Month")
    
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['date'] = pd.to_datetime(df_box['date'])
    df_box['year'] = [d.year for d in df_box['date']]
    df_box['month'] = [d.strftime('%b') for d in df_box['date']]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))

    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1], order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
