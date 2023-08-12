from data_checks.base.check import Check
from data_checks.utils import class_utils


class DataCheck(Check):
    @classmethod
    def defined_rules(cls) -> list[str]:
        return class_utils.get_current_class_specific_methods(cls)

    @classmethod
    def check_config(cls) -> dict:
        """
        System configuration for the check. In the following format:
        {
            "schedule": "0 8 * * *", # Cron schedule for all rule. If undefined runs just once.
            "rule_schedules": {
                "rule_name_1": "0 8 * * *", # Rule-specific cron schedule
                "rule_name_2": "0 8 * * *", # Rule-specific cron schedule
                ...
            }
        }
        """
        return {"schedule": "0 8 * * *"}
