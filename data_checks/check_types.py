from typing import TypedDict


# Function positional and keyword arguments
class FunctionArgs(TypedDict):
    args: tuple
    kwargs: dict


class RuleContext(TypedDict):
    name: str
    description: str
    severity: float
    args: tuple
    kwargs: dict
