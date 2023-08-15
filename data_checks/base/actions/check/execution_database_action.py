import json
import sys
import traceback
from io import StringIO
from data_checks.base.actions.check.check_action import CheckAction
from data_checks.base.exceptions import DataCheckException
from data_checks.database.managers import (
    CheckManager,
    CheckExecutionManager,
    RuleManager,
    RuleExecutionManager,
)

"""
Action that deals with creating the rows related to the execution of check and rules in the database
"""


class ExecutionDatabaseAction(CheckAction):
    @staticmethod
    def update_execution(type: str, execution_id: int | None, **kwargs):
        """
        Update the execution of a rule
        """
        if type == "rule" and execution_id:
            RuleExecutionManager.update_execution(execution_id, **kwargs)
        if type == "check" and execution_id:
            CheckExecutionManager.update_execution(execution_id, **kwargs)

    @staticmethod
    def setup(check, context):
        """
        One time setup for check
        """
        check._internal["check_model"] = CheckManager.latest_version(check.name)

        check._internal[
            "check_execution_model"
        ] = CheckExecutionManager.create_execution(
            main_model=check._internal["check_model"], status="running"
        )

    @staticmethod
    def before(check, context):
        """
        Executes before each child run
        """
        rule = context["rule"]
        params = context["params"]

        if "rule_model" in context:
            main_model = context["rule_model"]

        elif check._internal["check_model"] is not None:
            main_model = RuleManager.latest_version(
                rule,
                check_id=check._internal["check_model"].id,
                suite_id=check._internal["suite_model"].id
                if check._internal["suite_model"]
                else None,
            )

        else:
            return

        # new_rule = latest of the check found in DB
        new_rule_execution = RuleExecutionManager.create_execution(
            main_model=main_model,
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
        exec_id = context["exec_id"]
        ExecutionDatabaseAction.update_execution(
            type="rule",
            execution_id=exec_id,
            status="success",
            logs="",
        )

    @staticmethod
    def on_failure(check, context):
        """
        Executes after each failed child run
        """
        exec_id = context["exec_id"]
        exception: DataCheckException = context["exception"]

        ExecutionDatabaseAction.update_execution(
            type="rule",
            execution_id=exec_id,
            status="failure",
            logs="",
            traceback=traceback.format_tb(exception.exception.__traceback__)
            if exception.exception
            else None,
            exception=exception.toJSON(),
        )

        if check._internal["check_execution_model"]:
            ExecutionDatabaseAction.update_execution(
                type="check",
                execution_id=check._internal["check_execution_model"].id,
                status="failure",
            )

    @staticmethod
    def after(check, context):
        """
        Executes after each child run
        """
        logs = ""
        exec_id = context["exec_id"]
        params = context["params"]
        if exec_id and context["output"]:
            logs = context["output"].getvalue()
            sys.stdout = sys.__stdout__
            if logs.strip() != "":
                print(logs)

        ExecutionDatabaseAction.update_execution(
            type="rule",
            execution_id=exec_id,
            params=json.dumps(params, default=str),
            logs=logs,
        )

    @staticmethod
    def teardown(check, context):
        """
        One time teardown for parent run
        """
        check_execution = check._internal["check_execution_model"]

        if check_execution:
            CheckExecutionManager.update_execution(
                check_execution.id,
                status="success",
            )
