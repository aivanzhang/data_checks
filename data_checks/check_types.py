from typing import TypedDict


# Function positional and keyword arguments
class FunctionArgs(TypedDict):
    args: tuple
    kwargs: dict
