from typing import TypedDict


class RuleContext(TypedDict):
    name: str
    description: str
    severity: float
    tags: set
    args: tuple
    kwargs: dict
