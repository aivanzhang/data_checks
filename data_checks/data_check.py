from data_checks.base.check import Check
from data_checks.utils import class_utils


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
