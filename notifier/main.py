import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback, dcc, html

button = dbc.Button("Click")
notification = html.Div()

button2 = dbc.Button("Click")
notification2 = html.Div()

layout = dmc.NotificationsProvider(
    [
        # children
        html.Div([notification, button]),
        html.Div([notification2, button2]),
    ]
)


@callback(Output(notification, "children"), Input(button, "n_clicks"))
def notify(n_clicks: int):
    if n_clicks:
        return dmc.Notification(
            id=f"1_{n_clicks}",
            title="Click",
            action="show",
            message="You clicked !",
        )


@callback(Output(notification2, "children"), Input(button2, "n_clicks"))
def notify(n_clicks: int):
    if n_clicks:
        return dmc.Notification(
            id=f"2_{n_clicks}",
            title="Click",
            action="show",
            message="You clicked 2!",
        )


if __name__ == "__main__":
    app = Dash(__name__)
    app.layout = layout
    app.run(debug=True)
