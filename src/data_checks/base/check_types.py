from abc import ABC, abstractmethod
from typing import TypedDict, Dict, Callable, Optional, Union
from io import StringIO
from .rule_types import RuleContext
from .constants import DEFAULT_RULE_CONTEXT
from .dataset import Dataset
from ..database.managers import models


# Function positional and keyword arguments
class FunctionArgs(TypedDict):
    """
    Function positional and keyword arguments
    """

    args: tuple
    kwargs: dict


class CheckInternal(TypedDict):
    """
    Internal check data
    """

    suite_model: Optional[models.Suite]
    check_model: Optional[models.Check]
    check_execution_model: Optional[models.CheckExecution]
    rule_models: Dict[str, models.Rule]
    rule_execution_id_to_output: Dict[int, StringIO]


class CheckBase(ABC):
    """
    Base class for all checks
    """

    # Default rule context for rules missing fields
    DEFAULT_RULE_CONTEXT: RuleContext = DEFAULT_RULE_CONTEXT

    _internal: CheckInternal
    name: str
    dataset: Dataset
    shared_params: dict
    description: str
    rules: Dict[str, Callable[..., None]]  # Stores all the rules functions in the check
    rules_params: Dict[
        str,
        FunctionArgs
        | list[Union[FunctionArgs, dict, tuple]]
        | Callable[
            ..., FunctionArgs | dict | tuple | list[Union[FunctionArgs, dict, tuple]]
        ]
        | dict
        | tuple,
    ]  # Stores the params for each rule. If params is a list of params then run the rule multiple times with each param element
    rules_context: Dict[
        str, RuleContext
    ]  # Stores any metadata generated when a rule runs
    excluded_rules: set
    tags: set

    verbose: bool

    @classmethod
    @abstractmethod
    def rules_prefix(cls) -> str:
        """
        Prefix to automatically detect rules in the check
        """
        pass

    ...
