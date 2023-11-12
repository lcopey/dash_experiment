import dash
from dash import dcc, html
from flask_login import current_user, logout_user

dash.register_page(__name__)


def layout():
    if current_user.is_authenticated:
        logout_user()
    return html.Div(
        [
            html.Div(
                html.H2("You have been logged out - You will be redirected to login")
            ),
            dcc.Interval(
                id={"index": "redirectLogin", "type": "redirect"},
                n_intervals=0,
                interval=1 * 3000,
            ),
        ]
    )
