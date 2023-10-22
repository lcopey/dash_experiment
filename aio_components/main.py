import dash_bootstrap_components as dbc
from aio import BaseModalAIO, Callback
from dash import Dash, Input, Output, State, callback, html

if __name__ == "__main__":
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    # open_modal = dbc.Button("Click")
    # apply = dbc.Button("Apply")
    # app.layout = html.Div(
    #     [
    #         open_modal,
    #         BaseModalAIO(
    #             "modal", trigger=open_modal, header="Modal", close_button=apply
    #         ),
    #     ]
    # )
    button = dbc.Button("Click")
    label = html.Label()

    app.layout = html.Div([button, label])

    @Callback(
        Output(label, "children"),
        Input(button, "n_clicks"),
        debug=True,
        store=True,
        store_path="./storage",
    )
    def on_click(n_clicks):
        return n_clicks

    app.run()
