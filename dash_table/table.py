"""
Generate table
"""
from uuid import uuid4

import dash
import pandas as pd
import numpy as np
from dash import html
from dash import dcc
from dash.dash_table import DataTable
import dash_bootstrap_components as dbc
from dash import Input, Output, State, ClientsideFunction, callback, clientside_callback
from dash.exceptions import PreventUpdate
from utils import get_context
from typing import TYPE_CHECKING, List, Dict, Tuple

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
    if all([col != NEW_COLUMN['id'] for col in columns]):
        validated_columns = columns + [NEW_COLUMN]

    validated_datas = datas.copy()
    for item in datas:
        item[NEW_COLUMN['id']] = ''

    return validated_datas, validated_columns


def _as_dataframe(records: List[Dict]) -> pd.DataFrame:
    return pd.DataFrame(records). \
        replace([None], np.nan). \
        replace(np.nan, ''). \
        set_index('id')


def _to_records(dataframe: pd.DataFrame) -> List[Dict]:
    return dataframe. \
        replace('', np.nan). \
        reset_index(). \
        to_dict('records')


def _get_visible_records(dataframe: pd.DataFrame, is_hidden: bool) -> List[Dict]:
    if not is_hidden:
        return _to_records(dataframe)
    else:
        # get rows that are not empty (-1 because of label in first column)
        mask = (dataframe != '').sum(axis=1) - 1 != 0
        return _to_records(dataframe[mask])


def _has_last_column_values_changed(data: pd.DataFrame, data_previous: pd.DataFrame) -> bool:
    change = data != data_previous
    changed_column = data.columns[change.any(axis=0)]
    return NEW_COLUMN['id'] in changed_column


def _is_last_column_renamed(columns: List[Dict]) -> bool:
    return columns[-1]['name'] != NEW_COLUMN['name']


def _sync_change_with_data_reference(data: pd.DataFrame, datastore: pd.DataFrame) -> Tuple[
    pd.DataFrame, pd.DataFrame]:
    datastore = datastore.reindex(columns=data.columns)
    datastore.loc[data.index, data.columns] = data
    return data, datastore


def _get_records(data_reference: pd.DataFrame, is_hidden: bool):
    data = _get_visible_records(data_reference, is_hidden)
    data_reference = _to_records(data_reference)
    return data, data_reference


def _append_in_last_column(data_reference: pd.DataFrame, columns_count: int,
                           columns: List[Dict]):
    columns_count += 1
    new_column_name = f'Col {columns_count}'
    new_id = str(uuid4())
    columns += [{'id': new_id, 'name': new_column_name, **DEFAULT_COLUMNS_OPTIONS}]
    # swap list index in order to always have the last column available
    columns[-1], columns[-2] = columns[-2], columns[-1]
    data_reference[new_id] = data_reference[NEW_COLUMN['id']]
    data_reference[NEW_COLUMN['id']] = ''
    return columns_count, columns, data_reference


def _handle_last_column_naming(data_reference, columns):
    new_id = str(uuid4())
    columns[-1]['id'] = new_id
    columns += [NEW_COLUMN]
    data_reference[new_id] = ''
    return data_reference, columns


DEFAULT_COLUMNS_OPTIONS = {'renamable': True, 'type': 'numeric', 'deletable': True}
INDEX_COLUMNS = {'type': 'text'}
NEW_COLUMN = {'name': '* Create new col *', 'id': 'new_col_id', 'renamable': True}


