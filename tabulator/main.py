import dash_tabulator
from dash import Dash, html

# columns = [
#     {"title": "Name", "field": "name", "width": 150, "headerFilter": True, "editor": "input"},
#     {"title": "Age", "field": "age", "hozAlign": "left", "formatter": "progress"},
#     {"title": "Favourite Color", "field": "col", "headerFilter": True},
#     {"title": "Date Of Birth", "field": "dob", "hozAlign": "center"},
#     {"title": "Rating", "field": "rating", "hozAlign": "center", "formatter": "star"},
#     {"title": "Passed?", "field": "passed", "hozAlign": "center", "formatter": "tickCross"}
# ]
#
# # Setup some data
# data = [
#     {"id": 1, "name": "Oli Bob", "age": "12", "col": "red", "dob": ""},
#     {"id": 2, "name": "Mary May", "age": "1", "col": "blue", "dob": "14/05/1982"},
#     {"id": 3, "name": "Christine Lobowski", "age": "42", "col": "green", "dob": "22/05/1982"},
#     {"id": 4, "name": "Brendon Philips", "age": "125", "col": "orange", "dob": "01/08/1980"},
#     {"id": 5, "name": "Margret Marmajuke", "age": "16", "col": "yellow", "dob": "31/01/1999"},
#     {"id": 6, "name": "Fred Savage", "age": "16", "col": "yellow", "rating": "1", "dob": "31/01/1999"},
#     {"id": 6, "name": "Brie Larson", "age": "30", "col": "blue", "rating": "1", "dob": "31/01/1999"},
# ]
columns = [
    {
        "title": f"Col {n + 1}",
        "field": f"col_{n + 1}",
        "editor": "range",
        "editorParams": {"min": 0, "max": 100, "step": 1},
    }
    for n in range(10)
]
columns.insert(0, {"field": "col_0", "rowHandle": True})

base_input = {f"col_{n + 1}": "" for n in range(10)}
data = [{"id": i, **base_input} for i in range(10)]

# options = {"groupBy": "col", "selectable": 1}

layout = html.Div(
    [
        dash_tabulator.DashTabulator(
            id="tabulator",
            columns=columns,
            data=data,
            # options=options,
            # downloadButtonType=downloadButtonType,
        )
    ]
)

app = Dash()
app.layout = layout

if __name__ == "__main__":
    app.run_server()
