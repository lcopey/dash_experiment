from functools import wraps

import dash_mantine_components as dmc
from dash import Dash, html


class DashProxy(Dash):
    @wraps(Dash.__init__)
    def __init__(self, *args, activate_logging: bool = False, **kwargs):
        self.activate_logging = activate_logging
        super().__init__(*args, **kwargs)

    @Dash.layout.setter
    def layout(self, value):
        if self.activate_logging:
            value = dmc.NotificationsProvider(
                children=[html.Div(id="notification-target"), value]
            )
        Dash.layout.fset(self, value)
