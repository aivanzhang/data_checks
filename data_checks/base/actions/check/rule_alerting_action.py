"""
Action that sends alerts on rule 
"""
import requests
import json
from data_checks.conf.settings import settings
from data_checks.base.actions.check import CheckAction
from data_checks.base.check_types import CheckBase


class RuleAlertingAction(CheckAction):
    @staticmethod
    def on_success(check: CheckBase, context) -> None:
        rule_execution_id = None
        if "exec_id" in context["sys"]:
            rule_execution_id = context.get_sys("exec_id")

        success_request = requests.post(
            settings["ALERTING_ENDPOINT"],
            data={
                "status": "success",
                "rule_execution_id": rule_execution_id,
                "context": json.dumps(context, default=str),
            },
        )
        if check.verbose:
            print(success_request.status_code, success_request.reason)

    @staticmethod
    def on_failure(check: CheckBase, context) -> None:
        rule_execution_id = None
        if "exec_id" in context["sys"]:
            rule_execution_id = context.get_sys("exec_id")

        failed_request = requests.post(
            settings["ALERTING_ENDPOINT"],
            data={
                "status": "failure",
                "rule_execution_id": rule_execution_id,
                "context": json.dumps(context, default=str),
            },
        )
        if check.verbose:
            print(failed_request.status_code, failed_request.reason)
