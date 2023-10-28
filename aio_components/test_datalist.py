from dash import Dash, dcc, html

app = Dash()

names = ("Foo", "Bar")
select = html.Select(
    [html.Option(value, value=value) for value in names], name="select"
)
datalist = html.Datalist(
    [html.Option(value, value=value) for value in names], id="datalist"
)
input_with_autocomplete = dcc.Input(list="datalist")

app.layout = html.Div([select, datalist, input_with_autocomplete])

if __name__ == "__main__":
    app.run(debug=True)
