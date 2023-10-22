from dash import Dash, html
import dash_bootstrap_components as dbc
from aio import BaseModalAIO

if __name__ == '__main__':
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    open_modal = dbc.Button('Click')
    apply = dbc.Button('Apply')
    app.layout = html.Div([open_modal, BaseModalAIO('modal', trigger=open_modal, header='Modal', close_button=apply)])
    app.run()
