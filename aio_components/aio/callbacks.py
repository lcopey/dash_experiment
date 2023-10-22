from datetime import datetime
from functools import wraps
from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Union

import yaml
from dash import callback


class Callback:
    @wraps(callback)
    def __init__(
        self,
        *args,
        debug: bool = False,
        store: bool = False,
        store_path: Union[str, Path] = None,
        **kwargs,
    ):
        self.debug = debug
        if self.debug:
            self.logger = getLogger(__name__)

        self.store = store
        if self.store:
            assert (
                store_path is not None
            ), "store_path should not be None when store=True"
            self.store_path = store_path
            self.session_start = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._args = args
        self._kwargs = kwargs
        self._n_call = 0

    def __call__(self, func: Callable):
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            if self.debug:
                self.logger.warning(f"{args}, {kwargs}, {result}")
            if self.store:
                filename = Path(self.store_path) / f"{self.session_start}.yml"
                with open(filename, mode="a") as f:
                    yaml.safe_dump(
                        {
                            f"{func.__name__}.{self._n_call}": {
                                "args": args,
                                "kwargs": kwargs,
                                "result": result,
                            }
                        },
                        f,
                    )
                self._n_call += 1
            return result

        return callback(*self._args, **self._kwargs)(inner)
