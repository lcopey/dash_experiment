# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class task(Component):
    """A task component.


    Keyword arguments:

    - index (number; optional)

    - item (dict; optional):
        The ID used to identify this component in Dash callbacks."""

    @_explicitize_args
    def __init__(self, item=Component.UNDEFINED, index=Component.UNDEFINED, **kwargs):
        self._prop_names = ["index", "item"]
        self._type = "task"
        self._namespace = "dash_draggable"
        self._valid_wildcard_attributes = []
        self.available_properties = ["index", "item"]
        self.available_wildcard_properties = []
        _explicit_args = kwargs.pop("_explicit_args")
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != "children"}
        for k in []:
            if k not in args:
                raise TypeError("Required argument `" + k + "` was not specified.")
        super(task, self).__init__(**args)
