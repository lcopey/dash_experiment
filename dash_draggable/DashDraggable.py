# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashDraggable(Component):
    """A DashDraggable component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- columnOrder (list; optional)

- columns (dict; optional)

- handleText (string; default '')

- items (dict; optional)

- showHandle (boolean; default True)"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, items=Component.UNDEFINED, columns=Component.UNDEFINED, columnOrder=Component.UNDEFINED, showHandle=Component.UNDEFINED, handleText=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'columnOrder', 'columns', 'handleText', 'items', 'showHandle']
        self._type = 'DashDraggable'
        self._namespace = 'dash_draggable'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'columnOrder', 'columns', 'handleText', 'items', 'showHandle']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashDraggable, self).__init__(**args)
