from abc import ABC
from typing import TypedDict, Dict, Callable, Optional
from .rule_types import RuleContext
from .constants import DEFAULT_RULE_CONTEXT
from .dataset import Dataset
from .database.managers import models


# Function positional and keyword arguments
class FunctionArgs(TypedDict):
    """
    Function positional and keyword arguments
    """

    args: tuple
    kwargs: dict


class CheckInternal(TypedDict):
    """
    Internal suite data
    """

    suite_model: Optional[models.Suite]
    check_model: Optional[models.Check]


class CheckBase(ABC):
    """
    Base class for all checks
    """

    # Default rule context for rules missing fields
    DEFAULT_RULE_CONTEXT: RuleContext = DEFAULT_RULE_CONTEXT

    _internal: CheckInternal
    name: str
    dataset: Optional[Dataset]
    description: str
    rules_prefix: str  # Prefix for all rules in the check to be automatically run
    rules: Dict[str, Callable[..., None]]  # Stores all the rules functions in the check
    rules_params: Dict[
        str,
        FunctionArgs
        | list[FunctionArgs]
        | Callable[..., FunctionArgs | list[FunctionArgs]],
    ]  # Stores the params for each rule. If params is a list of params then run the rule multiple times with each param element
    rules_context: Dict[
        str, RuleContext
    ]  # Stores any metadata generated when a rule runs
    excluded_rules: set
    tags: set

    verbose: bool
    ...
