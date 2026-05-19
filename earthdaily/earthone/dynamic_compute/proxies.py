import datetime
import re
from typing import Type, Union

PARAM_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def is_datetime_parameter_name(name: str) -> bool:
    return bool(PARAM_NAME_RE.match(name))


class Proxytype:
    "Proxytype abstract base class"

    def __bool__(self):
        # Ensure Proxytypes can't be used in conditionals;
        # Python default would always resolve to True.
        raise TypeError(
            "Truth value of Proxytype {} objects is not supported".format(
                type(self).__name__
            )
        )

    def __contains__(self, _):
        if hasattr(self, "contains"):
            raise TypeError(
                (
                    "Please use {}.contains(other). Python requires a bool to be returned "
                    "from __contains__ and this value cannot be known for proxy types."
                ).format(type(self).__name__)
            )
        else:
            raise TypeError(
                "object of type {} does not support `in`.".format(type(self).__name__)
            )

    def __len__(self):
        if hasattr(self, "length"):
            raise TypeError(
                (
                    "Please use {}.length(). Python requires an int to be returned "
                    "from __len__ and this value cannot be known for proxy types."
                ).format(type(self).__name__)
            )
        else:
            raise TypeError(
                "object of type {} has no len()".format(type(self).__name__)
            )

    def __iter__(self):
        if hasattr(self, "map"):
            raise TypeError(
                (
                    "Proxy {0} is not iterable. Consider using {0}.map(...) instead."
                ).format(type(self).__name__)
            )
        else:
            raise TypeError(
                "object of type {} is not iterable.".format(type(self).__name__)
            )


class Datetime(Proxytype):
    # Kelly note: this is currently unverified anywhere, but we
    # may want to use the `allowed_types` property  in the
    # future to ensure the type of data being passed in is allowed
    allowed_types = Union[str, datetime.date, datetime.datetime]


class NumericProxy(Proxytype):
    # Kelly note: this is currently unverified anywhere, but we
    # may want to use the `allowed_types` property  in the
    # future to ensure the type of data being passed in is allowed
    allowed_types = Union[int, float]


class parameter:
    _RETURN_PRECEDENCE = 0

    def __init__(self, name: str, _type: Type[Proxytype]):
        assert isinstance(
            name, str
        ), f"Names must be strings, provided name was {type(name)} type"
        if _type is Datetime:
            assert is_datetime_parameter_name(name), (
                "Datetime parameter names must be valid identifiers "
                "(e.g. 'start', 'end_date'), not date literals or strings with spaces."
            )
        assert (
            _type != Proxytype
        ), "Cannot use Proxytype as type, you need to specify a defined type"
        assert issubclass(
            _type, Proxytype
        ), f"Specified type must be a subclass of Proxytype, not {type(_type)}"
        self.name = name
        self.type = _type
