from dash import dcc, html, register_page
from utils import require_login

register_page(__name__, path="/")
require_login(__name__)

layout = html.Div(
    [
        html.Label("Welcome")
        # dcc.Link("Go to Page 1", href="/page-1"),
        # html.Br(),
        # dcc.Link("Go to Page 2", href="/page-2"),
    ]
)
