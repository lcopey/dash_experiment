from datetime import datetime
from functools import wraps
from logging import getLogger
from pathlib import Path
from typing import Any, Callable, Union

import dash_mantine_components as dmc
import yaml
from dash import Output, callback, no_update


class Notifier:
    def __init__(
        self,
    ):
        self.base_id = None
        self._output = []

    def set_base_id(self, base_id: str):
        self.base_id = base_id

    def info(self, message: str):
        notifier_id = f"{self.base_id}.{len(self._output)}"
        self._output.append(
            dmc.Notification(
                id=notifier_id,
                color="blue",
                title="Info",
                message=message,
                action="show",
            )
        )

    def warning(self, message: str):
        notifier_id = f"{self.base_id}.{len(self._output)}"
        self._output.append(
            dmc.Notification(
                id=notifier_id,
                color="yellow",
                title="Warning",
                message=message,
                action="show",
            )
        )

    def error(self, message: str):
        notifier_id = f"{self.base_id}.{len(self._output)}"
        self._output.append(
            dmc.Notification(
                id=notifier_id,
                color="red",
                title="Error",
                message=message,
                action="show",
            )
        )

    @property
    def output(self):
        return self._output

    def clear_output(self):
        self._output = []


class Callback:
    @wraps(callback)
    def __init__(
        self,
        *args,
        debug: bool = False,
        store: bool = False,
        store_path: Union[str, Path] = None,
        notify: bool = False,
        **kwargs,
    ):
        self.debug = debug
        if debug:
            self.logger = getLogger(__name__)

        self.store = store
        if store:
            assert (
                store_path is not None
            ), "store_path should not be None when store=True"
            self.store_path = store_path
            self.session_start = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.notify = notify
        self.notifier = Notifier() if notify else None
        if notify:
            args = (
                Output(
                    component_id="notification-target", component_property="children"
                ),
                *args,
            )

        self._args = args
        self._kwargs = kwargs
        self._n_call = 0
        self._multioutput = sum(isinstance(arg, Output) for arg in args) > 1

    def __call__(self, func: Callable):
        def inner(*args):
            additional_args = tuple()
            if self.notify:
                self.notifier.set_base_id(func.__name__)
                self.notifier.clear_output()
                additional_args = (self.notifier,)
            output = func(*args, *additional_args)

            if self.debug:
                self.logger.warning(f"{args}, {output}")

            if self.store:
                self._save_callback_call(func, args, output)

            if self.notify:
                output = self._format_notify_output(output)

            return output

        return callback(*self._args, **self._kwargs)(inner)

    def _save_callback_call(self, func: Callable, args: tuple[Any], result: Any):
        filename = Path(self.store_path) / f"{self.session_start}.yml"
        with open(filename, mode="a") as f:
            yaml.safe_dump(
                {
                    f"{func.__name__}.{self._n_call}": {
                        "args": args,
                        "result": result,
                    }
                },
                f,
            )
            self._n_call += 1

    def _format_notify_output(self, output):
        if self.notifier.output is None:
            output = (no_update, output)
        elif self._multioutput:
            output = (self.notifier.output, *output)
        elif not self._multioutput:
            output = (self.notifier.output, output)
        return output
