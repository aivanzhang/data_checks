import argparse
from copy import deepcopy
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from data_checks.conf.settings import settings
from data_checks.conf.data_suite_registry import data_suite_registry
from data_checks.base.actions.suite import (
    SuiteAction,
    MainDatabaseAction,
    ErrorLoggingSuiteAction,
    FindSuiteModelAction,
)
from data_checks.base.actions.check import (
    MainDatabaseAction as CheckMainDatabaseAction,
    FindRuleModelAction,
    ExecutionDatabaseAction,
    ErrorLoggingCheckAction,
    SkipRuleExecutionAction,
    RuleAlertingAction,
)
from data_checks.base.suite import CheckActions
from data_checks.utils.main_utils import update_actions, run_suites, start_suite_run

parser = argparse.ArgumentParser(
    prog="python -m data_checks", description="Run a project's data checks."
)

parser.add_argument(
    "--only",
    "-o",
    type=str,
    choices=data_suite_registry.keys,
    help="Run a specific data suite.",
    default=None,
)

parser.add_argument(
    "--exclude",
    "-e",
    type=str,
    nargs="+",
    choices=data_suite_registry.keys,
    help="Exclude specific data suites.",
    default=[],
)

parser.add_argument(
    "--parallel",
    "-p",
    action="store_true",
    help="Run data suites in parallel. Order is not guaranteed.",
    default=False,
)

parser.add_argument(
    "--scheduling",
    "-sc",
    action="store_true",
    help="Only schedules the suites and does not run them.",
    default=False,
)

parser.add_argument(
    "--deploy",
    "-d",
    action="store_true",
    help="Deploy the existing scheduled data checks.",
    default=False,
)

parser.add_argument(
    "--error_logging",
    "-el",
    action="store_true",
    help="Log errors to the console. Note this will also log errors to the database.",
    default=False,
)

parser.add_argument(
    "--alerting",
    "-a",
    action="store_true",
    help="Log errors to the console. Note this will also log errors to the database.",
    default=False,
)


args = parser.parse_args()

suites_to_run = deepcopy(data_suite_registry.suites)


if len(args.exclude) > 0:
    print(f"Excluding the following data suites: {args.exclude}")
    for suite_name in args.exclude:
        del suites_to_run[suite_name]

if args.only is not None:
    if args.only in suites_to_run:
        suites_to_run = {args.only: suites_to_run[args.only]}
    else:
        raise ValueError(f"Suite {args.only} not found.")

default_suite_actions: list[type[SuiteAction]] = []
default_check_actions: CheckActions = {
    "default": [],
    "checks": {},
}

suite_actions: list[type[SuiteAction]]
check_actions: CheckActions

if args.error_logging:
    default_suite_actions += [ErrorLoggingSuiteAction]
    default_check_actions.update(
        {
            "default": [ErrorLoggingCheckAction],
        }
    )

if args.alerting:
    default_check_actions.update(
        {
            "default": [RuleAlertingAction],
        }
    )


if args.scheduling:
    print("Scheduling suites")
    # Create the suites and checks in the database with their respective schedules
    suite_actions = default_suite_actions + [MainDatabaseAction]
    check_actions = {
        "default": default_check_actions["default"]
        + [
            CheckMainDatabaseAction,
            SkipRuleExecutionAction,
        ],
        "checks": {},
    }
    run_suites(
        suites_to_run,
        suite_actions,
        check_actions,
        is_async=args.parallel,
    )

if args.deploy:
    print("Deploying suites")
    # Find database suites and checks to make the rule execution with
    suite_actions = default_suite_actions + [FindSuiteModelAction]
    check_actions = {
        "default": default_check_actions["default"]
        + [FindRuleModelAction, ExecutionDatabaseAction],
        "checks": {},
    }
    scheduler = BackgroundScheduler()
    for suite_name, suite in suites_to_run.items():
        schedule = suite.suite_config().get("schedule", settings["DEFAULT_SCHEDULE"])
        print(f"[CRON JOB - {schedule}] {suite_name}")
        suite = suite()
        update_actions(suite, suite_actions, check_actions)
        scheduler.add_job(
            start_suite_run,
            CronTrigger.from_crontab(schedule),
            id=suite_name,
            args=(
                suite,
                args.parallel,
            ),
        )

    scheduler.start()

    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

if not (args.scheduling or args.deploy):
    run_suites(
        suites_to_run=suites_to_run,
        actions=default_suite_actions,
        check_actions={"default": default_check_actions["default"], "checks": {}},
        is_async=args.parallel,
    )
