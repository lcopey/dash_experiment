import dash_bootstrap_components as dbc
from aio.badge_display import BadgeDisplay
from dash import (ALL, MATCH, Dash, Input, Output, State, clientside_callback,
                  dcc, html)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

badge_display = BadgeDisplay(aio_id="display", className="pills")
input_component = dcc.Input(id="input")
add_button = dbc.Button(id="validate", children="Add")

test_display = html.Div(id="test_display")

app.layout = html.Div([input_component, add_button, badge_display, test_display])

clientside_callback(
    """
    function(n_clicks, n_submit, value, current) {
        if (n_clicks || n_submit) {
            if (current) {
                return [...current, value];
            } else {
                return [value];
            }
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output(badge_display.ids.store, "data"),
    Input("validate", "n_clicks"),
    Input("input", "n_submit"),
    State("input", "value"),
    State(badge_display.ids.store, "data"),
)

# clientside_callback(
#     """function(children) {
#         return children;
#     }
#     """,
#     Output("test_display", "children"),
#     Input(badge_display.ids.display, "children"),
# )


if __name__ == "__main__":
    app.run(debug=True)
