from rule_types import RuleContext

DEFAULT_RULE_CONTEXT: RuleContext = {
    "name": "",
    "description": "",
    "severity": 1.0,
    "tags": set(),
    "args": tuple(),
    "kwargs": dict(),
}