def get_table_from_dataframe(app: 'Dash', dataframe, index_col: List[str], id, table_kwargs):
    """

    :param app:
    :param dataframe:
    :param index_col:
    :param id:
    :param table_kwargs:
    :return:
    """
    columns = [
        {"name": col, "id": str(uuid4()), **DEFAULT_COLUMNS_OPTIONS} if col not in index_col else
        {"name": col, "id": col, **INDEX_COLUMNS}
        for col in dataframe.columns]
    columns_count = len(columns) - 1

    datas = dataframe.copy()
    datas['id'] = np.arange(datas.shape[0])
    datas = datas. \
        rename(columns={value['name']: value['id'] for value in columns}). \
        to_dict('records')

    datas, columns = _validate(datas, columns)
    table = DataTable(data=datas, columns=columns,
                      tooltip={item['id']: {'value': item['name'], 'use_with': 'header'}
                               for item in columns},
                      id=_get_id('table', id),
                      row_selectable=False,
                      row_deletable=False,
                      fixed_columns={'headers': True, 'data': len(index_col)},
                      style_as_list_view=True,
                      style_table={'overflowX': 'auto', 'minWidth': '100%'},
                      style_data={'width': '5em', },
                      style_header_conditional=[
                          {'if': {'column_id': NEW_COLUMN['id']},
                           'fontStyle': 'italic', 'color': 'rgb(128, 128, 128)',
                           'backgroundColor': 'rgba(200, 200, 200, 0.1'}],
                      style_data_conditional=[{'if': {'column_id': NEW_COLUMN['id']},
                                               'fontStyle': 'italic', 'width': 'auto',
                                               'color': 'rgb(128, 128, 128)',
                                               'backgroundColor': 'rgba(200, 200, 200, 0.1'}],
                      **table_kwargs)
    table = dbc.Col(table, className='table-container')

    sidebar = [dbc.Button(id=_get_id('open-button', id), children='\u2630', className='button'),
               dbc.Checkbox(id=_get_id('hide-rows-checkbox', id), label='Hide', value=False,
                            className='button')]
    sidebar = html.Div(sidebar, className='side-bar', id=_get_id('side-bar', id))

    stores = [dcc.Store(id=_get_id('side-bar-status-store', id), data=False),
              dcc.Store(id=_get_id('columns-mapping-store', id), data=columns),
              dcc.Store(id=_get_id('columns-count-store', id), data=columns_count),
              dcc.Store(id=_get_id('table-data-store', id), data=datas)]

    layout = html.Div([
        table, sidebar, *stores
    ], className='customdatatable-container')

    @app.callback(Output(_get_id('table', id), 'data'),
                  Output(_get_id('columns-count-store', id), 'data'),
                  Output(_get_id('table', id), 'columns'),
                  Output(_get_id('table-data-store', id), 'data'),
                  Input(_get_id('table', id), 'data'),
                  Input(_get_id('table', id), 'columns'),
                  Input(_get_id('hide-rows-checkbox', id), 'value'),
                  State(_get_id('table', id), 'data_previous'),
                  State(_get_id('table-data-store', id), 'data'),
                  State(_get_id('columns-count-store', id), 'data'))
    def on_data_change(data, columns, is_hidden, data_previous, data_reference, columns_count):

        # On change of the data of the table
        context = get_context()
        if context == (_get_id('table', id), 'data') and data_previous is not None:
            data = _as_dataframe(data)
            data_previous = _as_dataframe(data_previous)
            data_reference = _as_dataframe(data_reference)
            data, data_reference = _sync_change_with_data_reference(data, data_reference)

            # If change was in the last column, append a new column and keep the new column at the
            # end of the table
            if _has_last_column_values_changed(data, data_previous):
                columns_count, columns, data_reference = \
                    _append_in_last_column(data_reference, columns_count, columns)

            else:
                columns_count, columns = dash.no_update, dash.no_update

            # keep the table, and data store synchronized
            data, data_reference = _get_records(data_reference, is_hidden)
            return data, columns_count, columns, data_reference

        # On change of the columns
        elif context == (_get_id('table', id), 'columns'):
            # if the change was in the last column, change its id and append it
            data = _as_dataframe(data)
            data_reference = _as_dataframe(data_reference)
            data, data_reference = _sync_change_with_data_reference(data, data_reference)

            if _is_last_column_renamed(columns):
                data_reference, columns = _handle_last_column_naming(data_reference, columns)
                data, data_reference = _get_records(data_reference, is_hidden)
                return data, dash.no_update, columns, data_reference

            return dash.no_update, dash.no_update, dash.no_update, _to_records(data_reference)

        elif context == (_get_id('hide-rows-checkbox', id), 'value'):
            data_reference = _as_dataframe(data_reference)
            data, data_reference = _get_records(data_reference, is_hidden)
            return data, dash.no_update, dash.no_update, dash.no_update

        else:
            raise PreventUpdate

    app.clientside_callback(ClientsideFunction('clientside', 'open_sidebar'),
                            Output(_get_id('side-bar', id), 'className'),
                            Output(_get_id('side-bar-status-store', id), 'data'),
                            Output(_get_id('open-button', id), 'children'),
                            Input(_get_id('open-button', id), 'n_clicks'),
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
