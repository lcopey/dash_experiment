from dash import html, clientside_callback, ClientsideFunction, Output, Input, State
import dash_bootstrap_components as dbc
from typing import Literal, Any
from .base import BaseAIOId


class BaseModalIds(BaseAIOId):
    window = 'window'


class BaseModalAIO(html.Div):
    def __init__(self, aio_id: str,
                 trigger: dbc.Button,
                 header: str,
                 close_button: dbc.Button,
                 body: Any = '',
                 is_open: bool = False,
                 size: Literal['sm', 'lg', 'xl'] = 'sm'):
        self.ids = BaseModalIds(aio_id)

        modal = dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle(header)),
                dbc.ModalBody(body),
                dbc.ModalFooter(close_button),
            ],
            id=self.ids.window,
            is_open=is_open,
            size=size
        )

        clientside_callback(
            ClientsideFunction(namespace='modal', function_name='open'),
            Output(self.ids.window, 'is_open'),
            Input(trigger, 'n_clicks'),
            State(self.ids.window, 'is_open')
        )

        super().__init__(modal)
