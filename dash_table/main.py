import pandas as pd
from dash import Dash
from dash import html
import dash_bootstrap_components as dbc
from dash_extensions import Keyboard
from dash_extensions.enrich import DashProxy, MultiplexerTransform
from table import get_table_from_dataframe

default_rows = [f'Row {n + 1}' for n in range(10)]
default_columns = [f'Col {n + 1}' for n in range(3)]

# df = pd.read_csv('https://git.io/Juf1t')
df = pd.DataFrame(index=default_rows, columns=default_columns)
df.index.name = 'Rows'
df.reset_index(inplace=True)

# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app = DashProxy(__name__, transforms=[MultiplexerTransform()], external_stylesheets=[dbc.themes.BOOTSTRAP])

layout = html.Div(
    [Keyboard(id='keyboard'),
     # *[dcc.Dropdown(options=df[c].unique(), multi=True) for c in df.columns],
     get_table_from_dataframe(app, df, id='table', table_kwargs={'editable': True}),
     html.Label(id='txt')]
)

# app.clientside_callback(
#     ClientsideFunction(namespace='clientside',
#                        function_name='copy_function'),
#     Output('txt', 'children'),
#     Input('keyboard', 'keydown'),
#     State('table', 'selected_cells'),
#     State('table', 'datas')
# )

if __name__ == '__main__':
    app.layout = layout
    app.run_server(debug=True)
