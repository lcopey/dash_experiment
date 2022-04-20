# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class column(Component):
    """A column component.


Keyword arguments:

- column (dict; optional)

- handleText (string; default '')

- items (list; optional):
    The ID used to identify this component in Dash callbacks.

- showHandle (boolean; default True)"""
    @_explicitize_args
    def __init__(self, items=Component.UNDEFINED, column=Component.UNDEFINED, showHandle=Component.UNDEFINED, handleText=Component.UNDEFINED, **kwargs):
        self._prop_names = ['column', 'handleText', 'items', 'showHandle']
        self._type = 'column'
        self._namespace = 'dash_draggable'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['column', 'handleText', 'items', 'showHandle']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(column, self).__init__(**args)
