import json
import sys
import pandas as pd
import traceback
from datetime import datetime, timezone
from io import StringIO
from data_checks.base.actions.check.check_action import CheckAction
from data_checks.base.exceptions import DataCheckException, SkipExecutionException
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
        rule = context.get_sys("rule")
        params = context.get_sys("params")

        rule = RuleManager.latest(
            suite_name=None
            if check._internal["suite_model"] is None
            else check._internal["suite_model"].name,
            check_name=check.name,
            name=rule,
            params=json.dumps(params, default=str),
        )

        if not rule:
            return

        rule_config = json.loads(rule.config) if rule.config else {}
        silenced_until = rule_config.get("silenced_until", None)
        if silenced_until and pd.to_datetime(silenced_until) > datetime.now(
            tz=timezone.utc
        ):
            raise SkipExecutionException(
                f"Rule {rule.name} is silenced until {silenced_until}"
            )

        context.set_sys("rule_model", rule)

        new_rule_execution = RuleExecutionManager.create_execution(
            rule=rule,
            status="running",
            params=json.dumps(params, default=str),
        )

        rule_output = StringIO()

        context.set_sys("output", rule_output)
        sys.stdout = rule_output
        context.set_sys("exec_id", new_rule_execution.id)

    @staticmethod
    def on_success(check, context):
        """
        Executes after each successful child run
        """
        if "exec_id" not in context["sys"]:
            return
        exec_id = context.get_sys("exec_id")
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
        if "exec_id" not in context["sys"]:
            return
        exec_id = context.get_sys("exec_id")
        exception: DataCheckException = context.get_sys("exception")
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
        if "exec_id" not in context["sys"]:
            return
        exec_id = context.get_sys("exec_id")

        logs = ""
        if exec_id and "output" in context["sys"]:
            logs = context.get_sys("output").getvalue()
            if logs.strip() != "":
                print(logs)

        RuleExecutionManager.update_execution(
            execution_id=exec_id,
            logs=logs,
        )
