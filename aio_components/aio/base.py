from typing import Any, Callable


def is_dunder(name: str) -> bool:
    return (
            len(name) > 4
            and name.isascii()
            and name.startswith("__")
            and name.endswith("__")
    )


def is_private(name: str) -> bool:
    return name.startswith("_")


def is_callable(value: Any) -> bool:
    return isinstance(value, Callable)


class BaseMetaAIOId(type):
    def __new__(
            cls, cls_name: str, bases: tuple[type[Any], ...], namespace: dict[str, Any]
    ):
        attributes = {
            key: value
            for key, value in namespace.items()
            if not is_dunder(key) and not is_private(key) and not is_callable(value)
        }
        namespace['_class_attributes'] = attributes

        x = super().__new__(cls, cls_name, bases, namespace)
        return x


class BaseAIOId(metaclass=BaseMetaAIOId):
    _class_attributes: dict[str, Any]

    def __init__(self, aio_id: str):
        self.aio_id = aio_id
        for key, value in self._class_attributes.items():
            setattr(self, key, self.compose_id(value))

    def compose_id(self, inner_id: str):
        return '-'.join((self.aio_id, inner_id))
