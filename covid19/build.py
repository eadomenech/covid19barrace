from datetime import date, datetime

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation

from confirmed_province import build_confirmed_data
from deceased_province import build_deceased_data
from utils import utils


def build_confirmed(date_end, intermediate_days=1):

    build_confirmed_data(date_end, intermediate_days=intermediate_days)

    df = pd.read_csv (f"data/province_confirmed_{intermediate_days}.csv")

    mesesDic = utils.mesesDic

    fig, ax = plt.subplots(figsize=(15, 8))
    fig.subplots_adjust(
        left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)

    def draw_barchart(date):
        dff = df[df['date'].eq(date)].sort_values(
            by='accumulated_confirmed', ascending=True).tail(16)
        ax.clear()

        normal_colors = utils.normal_colors
        
        ax.barh(
            dff['province'], dff['accumulated_confirmed'],
            color = [normal_colors[x] for x in dff['province']])
        dx = dff['accumulated_confirmed'].max() / 100
        for i, (value, name) in enumerate(
                zip(dff['accumulated_confirmed'], dff['province'])):
            ax.text(0, i, name, size=12, weight=800, ha='right')
            ax.text(
                value+dx, i, f'{value:,.0f}', size=10, ha='left',
                va='center')
            
        # ... polished styles
        ax.text(
            1, 0.4,
            mesesDic[datetime.strptime(date, '%Y-%m-%d').month],
            transform=ax.transAxes,
            color='#766712', size=56, ha='right', weight=500)
        ax.text(
            1, 0.3, date, transform=ax.transAxes, color='#777777',
            size=30, ha='right', weight=500)
        ax.text(
            0, 1.06, 'Casos Confirmados', transform=ax.transAxes,
            size=12, color='#777777')
        ax.xaxis.set_major_formatter(
            ticker.StrMethodFormatter('{x:,.0f}'))
        ax.xaxis.set_ticks_position('top')
        ax.tick_params(axis='x', colors='#777777', labelsize=8)
        ax.set_yticks([])
        ax.margins(0, 0.01)
        ax.grid(which='major', axis='x', linestyle='-')
        ax.set_axisbelow(True)
        # ax.text(
        #     0, 1.12,
        #     '\n\nCOVID-19 Casos Confirmados (11/03/2020 - 02/03/2021)',
        #     transform=ax.transAxes, size=16, weight=400, ha='left')
        plt.box(False)
        plt.tight_layout()
        
    dates=pd.Series(pd.to_datetime(df['date'].unique()))
    dates = dates.where(dates <= date_end)
    dates.dropna(inplace=True)
    dates = dates.astype(str)

    fig, ax = plt.subplots(figsize=(15, 8))
    animator = animation.FuncAnimation(fig, draw_barchart, frames=dates)
    animator.save(
        f"static/confirmed_h{intermediate_days}.gif",
        writer='imagemagick', fps=6, extra_args=['-loop','1'])

    # os.system(
    #     'convert -size 1500x800 static/confirmed.gif -resize 750x400 download/confirmed.gif')


def build_deceased(date_end, intermediate_days=1):

    build_deceased_data(date_end, intermediate_days=intermediate_days)

    df = pd.read_csv (f"data/province_deceased_{intermediate_days}.csv")

    mesesDic = utils.mesesDic

    fig, ax = plt.subplots(figsize=(15, 8))
    fig.subplots_adjust(
        left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)

    def draw_barchart(date):
        dff = df[df['date'].eq(date)].sort_values(
            by='accumulated_deceased', ascending=True).tail(16)
        ax.clear()

        normal_colors = utils.normal_colors
        
        ax.barh(
            dff['province'], dff['accumulated_deceased'],
            color = [normal_colors[x] for x in dff['province']])
        dx = dff['accumulated_deceased'].max() / 100
        for i, (value, name) in enumerate(
                zip(dff['accumulated_deceased'], dff['province'])):
            ax.text(0, i, name, size=12, weight=800, ha='right')
            ax.text(
                value+dx, i, f'{value:,.0f}', size=10, ha='left',
                va='center')
            
        # ... polished styles
        ax.text(
            1, 0.4,
            mesesDic[datetime.strptime(date, '%Y-%m-%d').month],
            transform=ax.transAxes,
            color='#766712', size=56, ha='right', weight=500)
        ax.text(
            1, 0.3, date, transform=ax.transAxes, color='#777777',
            size=30, ha='right', weight=500)
        ax.text(
            0, 1.06, 'Fallecidos', transform=ax.transAxes,
            size=12, color='#777777')
        ax.xaxis.set_major_formatter(
            ticker.StrMethodFormatter('{x:,.0f}'))
        ax.xaxis.set_ticks_position('top')
        ax.tick_params(axis='x', colors='#777777', labelsize=8)
        ax.set_yticks([])
        ax.margins(0, 0.01)
        ax.grid(which='major', axis='x', linestyle='-')
        ax.set_axisbelow(True)
        # ax.text(
        #     0, 1.12,
        #     '\n\nCOVID-19 Fallecidos (11/03/2020 - 02/03/2021)',
        #     transform=ax.transAxes, size=16, weight=400, ha='left')
        plt.box(False)
        plt.tight_layout()
        
    dates=pd.Series(pd.to_datetime(df['date'].unique()))
    dates = dates.where(dates <= date_end)
    dates.dropna(inplace=True)
    dates = dates.astype(str)

    fig, ax = plt.subplots(figsize=(15, 8))
    animator = animation.FuncAnimation(fig, draw_barchart, frames=dates)
    animator.save(
        f"static/deceased_h{intermediate_days}.gif",
        writer='imagemagick', fps=6, extra_args=['-loop','1'])

    # os.system(
    #     'convert -size 1500x800 static/deceased.gif -resize 750x400 download/deceased.gif')