"""
Action that sends alerts on rule 
"""
import requests
from data_checks.conf.settings import settings
from data_checks.base.actions.check import CheckAction
from data_checks.base.check_types import CheckBase


class RuleAlertingAction(CheckAction):
    @staticmethod
    def on_success(check: CheckBase, context: dict) -> None:
        rule_execution_id = context["exec_id"]
        success_request = requests.post(
            settings["ALERTING_ENDPOINT"],
            data={"status": "success", "rule_execution_id": rule_execution_id},
        )
        if check.verbose:
            print(success_request.status_code, success_request.reason)

    @staticmethod
    def on_failure(check: CheckBase, context: dict) -> None:
        rule_execution_id = context["exec_id"]
        failed_request = requests.post(
            settings["ALERTING_ENDPOINT"],
            data={"status": "failure", "rule_execution_id": rule_execution_id},
        )
        if check.verbose:
            print(failed_request.status_code, failed_request.reason)
