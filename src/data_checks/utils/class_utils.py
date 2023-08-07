"""
This module contains functions for working with classes.
"""
from types import FunctionType
from typing import Any
import inspect


def get_all_methods(cls: object) -> list[str]:
    """
    Get list of methods (excluding magic methods) for a class.
    """
    return [
        func
        for func in dir(cls)
        if callable(getattr(cls, func)) and not func.startswith("__")
    ]


def extract_wrapped(decorated):
    closure = (c.cell_contents for c in decorated.__closure__)
    return next((c for c in closure if isinstance(c, FunctionType)), None)


def get_function_code(cls: object, function_name: str):
    function_obj: Any = extract_wrapped(getattr(cls, function_name))
    source_code = inspect.getsource(function_obj)
    return source_code


def get_class_code(cls: type):
    parent_classes = cls.__bases__
    source = ""

    for parent in parent_classes:
        print(parent)
        if parent.__name__ == "Check" or parent.__name__ == "Suite":
            continue
        source += inspect.getsource(parent) + "\n"

    source += inspect.getsource(cls)
    return source
