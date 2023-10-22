from aio import Callback, DashProxy, Notifier
from dash import Dash, Input, Output, State, html
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import LogTransform

app = DashProxy(__name__, activate_logging=True)
app.layout = html.Div(
    [html.Button("Run", id="btn"), html.Div(id="txt"), html.Div(id="txt2")]
)


@Callback(
    Output("txt", "children"),
    Output("txt2", "children"),
    Input("btn", "n_clicks"),
    notify=True,
)
def do_stuff(n_clicks, notifier: Notifier):
    if not n_clicks:
        raise PreventUpdate()
    notifier.info("Message")
    notifier.info("Message2")
    return f"Run number {n_clicks} completed", "Test"


if __name__ == "__main__":
    app.run_server(debug=False)
