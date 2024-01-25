import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"]= (10,2)
import warnings
warnings.filterwarnings("ignore")
import plotly.express as px

def sliderPlot(df1,t=None):
    if t =="line":
        fig = px.line(x=df1.index, y=df1)
    else:
        fig = px.scatter(x=df1.index, y=df1)
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(count=2, label="2y", step="year", stepmode="backward"),
                dict(count=3, label="3y", step="year", stepmode="backward"),
                dict(step="all")
            ])))
    fig.show()
    return

def scatter(df1):
    plt.scatter(df1.index, df1,s=10)
    plt.xlabel('timestamp')
    # plt.title('current')
    plt.show()

def create_features(hourly_data):
    hourly_data = hourly_data.copy()
    # Check if the index is in datetime format
    if not isinstance(hourly_data.index, pd.DatetimeIndex):
        hourly_data.index = pd.to_datetime(hourly_data.index)
    
    hourly_data['sec'] = hourly_data.index.second
    hourly_data['minute'] = hourly_data.index.minute
    hourly_data['hour'] = hourly_data.index.hour
    hourly_data['day'] = hourly_data.index.day
    hourly_data['dayofweek'] = hourly_data.index.dayofweek
    hourly_data['weekofyear'] = hourly_data.index.isocalendar().week
    hourly_data['month'] = hourly_data.index.month
    return hourly_data
