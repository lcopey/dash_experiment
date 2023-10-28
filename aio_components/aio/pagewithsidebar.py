import dash_bootstrap_components as dbc
from dash import Input, Output, State, clientside_callback, dcc, html

from .ids import BaseAIOId, auto


class PageIds(BaseAIOId):
    side_bar = auto()
    main_page = auto()
    close_button = auto()
    is_open = auto()


class PageWithSideBar(html.Div):
    def __init__(
        self, side_bar_children, main_page_children, aio_id: str, side_bar_width: str
    ):
        self.ids = PageIds(aio_id)
        close_button = dbc.Button(
            children="\u2630",
            id=self.ids.close_button,
            style={"position": "absolute", "top": "0", "right": "0"},
        )
        side_bar = html.Div(
            id=self.ids.side_bar,
            className="box side-bar",
            style={"width": side_bar_width},
            children=[
                close_button,
                html.Div(side_bar_children, className="side-bar-content"),
            ],
        )
        main_page = html.Div(
            id=self.ids.main_page,
            className="box main-page",
            style={
                "width": f"calc(100% - 4rem - {side_bar_width})",
            },
            children=main_page_children,
        )
        is_open = dcc.Store(id=self.ids.is_open, data=False)
        super().__init__([is_open, side_bar, main_page])

        clientside_callback(
            f"""function(is_open, side_bar_style, main_page_style) {{
                const side_bar_width = is_open ? '2rem' : '{side_bar_width}';
                const main_page_width = `calc(100% - 4rem - ${{side_bar_width}})`;
                const output = [
                {{ ...side_bar_style, width: side_bar_width }}, 
                is_open ? 'box side-bar-closed' : 'box side-bar',
                {{ ...main_page_style, width: main_page_width }}
                ];
                return output;
            }}""",
            Output(self.ids.side_bar, "style"),
            Output(self.ids.side_bar, "className"),
            Output(self.ids.main_page, "style"),
            Input(self.ids.is_open, "data"),
            State(self.ids.side_bar, "style"),
            State(self.ids.main_page, "style"),
        )

        clientside_callback(
            f"""function(n_clicks, is_open) {{
                            if (n_clicks) {{
                                return !is_open;
                            }}
                            return window.dash_clientside.no_update
                        }}""",
            Output(self.ids.is_open, "data"),
            Input(self.ids.close_button, "n_clicks"),
            State(self.ids.is_open, "data"),
        )
