"""
This module contains functions for working with classes.
"""
from types import FunctionType
from typing import Any
import inspect
import os
import importlib.util


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
    function_obj: Any = getattr(cls, function_name)
    if function_obj.__closure__ is not None:
        function_obj = extract_wrapped(function_obj)
    source_code = inspect.getsource(function_obj)
    return source_code


def get_current_class_specific_methods(cls):
    """
    Get list of methods (excluding magic methods) specifically defined by the current class and not any of its parents.
    """

    return [
        func_name
        for func_name in dir(cls)
        if callable(getattr(cls, func_name))
        and not func_name.startswith("__")
        and func_name not in get_all_methods(cls.__bases__[0])
    ]


def get_class_code(cls: type):
    parent_classes = cls.__bases__
    source = ""

    for parent in parent_classes:
        if parent.__name__ == "Check" or parent.__name__ == "Suite":
            continue
        source += inspect.getsource(parent) + "\n"

    source += inspect.getsource(cls)
    return source
