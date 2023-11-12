from typing import Any, Callable


class auto(str):
    """Class to automatically name an attribute."""

    pass


def _is_dunder(name: str) -> bool:
    return (
        len(name) > 4
        and name.isascii()
        and name.startswith("__")
        and name.endswith("__")
    )


def _is_private(name: str) -> bool:
    return name.startswith("_")


def _is_callable(value: Any) -> bool:
    return isinstance(value, Callable)


def _is_valid_id_attribute(key: str, value: Any):
    return not _is_dunder(key) and not _is_private(key) and not _is_callable(value)


class BaseMetaId(type):
    def __new__(
        cls, cls_name: str, bases: tuple[type[Any], ...], namespace: dict[str, Any]
    ):
        _ids = {}
        for base in bases:
            _base_ids = getattr(base, "_ids")
            if _base_ids:
                _ids.update(_base_ids)

        _ids.update(
            {
                key: value
                for key, value in namespace.items()
                if _is_valid_id_attribute(key, value)
            }
        )
        namespace["_ids"] = _ids

        x = super().__new__(cls, cls_name, bases, namespace)
        return x


class BaseId(metaclass=BaseMetaId):
    _ids: dict[str, Any]

    def __init__(self, aio_id: str):
        self.aio_id = aio_id
        for key, value in self._ids.items():
            if isinstance(value, auto):
                value = key
            setattr(self, key, self.compose_ids(value))

    def compose_ids(self, inner_id: str):
        return "-".join((self.aio_id, inner_id))
