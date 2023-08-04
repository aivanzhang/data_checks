from typing import Callable, Iterable, Optional, TypeVar, ParamSpec, Concatenate
from .globals import rule_registry
from .check_types import CheckBase

CheckType = TypeVar("CheckType", bound=CheckBase)
RuleReturnParameters = ParamSpec("RuleReturnParameters")
RuleReturnType = TypeVar("RuleReturnType")


def rule(
    name: Optional[str] = None,
    description: Optional[str] = None,
    severity: Optional[float] = None,
    tags: Optional[Iterable] = None,
    should_prefix_tags: bool = False,
):
    """
    Decorator to instantiate a rule function inside a Check class
    Parameters:
        name: name of the rule
        description: description of the rule
        severity: severity of the rule
        tags: tags for the rule
        should_prefix_tags: if True, prefixes the tags with the check name
    """

    def wrapper(
        rule_func: Callable[
            Concatenate[CheckType, RuleReturnParameters], RuleReturnType
        ]
    ) -> Callable[Concatenate[CheckType, RuleReturnParameters], RuleReturnType]:
        rule_name = rule_func.__name__

        def wrapper_func(
            self: CheckType,
            *args: RuleReturnParameters.args,
            **kwargs: RuleReturnParameters.kwargs,
        ) -> RuleReturnType:
            self.rules_context[rule_name]["name"] = (
                name or self.DEFAULT_RULE_CONTEXT["name"]
            )
            self.rules_context[rule_name]["description"] = (
                description or self.DEFAULT_RULE_CONTEXT["description"]
            )
            self.rules_context[rule_name]["severity"] = (
                severity or self.DEFAULT_RULE_CONTEXT["severity"]
            )
            self.rules_context[rule_name]["args"].append(args)
            self.rules_context[rule_name]["kwargs"].append(kwargs)
            return rule_func(self, *args, **kwargs)

        wrapper_func.name = name or rule_name
        wrapper_func.is_rule = True
        wrapper_func.should_prefix_tags = should_prefix_tags
        wrapper_func.tags = set(tags or [])

        return wrapper_func

    return wrapper


def rule_func(
    name: Optional[str] = None,
    description: Optional[str] = None,
    severity: Optional[float] = None,
    tags: Optional[Iterable] = None,
):
    """
    Decorator to instantiate a rule function
    Parameters:
        name: name of the rule
        description: description of the rule
        severity: severity of the rule
        tags: tags for the rule
    """

    def wrapper(rule_func):
        rule_name = rule_func.__name__
        rule_registry[rule_name] = rule_func

        return rule_func

    return wrapper
