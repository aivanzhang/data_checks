"""
Action Mixin for Executing Actions on Data Checks
"""
from data_checks.base.actions import ActionBase


class ActionMixin:
    def __init__(self):
        self.actions: list[type[ActionBase]] = []

    def _exec_actions(self, action_type: str, context: dict = {}, **kwargs):
        """
        Execute an action
        """
        context[action_type] = {}
        for action in self.actions:
            action_func = getattr(action, action_type, None)
            if action_func is not None:
                if action_type == "setup" or action_type == "teardown":
                    action_func(self)
                else:
                    action_func(self, context, **kwargs)

    def setup(self):
        """
        Runs all the setup functions
        """
        self._exec_actions("setup")

    def before(self, context: dict):
        """
        Run before each rule. If None, the rule will not be run
        """
        self._exec_actions("before", context)

    def after(self, context: dict):
        """
        Runs after each rule
        """
        self._exec_actions("after", context)

    def on_success(self, context: dict):
        """
        Called when a rule succeeds
        """
        self._exec_actions("on_success", context)

    def on_failure(self, context: dict):
        """
        Called when a rule fails
        """
        self._exec_actions("on_failure", context)

    def teardown(self):
        """
        One time teardown after all rules are run
        """
        self._exec_actions("teardown")

    def add_actions(self, *actions: type[ActionBase]):
        """
        Add actions to the check
        """
        for action in actions:
            self.actions.append(action)

    def remove_actions(self, *actions: type[ActionBase]):
        """
        Remove actions from the check
        """
        for action in actions:
            self.actions.remove(action)
