import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression


def generate_forecast(df, date_col, target_col, periods):

    data = df[[date_col, target_col]].copy()

    data[date_col] = pd.to_datetime(
    data[date_col],
    format="mixed",
    dayfirst=True,
    errors="coerce"
    )

    data = data.dropna(subset=[date_col])

    data = data.sort_values(date_col)

    data = data.groupby(date_col)[target_col].sum().reset_index()

    data["Day"] = np.arange(len(data))

    X = data[["Day"]]
    y = data[target_col]

    model = LinearRegression()

    model.fit(X, y)

    future_days = np.arange(
        len(data),
        len(data) + int(periods)
    )

    future_pred = model.predict(
        future_days.reshape(-1, 1)
    )

    future_dates = pd.date_range(
        start=data[date_col].max() + pd.Timedelta(days=1),
        periods=int(periods)
    )

    forecast_df = pd.DataFrame({

        "Date": future_dates,

        "Forecast": future_pred

    })

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=data[date_col],

            y=data[target_col],

            mode="lines",

            name="Actual"

        )

    )

    fig.add_trace(

        go.Scatter(

            x=forecast_df["Date"],

            y=forecast_df["Forecast"],

            mode="lines",

            name="Forecast"

        )

    )

    fig.update_layout(

        title="Sales Forecast",

        xaxis_title="Date",

        yaxis_title=target_col,

        template="plotly_white"

    )

    return fig.to_html(full_html=False), forecast_df