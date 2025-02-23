from importlib import import_module
import inspect
from pathlib import Path
import pkgutil
from typing import Dict, Optional, Type

from sqltask.engine_specs.base import BaseEngineSpec

_engines: Dict[str, Type[BaseEngineSpec]] = {}

for (_, name, _) in pkgutil.iter_modules([Path(__file__).parent]):  # type: ignore
    imported_module = import_module("." + name, package=__name__)

    for i in dir(imported_module):
        attribute = getattr(imported_module, i)

        if (
            inspect.isclass(attribute)
            and issubclass(attribute, BaseEngineSpec)
            and attribute.engine != ""
        ):
            _engines[attribute.engine] = attribute


def get_engine_spec(engine_name: Optional[str]) -> Type[BaseEngineSpec]:
    """
    Get an engine spec based on an engine name, e.g. snowflake.

    :param engine_name: Name of engine, i.e. engine.name
    :return: Engine spec for a given engine name. Returns `BaseEngineSpec`
    if engine does not have a dedicated spec available.
    """
    return _engines[engine_name if engine_name in _engines else None]
