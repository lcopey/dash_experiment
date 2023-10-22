import time

from dash import Dash, Input, Output, State, callback, dcc, html

upload = dcc.Upload(
    children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
    style={
        "width": "100%",
        "height": "60px",
        "lineHeight": "60px",
        "borderWidth": "1px",
        "borderStyle": "dashed",
        "borderRadius": "5px",
        "textAlign": "center",
        "margin": "10px",
    },
    # Allow multiple files to be uploaded
    multiple=True,
)
on_upload_div = html.Div()

loading = dcc.Loading(id="loading", children=on_upload_div)


@callback(Output(on_upload_div, "children"), Input(upload, "filename"))
def input_triggers_nested(value):
    return value


if __name__ == "__main__":
    app = Dash(__name__)
    app.layout = html.Div([upload, loading])
    app.run(debug=True)
