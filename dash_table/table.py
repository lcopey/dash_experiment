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

DEFAULT_COLUMNS_OPTIONS = {'renamable': True, 'type': 'numeric', 'deletable': True}
INDEX_COLUMNS_OPTIONS = {'type': 'text'}
NEW_COLUMNS_OPTIONS = {'name': '* Create new col *',
                       'id': 'new_col_id',
                       'renamable': True,
                       'type': 'numeric'}
INDEX_STYLE = {'textAlign': 'left', 'fontWeight': 'bold'}


def _get_id(subcomponent_id, aio_id):
    return {
        'component': 'CustomDataTable',
        'subcomponent': subcomponent_id,
        'aio_id': aio_id
    }


def _init_datatable_values(dataframe: pd.DataFrame, index_col: List[str]):
    """Initialize main Dash.DataTable parameters

    :param dataframe: Dataframe containing the values to generate the table from. The index are not
    significant. However the columns are.
    :param index_col:
    :return: List[Dict], List[Dict], int
    """
    # generate mapping between columns name and unique id
    columns = [{"name": col, "id": str(uuid4()), **DEFAULT_COLUMNS_OPTIONS} if col not in index_col
               else {"name": col, "id": col, **INDEX_COLUMNS_OPTIONS}
               for col in dataframe.columns]
    columns_count = len(columns) - 1

    datas = dataframe.copy()
    datas['id'] = np.arange(datas.shape[0])
    datas = datas. \
        rename(columns={value['name']: value['id'] for value in columns}). \
        to_dict('records')

    # append the last column
    if all([col != NEW_COLUMNS_OPTIONS['id'] for col in columns]):
        columns += [NEW_COLUMNS_OPTIONS]
    for item in datas:
        item[NEW_COLUMNS_OPTIONS['id']] = ''

    return datas, columns, columns_count


def _as_dataframe(records: List[Dict]) -> pd.DataFrame:
    """Transform records into dataframe. Also takes care of None and nan values.

    :param records: Expects a List of dictionary with at least 'id' as key.
    :return: DataFrame with id column as index
    """
    return pd.DataFrame(records). \
        replace([None], np.nan). \
        replace(np.nan, ''). \
        set_index('id')


def _to_records(dataframe: pd.DataFrame) -> List[Dict]:
    """Transform dataframe into records. Replace empty strings by Nan values

    :param dataframe: Expects a dataframe with 'id' as index.
    :return: List of dictionaries
    """
    return dataframe. \
        replace('', np.nan). \
        reset_index(). \
        to_dict('records')


def _get_visible_records(dataframe: pd.DataFrame, is_hidden: bool, columns: List[Dict]) -> \
        List[Dict]:
    """

    :param dataframe: Expects empty strings when
    :param is_hidden: When True, return only
    :param columns: List of dictionaries. Expects 'type' as key holding either 'text' or
    'numeric' values.
    :return:
    """
    if not is_hidden:
        return _to_records(dataframe)
    else:
        # get rows that are not empty (-1 because of label in first column)
        len_index_col = sum([col['type'] == 'text' for col in columns])
        mask = (dataframe != '').sum(axis=1) - len_index_col != 0
        return _to_records(dataframe[mask])


def _has_last_column_values_changed(data: pd.DataFrame, data_previous: pd.DataFrame) -> bool:
    change = data != data_previous
    changed_column = data.columns[change.any(axis=0)]
    return NEW_COLUMNS_OPTIONS['id'] in changed_column


def _is_last_column_renamed(columns: List[Dict]) -> bool:
    return columns[-1]['name'] != NEW_COLUMNS_OPTIONS['name']


def _sync_change_with_data_reference(datas: pd.DataFrame, datas_reference: pd.DataFrame) -> \
        Tuple[pd.DataFrame, pd.DataFrame]:
    """Synchronize data_reference with datas. Reindex datas_reference columns with datas columns in
    case columns deletion. Update datas_reference values with datas values on common position."""
    datas_reference = datas_reference.reindex(columns=datas.columns)
    datas_reference.loc[datas.index, datas.columns] = datas
    return datas, datas_reference


def _get_records(datas_reference: pd.DataFrame, is_hidden: bool, columns: List[Dict]) -> \
        Tuple[List[Dict], List[Dict]]:
    """Returns datas_reference as records and datas as visible records."""
    data = _get_visible_records(datas_reference, is_hidden, columns)
    datas_reference = _to_records(datas_reference)
    return data, datas_reference


