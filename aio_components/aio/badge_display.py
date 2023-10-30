from dash import ALL, Input, Output, State, clientside_callback, dcc, html
from dash_iconify import DashIconify
from .ids import BaseAIOId, auto


class BadgeIds(BaseAIOId):
    display = auto()
    store = auto()
    child = auto()


def _walk(json_component):
    if "props" in json_component and "children" in json_component["props"]:
        childs = json_component["props"]["children"]
        # if isinstance(childs, Sequence) and not isinstance(childs, str):
        if isinstance(childs, list):
            childs = [_to_json(child) for child in childs]
            json_component["props"]["children"] = childs

        else:
            json_component["props"]["children"] = _to_json(childs)

    return json_component


def _to_json(component):
    if hasattr(component, 'to_plotly_json'):
        return _walk(component.to_plotly_json())
    return component


class BadgeDisplay(html.Div):
    def __init__(
            self, aio_id: str,
            child_class=html.Div,
            className: str = 'pills',
            removable: bool = True,
            **child_kwargs
    ):
        self.ids = BadgeIds(aio_id)

        display = html.Div(id=self.ids.display)
        store = dcc.Store(id=self.ids.store, data=[])
        super().__init__([display, store])

        parent_kwargs = {}
        if className:
            parent_kwargs['className'] = className
        inner_components = [child_class(children='', **child_kwargs)]
        if removable:
            inner_components.append(
                html.Button(
                    DashIconify(icon='carbon:close-filled')
                )
            )
        child_template = _to_json(html.Div(children=inner_components, **parent_kwargs))

        clientside_callback(
            f"""
            function(items) {{
                if (items) {{
                    const children = items.map(
                        (item, index) => {{
                            const child = {child_template};
                            child.props.children[0].props.id = {{ type: '{self.ids.child}',
                                subtype: 'badge', 
                                index: index 
                                }};
                            child.props.children[0].props.children = item;
                            if ('{removable}' == 'True') {{
                                child.props.children[1].props.id = {{ type: '{self.ids.child}', 
                                    subtype: 'close', 
                                    index: index 
                                }};
                            }}
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
                Input({"type": self.ids.child, 'subtype': 'close', "index": ALL}, "n_clicks"),
                State({"type": self.ids.child, 'subtype': 'badge', "index": ALL}, "children"),
                State(self.ids.store, "data"),
                prevent_initial_call=True,
            )
