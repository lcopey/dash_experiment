import json
from dash import callback_context as ctx
from dash.exceptions import PreventUpdate


def get_context():
    if not ctx.triggered:
        raise PreventUpdate
    else:
        context, prop = ctx.triggered[0]['prop_id'].split('.')
        try:
            return json.loads(context), prop
        except:
            return context, prop