def _append_in_last_column(data_reference: pd.DataFrame, columns_count: int,
                           columns: List[Dict]):
    columns_count += 1
    new_column_name = f'Col {columns_count}'
    new_id = str(uuid4())
    columns += [{'id': new_id, 'name': new_column_name, **DEFAULT_COLUMNS_OPTIONS}]
    # swap list index in order to always have the last column available
    columns[-1], columns[-2] = columns[-2], columns[-1]
    data_reference[new_id] = data_reference[NEW_COLUMNS_OPTIONS['id']]
    data_reference[NEW_COLUMNS_OPTIONS['id']] = ''
    return columns_count, columns, data_reference


def _handle_last_column_naming(data_reference, columns):
    new_id = str(uuid4())
    columns[-1]['id'] = new_id
    columns.append(NEW_COLUMNS_OPTIONS)
    data_reference[new_id] = ''
    return data_reference, columns


def get_table_from_dataframe(app: 'Dash', dataframe, index_col: List[str], id, table_kwargs):
    """

    :param app:
    :param dataframe:
    :param index_col:
    :param id:
    :param table_kwargs:
    :return:
    """

    datas, columns, columns_count = _init_datatable_values(dataframe, index_col)

    style_header_conditional = [{'if': {'column_id': NEW_COLUMNS_OPTIONS['id']},
                                 'fontStyle': 'italic', 'color': 'rgb(128, 128, 128)',
                                 'backgroundColor': 'rgba(200, 200, 200, 0.1'}]
    style_header_conditional += [{'if': {'column_id': col}, **INDEX_STYLE} for col in index_col]

    style_data_conditional = [{'if': {'column_id': NEW_COLUMNS_OPTIONS['id']},
                               'fontStyle': 'italic', 'width': 'auto',
                               'color': 'rgb(128, 128, 128)',
                               'backgroundColor': 'rgba(200, 200, 200, 0.1'}]
    style_data_conditional += [{'if': {'column_id': col}, **INDEX_STYLE} for col in index_col]

    tooltip = {item['id']: {'value': item['name'], 'use_with': 'header'} for item in columns}
    table = DataTable(data=datas, columns=columns,
                      tooltip=tooltip,
                      id=_get_id('table', id),
                      row_selectable=False,
                      row_deletable=False,
                      fixed_columns={'headers': True, 'data': len(index_col)},
                      style_as_list_view=True,
                      style_table={'overflowX': 'auto', 'minWidth': '100%'},
                      style_data={'width': '5em', },
                      style_header={'width': '5em'},
                      style_header_conditional=style_header_conditional,
                      style_data_conditional=style_data_conditional,
                      **table_kwargs)
    table = dbc.Col(table, className='table-container')

    sidebar = [
        dbc.Button(id=_get_id('open-button', id), children='\u2630', className='side-bar-item'),
        dbc.Checkbox(id=_get_id('hide-rows-checkbox', id), value=False, label='Hide',
                     className='side-bar-item')]
    sidebar = html.Div(sidebar, className='side-bar', id=_get_id('side-bar', id))

    stores = [dcc.Store(id=_get_id('side-bar-status-store', id), data=False),
              dcc.Store(id=_get_id('columns-mapping-store', id), data=columns),
              dcc.Store(id=_get_id('columns-count-store', id), data=columns_count),
              dcc.Store(id=_get_id('table-data-store', id), data=datas)]

    layout = html.Div([table, sidebar, *stores], className='customdatatable-container')

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
                data, data_reference = _get_records(data_reference, is_hidden, columns)

            else:
                data, data_reference = _get_records(data_reference, is_hidden, columns)
                columns_count, columns = dash.no_update, dash.no_update

            # keep the table, and data store synchronized
            return data, columns_count, columns, data_reference

        # On change of the columns
        elif context == (_get_id('table', id), 'columns'):
            # if the change was in the last column, change its id and append it
            data = _as_dataframe(data)
            data_reference = _as_dataframe(data_reference)
            data, data_reference = _sync_change_with_data_reference(data, data_reference)

            if _is_last_column_renamed(columns):
                data_reference, columns = _handle_last_column_naming(data_reference, columns)
                data, data_reference = _get_records(data_reference, is_hidden, columns)
                return data, dash.no_update, columns, data_reference

            return dash.no_update, dash.no_update, dash.no_update, _to_records(data_reference)

        elif context == (_get_id('hide-rows-checkbox', id), 'value'):
            data_reference = _as_dataframe(data_reference)
            data, data_reference = _get_records(data_reference, is_hidden, columns)
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
