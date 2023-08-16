import json
import sys
import traceback
from io import StringIO
from data_checks.base.actions.check.check_action import CheckAction
from data_checks.base.exceptions import DataCheckException
from data_checks.database.managers import (
    RuleExecutionManager,
)

"""
Action that deals with creating the rows related to the execution of check and rules in the database
"""


class ExecutionDatabaseAction(CheckAction):
    @staticmethod
    def before(check, context):
        params = context["params"]

        if "rule_model" not in context:
            return

        rule = context["rule_model"]
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
            traceback="".join(traceback.format_tb(exception.exception.__traceback__))
            if exception.exception
            else None,
            exception=exception.toJSON(),
        )

    @staticmethod
    def after(check, context):
        """
        Executes after each child run
        """
        if "exec_id" not in context:
            sys.stdout = sys.__stdout__
            return

        logs = ""
        exec_id = context["exec_id"]

        params = context["params"]
        if exec_id and context["output"]:
            logs = context["output"].getvalue()
            sys.stdout = sys.__stdout__
            if logs.strip() != "":
                print(logs)

        RuleExecutionManager.update_execution(
            execution_id=exec_id,
            logs=logs,
            params=json.dumps(params, default=str),
        )
