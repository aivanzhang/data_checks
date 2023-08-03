from typing import TypedDict, Callable


class RuleContext(TypedDict):
    name: str
    description: str
    severity: float
    tags: set
    run_if: Callable[..., bool]
    args: list[tuple]
    kwargs: list[dict]
