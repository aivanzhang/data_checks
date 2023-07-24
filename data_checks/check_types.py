from abc import ABC
from typing import TypedDict, Dict, Callable
from rule_types import RuleContext
from constants import DEFAULT_RULE_CONTEXT


# Function positional and keyword arguments
class FunctionArgs(TypedDict):
    args: tuple
    kwargs: dict


class CheckBase(ABC):
    # Default rule context for rules missing fields
    DEFAULT_RULE_CONTEXT: RuleContext = DEFAULT_RULE_CONTEXT

    verbose: bool

    name: str
    description: str
    rules_prefix: str  # Prefix for all rules in the check to be automatically run
    rules: Dict[str, Callable[..., None]]  # Stores all the rules functions in the check
    rule_params: Dict[
        str, FunctionArgs | Callable[..., FunctionArgs]
    ]  # Stores the params for each rule
    rules_context: Dict[
        str, RuleContext
    ]  # Stores any metadata generated when a rule runs
    tags: set
    ...
