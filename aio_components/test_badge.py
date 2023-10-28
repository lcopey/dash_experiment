import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, clientside_callback, dcc, html

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

badge_store = dcc.Store(id="badge_store", data=[])
badge_display = html.Div(id="badge_display")
input_component = dcc.Input(id="input")
add_button = dbc.Button(id="validate", children="Add")

test_display = html.Div(id="test_display")

app.layout = html.Div(
    [input_component, add_button, badge_store, badge_display, test_display]
)

clientside_callback(
    """
    function(n_clicks, value, current) {
        if (n_clicks) {
            if (current) {
                return [...current, value];
            } else {
                return [value];
            }
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("badge_store", "data"),
    Input("validate", "n_clicks"),
    State("input", "value"),
    State("badge_store", "data"),
)

clientside_callback(
    f"""
    function(items) {{
        if (items) {{
            const children = items.map(
                (item) => {{
                    const child = {html.Div(children='', className='custom-badge').to_plotly_json()};
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
    Output("badge_display", "children"),
    Input("badge_store", "data"),
)

clientside_callback(
    """function(children) {
        return children;
    }
    """,
    Output("test_display", "children"),
    Input("badge_display", "children"),
)

if __name__ == "__main__":
    app.run(debug=True)
