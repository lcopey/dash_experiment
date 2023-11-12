import dash
from dash import dcc, html

dash.register_page(__name__, path="/")


layout = html.Div(
    [
        dcc.Link("Go to Page 1", href="/page-1"),
        html.Br(),
        dcc.Link("Go to Page 2", href="/page-2"),
    ]
)
