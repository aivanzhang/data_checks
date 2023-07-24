"""
This module contains functions for working with classes.
"""


def get_all_methods(cls: object) -> list[str]:
    """
    Get list of methods (excluding magic methods) for a class.
    """
    return [
        func
        for func in dir(cls)
        if callable(getattr(cls, func)) and not func.startswith("__")
    ]
