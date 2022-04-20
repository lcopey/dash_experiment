"""
Generate table
"""
from uuid import uuid4
import pandas as pd
import numpy as np
from dash import html
from dash import dcc
from dash.dash_table import DataTable
import dash_bootstrap_components as dbc
from dash import Input, Output, State, ClientsideFunction, callback, clientside_callback
from dash.exceptions import PreventUpdate
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dash import Dash


def _get_id(subcomponent_id, aio_id):
    return {
        'component': 'CustomDataTable',
        'subcomponent': subcomponent_id,
        'aio_id': aio_id
    }


def _validate(datas, columns):
    validated_columns = columns
    if all([c != '*' for c in columns]):
        validated_columns = columns + [{'name': '*', 'id': '*', 'renamable': True}]

    validated_datas = datas
    if all([r[validated_columns[0]['id']] != '*' for r in datas]):
        validated_datas = datas + [{c['id']: '*' if n == 0 else '' for n, c in enumerate(validated_columns)}]

    return validated_datas, validated_columns


DEFAULT_COLUMNS_OPTIONS = {'renamable': True, 'type': 'numeric'}


def get_table_from_dataframe(app: 'Dash', dataframe, id, table_kwargs):
    columns = [{"name": col, "id": str(uuid4()), **DEFAULT_COLUMNS_OPTIONS} if n != 0 else
               {"name": col, "id": str(uuid4()), 'type': 'text'}
               for n, col in enumerate(dataframe.columns)]
    datas = dataframe. \
        rename(columns={value['name']: value['id'] for value in columns}). \
        to_dict('records')

    datas, columns = _validate(datas, columns)
    table = DataTable(data=datas, columns=columns,
                      tooltip_header={value['id']: value['name'] for value in columns},
                      id=_get_id('table', id),
                      row_selectable='multi', row_deletable=True,
                      style_data_conditional=[{'if': {'column_id': '*'}, 'fontStyle': 'italic'}],
                      **table_kwargs)
    table = dbc.Col(table, className='table-container')

    sidebar = [dbc.Button(id=_get_id('open', id), children='\u2630', className='button'),
               dcc.Store(id=_get_id('side-bar-status-store', id), data=False),
               dcc.Store(id=_get_id('columns-mapping-store', id), data=columns)]
    sidebar = html.Div(sidebar, className='side-bar', id=_get_id('side-bar', id))

    layout = html.Div([
        sidebar, table,
    ], className='customdatatable-container')

    @app.callback(Output(_get_id('table', id), 'data'),
                  Input(_get_id('table', id), 'data'),
                  State(_get_id('table', id), 'data_previous'))
    def on_data_change(data, data_previous):
        def as_dataframe(records):
            return pd.DataFrame(records).fillna('')

        if data_previous is not None:
            data = as_dataframe(data)
            data_previous = as_dataframe(data_previous)

            change = data != data_previous

            col_wo_index = [col for n, col in enumerate(data.columns) if n != 0]
            # records[col_wo_index] = records[col_wo_index]. \
            #     replace(np.nan, '')
            # records[col_wo_index] = records. \
            #     astype(str).\
            #     replace(',', '.', regex=True). \
            #     apply(pd.to_numeric, errors='coerce')

            return data.to_dict('records')
        else:
            raise PreventUpdate

    app.clientside_callback(ClientsideFunction('clientside', 'open_sidebar'),
                            Output(_get_id('side-bar', id), 'className'),
                            Output(_get_id('side-bar-status-store', id), 'data'),
                            Output(_get_id('open', id), 'children'),
                            Input(_get_id('open', id), 'n_clicks'),
                            State(_get_id('side-bar-status-store', id), 'data')
                            )
    app.clientside_callback(ClientsideFunction('clientside', 'synchronize_columns_mapping'),
                            Output(_get_id('columns-mapping-store', id), 'data'),
                            Input(_get_id('table', id), 'columns')
                            )
    app.clientside_callback(ClientsideFunction('clientside', 'synchronize_tooltip'),
                            Output(_get_id('table', id), 'tooltip'),
                            Input(_get_id('table', id), 'columns')
                            )

    return layout
