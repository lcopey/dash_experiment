from dash import Input, Output, clientside_callback, dcc, html

from .ids import BaseAIOId, auto


class BadgeIds(BaseAIOId):
    display = auto()
    store = auto()


class BadgeDisplay(html.Div):
    def __init__(self, aio_id: str, child_class=html.Div, **child_kwargs):
        self.ids = BadgeIds(aio_id)

        display = html.Div(id=self.ids.display)
        store = dcc.Store(id=self.ids.store, data=[])
        super().__init__([display, store])

        clientside_callback(
            f"""
            function(items) {{
                if (items) {{
                    const children = items.map(
                        (item) => {{
                            const child = {child_class(children='', **child_kwargs).to_plotly_json()};
                            child.props.children = item;
                            return child;
                        }}
                    );
                    return children;
                }} else {{
                    return window.dash_clientside.no_update;
                }}
            }}
            """,
            Output(self.ids.display, "children"),
            Input(self.ids.store, "data"),
        )
