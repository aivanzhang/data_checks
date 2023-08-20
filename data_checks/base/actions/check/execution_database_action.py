import json
import sys
import traceback
from io import StringIO
from data_checks.base.actions.check.check_action import CheckAction
from data_checks.base.exceptions import DataCheckException
from data_checks.database.managers import (
    CheckManager,
    RuleManager,
    RuleExecutionManager,
)

"""
Action that deals with creating the rows related to the execution of check and rules in the database
"""


class ExecutionDatabaseAction(CheckAction):
    @staticmethod
    def setup(check) -> None:
        check._internal["check_model"] = CheckManager.latest(check.name)

    @staticmethod
    def before(check, context):
        rule = context["rule"]
        params = context["params"]

        rule = RuleManager.latest(
            suite_name=None
            if check._internal["suite_model"] is None
            else check._internal["suite_model"].name,
            check_name=check.name,
            group=json.dumps(check.group, default=str) if check.group else None,
            name=rule,
            params=json.dumps(params, default=str),
        )

        if not rule:
            return

        context["rule_model"] = rule

        new_rule_execution = RuleExecutionManager.create_execution(
            rule=rule,
            status="running",
            params=json.dumps(params, default=str),
        )

        rule_output = StringIO()

        context["output"] = rule_output
        sys.stdout = rule_output
        context["exec_id"] = new_rule_execution.id

    @staticmethod
    def on_success(check, context):
        """
        Executes after each successful child run
        """
        if "exec_id" not in context:
            return
        exec_id = context["exec_id"]
        RuleExecutionManager.update_execution(
            execution_id=exec_id,
            status="success",
            logs="",
        )

    @staticmethod
    def on_failure(check, context):
        """
        Executes after each failed child run
        """
        if "exec_id" not in context:
            return

        exec_id = context["exec_id"]
        exception: DataCheckException = context["exception"]
        RuleExecutionManager.update_execution(
            execution_id=exec_id,
            status="failure",
            logs="",
            traceback="\n".join(traceback.format_tb(exception.exception.__traceback__))
            if exception.exception
            else None,
            exception=exception.toJSON(),
        )

    @staticmethod
    def after(check, context):
        """
        Executes after each child run
        """
        sys.stdout = sys.__stdout__
        if "exec_id" not in context:
            return

        logs = ""
        exec_id = context["exec_id"]
        if exec_id and context["output"]:
            logs = context["output"].getvalue()
            if logs.strip() != "":
                print(logs)

        RuleExecutionManager.update_execution(
            execution_id=exec_id,
            logs=logs,
        )
