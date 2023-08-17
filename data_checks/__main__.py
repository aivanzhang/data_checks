import argparse
from copy import deepcopy
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from multiprocessing import Process
from data_checks.conf.settings import settings
from data_checks.conf.data_suite_registry import data_suite_registry
from data_checks.base.suite import Suite
from data_checks.base.actions.suite import (
    SuiteAction,
    MainDatabaseAction,
    DefaultSuiteAction,
    FindSuiteModelAction,
)
from data_checks.base.actions.check import (
    MainDatabaseAction as CheckMainDatabaseAction,
    FindRuleModelAction,
    ExecutionDatabaseAction,
    DefaultCheckAction,
    SkipRuleExecutionAction,
)
from data_checks.base.suite import CheckActions
from data_checks.utils.main_utils import update_actions, run_suites

parser = argparse.ArgumentParser(
    prog="python -m data_checks", description="Run a project's data checks."
)

parser.add_argument(
    "--suite",
    "-s",
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
    "--async",
    "-a",
    action="store_true",
    help="Run data suites asynchronously. This is useful for running suites in parallel. Order is not guaranteed.",
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

args = parser.parse_args()

suites_to_run = deepcopy(data_suite_registry.suites)


if len(args.exclude) > 0:
    print(f"Excluding the following data suites: {args.exclude}")
    for suite_name in args.exclude:
        del suites_to_run[suite_name]

if args.suite is not None:
    suites_to_run = {args.suite: suites_to_run[args.suite]}

suite_actions: list[type[SuiteAction]] = []
check_actions: CheckActions = {"default": [], "checks": {}}


if args.scheduling:
    print("Scheduling suites")
    suite_actions = [DefaultSuiteAction, MainDatabaseAction]
    check_actions: CheckActions = {
        "default": [
            DefaultCheckAction,
            CheckMainDatabaseAction,
            SkipRuleExecutionAction,
        ],
        "checks": {},
    }
    run_suites(
        suites_to_run,
        suite_actions,
        check_actions,
        is_async=getattr(args, "async"),
    )

if args.deploy:
    suite_actions = [FindSuiteModelAction]
    check_actions: CheckActions = {
        "default": [FindRuleModelAction, ExecutionDatabaseAction],
        "checks": {},
    }
    scheduler = BackgroundScheduler()
    for suite_name, suite in suites_to_run.items():
        schedule = suite.suite_config().get("schedule", settings["DEFAULT_SCHEDULE"])
        print(f"[CRON JOB - {schedule}] {suite_name}")
        suite = suite()
        update_actions(suite, suite_actions, check_actions)
        suite_run_func = suite.run_async if getattr(args, "async") else suite.run
        scheduler.add_job(
            suite_run_func, CronTrigger.from_crontab(schedule), id=suite_name
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
        actions=[],
        check_actions={"default": [], "checks": {}},
        is_async=getattr(args, "async"),
    )
