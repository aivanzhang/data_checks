from abc import ABC, abstractmethod
from typing import TypedDict, Dict, Callable, Optional, Union
from data_checks.base.dataset import Dataset
from data_checks.base.actions.action_types import ActionBase
from data_checks.database.managers import models


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


class CheckSchedule(TypedDict):
    """
    Check schedule
    """

    schedule: str
    rule_schedules: dict[str, str]


class CheckBase(ABC):
    """
    Base class for all checks
    """

    _internal: CheckInternal
    name: str
    dataset: Dataset
    config: dict
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
    excluded_rules: set
    schedule: CheckSchedule
    tags: set
    actions: list[type[ActionBase]]

    verbose: bool

    @classmethod
    @abstractmethod
    def defined_rules(cls) -> list[str]:
        """
        Rules to be run by the check. Each rule should be a function in the check class.
        """
        pass

    @classmethod
    @abstractmethod
    def check_config(cls) -> dict:
        """
        System configuration for the check
        """
        pass

    ...
