from typing import TypedDict


class RuleContext(TypedDict):
    name: str
    description: str
    severity: float
    tags: set
    args: list[tuple]
    kwargs: list[dict]


class RuleData(TypedDict):
    """
    Data to be passed from decorator to rules_context
    """

    name: str
    description: str
    severity: float
    tags: set
