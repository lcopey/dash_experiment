import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, clientside_callback, dcc, html

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

badge_store = dcc.Store(id="badge_store", data=[])
badge_display = html.Div(
    id="badge_display",
    # children=html.Div(['Test', html.Button('x')], className='custom-badge')
)
dummy_output = html.Div(id="dummy")
input_component = dcc.Input(id="input")
add_button = dbc.Button(id="validate", children="Add")
test_div = html.Div(id="test")

app.layout = html.Div(
    [input_component, add_button, badge_store, badge_display, dummy_output, test_div]
)

clientside_callback(
    """
    function(n_clicks, value, current) {
        if (n_clicks) {
            const new_div = `<div class='custom-badge'>${value}<button>x</button></div>`;
            if (current) {
                return [...current, new_div];
            } else {
                return [new_div];
            }
        } else {
            return window.dash_clientside.no_update;
        }
    }
    """,
    Output("badge_store", "data"),
    Input("validate", "n_clicks"),
    State("input", "value"),
    State("badge_store", "data"),
)

clientside_callback(
    """
    function(data) {
        let inner_html = data.join('');
        let badge_display = document.getElementById('badge_display');
        badge_display.innerHTML = inner_html;
        return window.dash_clientside.no_update
    }""",
    Output("dummy", "children"),
    Input("badge_store", "data"),
)

clientside_callback(
    """
    function(data) {
        console.log(data);
        return data;
    }
    """,
    Output("test", "children"),
    Input("badge_display", "children"),
)

if __name__ == "__main__":
    app.run(debug=True)
