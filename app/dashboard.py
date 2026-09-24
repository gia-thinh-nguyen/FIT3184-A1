import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

from app.carparks import carparks
from app.logs import count_requests_last_n_seconds

dash_app = dash.Dash(
    __name__,
    requests_pathname_prefix="/dashboard/",
)

dash_app.layout = html.Div([
    html.H1("Smart Parking — Operator Dashboard"),
    html.Div(id="active-users-stat"),
    dcc.Graph(id="availability-chart"),
    dcc.Interval(id="refresh-interval", interval=2000, n_intervals=0),
])


@dash_app.callback(
    Output("availability-chart", "figure"),
    Output("active-users-stat", "children"),
    Input("refresh-interval", "n_intervals"),
)
def update_dashboard(n):
    ids = [cp["carpark_id"] for cp in carparks.values()]
    available = [cp["available_spaces"] or 0 for cp in carparks.values()]

    figure = go.Figure(
        data=[go.Bar(x=ids, y=available)],
        layout=go.Layout(
            title="Available Spaces per Car Park",
            xaxis_title="Car Park",
            yaxis_title="Available Spaces",
            yaxis=dict(rangemode="tozero"),
            xaxis_tickangle=-90,
        ),
    )

    stat_text = f"Active users (last 30s): {count_requests_last_n_seconds(30)}"
    return figure, stat_text