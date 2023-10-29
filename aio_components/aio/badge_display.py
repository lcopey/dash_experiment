from dash import ALL, Input, Output, State, clientside_callback, dcc, html

from .ids import BaseAIOId, auto


class BadgeIds(BaseAIOId):
    display = auto()
    store = auto()
    child = auto()


class BadgeDisplay(html.Div):
    def __init__(self, aio_id: str, child_class=html.Div, removable: bool = True, **child_kwargs):
        self.ids = BadgeIds(aio_id)

        display = html.Div(id=self.ids.display)
        store = dcc.Store(id=self.ids.store, data=[])
        super().__init__([display, store])

        clientside_callback(
            f"""
            function(items) {{
                if (items) {{
                    const children = items.map(
                        (item, index) => {{
                            const child = {child_class(children='', **child_kwargs).to_plotly_json()};
                            child.props.id = {{ type: '{self.ids.child}', index: index }};
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

        if removable:
            clientside_callback(
                """
                function(n_click, childs, data) {
                    if ( n_click.some(t => t) ) {
                        const triggered = dash_clientside.callback_context.triggered.map(
                        t => JSON.parse(
                                t['prop_id'].split('.')[0]
                            )['index']
                        )[0]; 
                        return data.filter(t => t !== childs[triggered]);
                    } else {
                        return window.dash_clientside.no_update
                    }
                }
                """,
                Output(self.ids.store, "data", allow_duplicate=True),
                Input({"type": self.ids.child, "index": ALL}, "n_clicks"),
                State({"type": self.ids.child, "index": ALL}, "children"),
                State(self.ids.store, "data"),
                prevent_initial_call=True,
            )
