from data_checks.base.check import Check
from data_checks.base.actions.execution_context import ExecutionContext


class DataCheck(Check):
    @classmethod
    def defined_rules(cls) -> list[str]:
        return super().defined_rules()

    @classmethod
    def check_config(cls) -> dict:
        """
        You can attach any configuration option as long as it is JSON serializable.
        The only system defined config option is "rules_config", which is a
        dictionary of rule configurations. In the following format:
        {
            "check_config_option_1": value1,
            "check_config_option_2": value2,
            ...
            "rules_config": {

                "rule_1": {
                    "rule_config_option_1": value1,
                    "rule_config_option_2": value2,
                    ...
                },
                "rule_2": {
                    "rule_config_option_1": value1,
                    "rule_config_option_2": value2,
                    ...
                },
                ...
            }
        }
        """
        return {}

    def setup(self):
        """
        Setup the check. Use this to load data, initialize models, etc.
        For example `self.df = pd.read_csv("data.csv")` sets a dataframe
        for all the rules to use.
        """
        super().setup()

    def before(self, context: ExecutionContext):
        """
        Run before each rule. If None, the rule will not be run
        """
        super().before(context)

    def after(self, context: ExecutionContext):
        """
        Runs after each rule
        """
        super().before(context)

    def on_success(self, context: ExecutionContext):
        """
        Called when a rule succeeds
        """
        super().before(context)

    def on_failure(self, context: ExecutionContext):
        """
        Called when a rule fails
        """
        super().before(context)

    def teardown(self):
        """
        Teardown the check. Use this to close connections, etc.
        """
        super().teardown()
