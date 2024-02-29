from plotly.subplots import make_subplots
import plotly.graph_objects as go
from pandas import DataFrame
from typing import Optional
import pandas as pd


def plot_preds(train_df: DataFrame,
               valid_df: DataFrame,
               pred_df: DataFrame,
               calendar_df: DataFrame,
               plot_train_data: Optional[bool] = False) -> None:
    """
    Plots the training, validation, and prediction data for a series of 
    time series.

    Args:
        train_df (DataFrame): DataFrame containing the training data.
        valid_df (DataFrame): DataFrame containing the validation data.
        pred_df (DataFrame): DataFrame containing the prediction data.
        calendar_df (DataFrame): DataFrame containing the calendar data to
        merge based on 'd' column for date mapping.
        plot_train_data (bool, optional): Flag to determine if training data
        should be plotted. Defaults to False.
    """

    n_ts = len(train_df)
    if n_ts > 10:                 # limiting the number of timeseries that can
        # be plotted to reduce plotly runtime
        n_ts = 10
        train_df = train_df.iloc[:10, :]
        print('Since there are more than 10 timeseries, plotting only top 10' +
              'as an example')

    fig = make_subplots(rows=n_ts, cols=1, subplot_titles=[
                        id.replace('_validation', '') for id in train_df['id']])

    for i in range(n_ts):

        train_ts_df = train_df[
            [col for col in train_df.columns if 'd_' in col]
        ].iloc[i].reset_index().rename(columns={'index': 'd'})
        valid_ts_df = valid_df[
            [col for col in valid_df.columns if 'd_' in col]
        ].iloc[i].reset_index().rename(columns={'index': 'd'})
        pred_ts_df = pred_df
        [[col for col in pred_df.columns if 'd_' in col]
         ].iloc[i].reset_index().rename(columns={'index': 'd'})

        train_ts_df = pd.merge(train_ts_df, calendar_df[['d', 'date']])
        valid_ts_df = pd.merge(valid_ts_df, calendar_df[['d', 'date']])
        pred_ts_df = pd.merge(pred_ts_df, calendar_df[['d', 'date']])

        # showlegend = True if i == 0 else False

        if plot_train_data:
            fig.add_trace(
                go.Scatter(x=train_ts_df['date'],
                           y=train_ts_df.iloc[:, 1],
                           name='training', line=dict(
                    color='blue'),
                    showlegend=True if i == 0 else False,
                    legendgroup=str(i)), row=i+1, col=1)
        fig.add_trace(go.Scatter(x=valid_ts_df['date'],
                                 y=valid_ts_df.iloc[:, 1],
                                 name='validation', line=dict(
            color='black'), showlegend=True if i == 0 else False,
            legendgroup=str(i)), row=i+1, col=1)
        fig.add_trace(go.Scatter(
            x=pred_ts_df['date'],  y=pred_ts_df.iloc[:, 1],
            name='predictions', line=dict(
                color='green'),
            showlegend=True if i == 0 else False,
            legendgroup=str(i)), row=i+1, col=1)

    fig.update_layout(height=n_ts*180, margin=dict(l=0, r=0,
                      b=0, t=20), legend_tracegroupgap=150)
    fig.show()
