import json
from croniter import croniter
from sqlalchemy import func, case
from datetime import datetime, timedelta
from data_checks.database.utils.session_utils import session_scope
from data_checks.database import RuleExecution, Rule, Suite


def get_latest(session, model, group_by, group_by_column):
    latest_created_at_subq = (
        session.query(
            group_by,
            func.max(model.created_at).label("latest_created_at"),
        )
        .group_by(group_by)
        .subquery()
    )

    return session.query(model).join(
        latest_created_at_subq,
        (group_by == latest_created_at_subq.c[group_by_column])
        & (model.created_at == latest_created_at_subq.c.latest_created_at),
    )


def get_executions_since(status=None, last_num_days: int = 1):
    with session_scope() as session:
        executions = (
            get_latest(
                session=session,
                model=RuleExecution,
                group_by=RuleExecution.rule_id,
                group_by_column="rule_id",
            )
            .filter(
                RuleExecution.created_at
                > datetime.now() - timedelta(days=last_num_days)
            )
            .all()
        )

        if status:
            print(f"Filtering by status: {status}")
            executions = [
                execution for execution in executions if execution.status == status
            ]
        for execution in executions:
            print(f"Rule: {execution.rule.name}")
            if status == None:
                print(f"Status: {execution.status}")
            print(f"Created at: {execution.created_at}")
            print(f"Finished at: {execution.finished_at}")
            print(f"Params: {execution.params}")
            print(f"Logs: {execution.logs}")
            print(f"Traceback: {execution.traceback}")
            print(f"Exception: {execution.exception}")
            print("\n")


def get_status_counts(last_num_days: int = 1):
    with session_scope() as session:
        counts_subquery = (
            session.query(
                RuleExecution.rule_id,
                func.count().label("total"),
                func.sum(case((RuleExecution.status == "success", 1), else_=0)).label(
                    "success_total"
                ),
                func.sum(case((RuleExecution.status == "failure", 1), else_=0)).label(
                    "failure_total"
                ),
            )
            .filter(
                RuleExecution.created_at
                > datetime.now() - timedelta(days=last_num_days)
            )
            .group_by(RuleExecution.rule_id)
            .subquery()
        )
        executions = (
            session.query(
                RuleExecution,
                counts_subquery.c.total,
                counts_subquery.c.success_total,
                counts_subquery.c.failure_total,
            )
            .join(counts_subquery, RuleExecution.rule_id == counts_subquery.c.rule_id)
            .all()
        )
        for execution, total, successes, failures in executions:
            print(f"Rule: {execution.rule}")
            print(f"Total: {total}")
            print(f"Successes: {successes}")
            print(f"Failures: {failures}")
            print("\n")


def get_silenced_rules():
    with session_scope() as session:
        rules = (
            get_latest(
                session=session,
                model=Rule,
                group_by=Rule.hash,
                group_by_column="hash",
            )
            .filter(Rule.config.contains('"' + "silenced_until" + '":'))
            .all()
        )

        for rule in rules:
            print(f"Rule: {rule.name}")
            print(f"Hash: {rule.hash}")
            print(f"Config: {rule.config }")
            print(f"Suite: {rule.suite.name}")
            print(f"Check: {rule.check.name}")
            print(f"Executions: {rule.executions}")
            print("\n")


def get_prev_next_executions():
    with session_scope() as session:
        suites = (
            get_latest(
                session=session,
                model=Suite,
                group_by=Suite.name,
                group_by_column="name",
            )
            .filter(Suite.config.contains('"' + "schedule" + '":'))
            .all()
        )
        current_time = datetime.now()

        for suite in suites:
            schedule = json.loads(suite.config).get("schedule", None)
            print(f"Suite: {suite.name}")
            print(f"Config: {suite.config}")
            print(f"Rules: {suite.rules}")

            if schedule:
                print(f"Schedule: {schedule}")
                cron = croniter(schedule, current_time)
                previous_execution_time = cron.get_prev()
                print(
                    "Previous execution:",
                    datetime.utcfromtimestamp(previous_execution_time),
                )
                next_execution_time = cron.get_next()
                print("Next execution:", datetime.utcfromtimestamp(next_execution_time))


def get_latest_rules():
    with session_scope() as session:
        rules = get_latest(
            session=session,
            model=Rule,
            group_by=Rule.hash,
            group_by_column="hash",
        ).all()

        for rule in rules:
            print(f"Rule: {rule.name}")
            print(f"Hash: {rule.hash}")
            print(f"Config: {rule.config }")
            print(f"Suite: {rule.suite.name}")
            print(f"Check: {rule.check.name}")
            print(f"Executions: {rule.executions}")
            print("\n")
