import argparse
from copy import deepcopy
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from multiprocessing import Process
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
    ExecutionDatabaseAction,
    ErrorLoggingCheckAction,
    SkipRuleExecutionAction,
    RuleAlertingAction,
)
from data_checks.base.suite import CheckActions
from data_checks.classes.data_suite import DataSuite


def start_suite_deployment(suite: DataSuite, is_async: bool = False):
    """
    Each suite is run in a separate process so that stdout don't get mixed up
    """
    process = Process(target=suite.run if not is_async else suite.run_async)
    process.start()
    process.join()


def update_actions(
    suite: DataSuite,
    suite_actions: list[type[SuiteAction]],
    check_actions: CheckActions,
):
    suite.set_actions(suite_actions)
    suite.set_check_actions(check_actions)


def run_suites(
    suites_to_run: dict[str, type[DataSuite]],
    actions: list[type[SuiteAction]],
    check_actions: CheckActions,
    is_async: bool = False,
):
    if is_async:
        print("Starting async run")
        running_suite_processes = []
        for suite_name, suite in suites_to_run.items():
            print(f"Running suite {suite_name}")
            suite = suite()
            update_actions(suite, actions, check_actions)
            process = Process(target=suite.run_async)
            process.start()
            running_suite_processes.append(process)
        for process in running_suite_processes:
            process.join()
    else:
        count = 1
        for suite_name, suite in suites_to_run.items():
            print(f"[{count}/{len(suites_to_run)} Suites] {suite_name}")
            suite = suite()
            update_actions(suite, actions, check_actions)
            suite.run()
            count += 1


def main():
    parser = argparse.ArgumentParser(
        prog="python -m data_checks", description="Run a project's data checks."
    )

    parser.add_argument(
        "--only",
        "-o",
        type=str,
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
        "--deploy",
        "-d",
        action="store_true",
        help="Deploy the existing scheduled data checks.",
        default=False,
    )

    parser.add_argument(
        "--disable_exception_logging",
        "-s",
        action="store_true",
        help="Disable exception logs to the console. Set this flag if you see superfluous logs.",
        default=False,
    )

    parser.add_argument(
        "--alerting",
        "-a",
        action="store_true",
        help="Alerts the user when a data check fails. Make sure to set up the alerting endpoint in the settings file.",
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

    if not args.disable_exception_logging:
        default_suite_actions += [ErrorLoggingSuiteAction]
        default_check_actions["default"].append(ErrorLoggingCheckAction)

    if args.alerting:
        default_check_actions["default"].append(RuleAlertingAction)

    if args.deploy:
        print("Creating database rows for suites, checks, and rows.")
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

        print("Deploying suites")
        # Find database suites and checks to make the rule execution with
        suite_actions = default_suite_actions + [
            FindSuiteModelAction,  # Finds the corresponding Suite model for the check and rule
        ]
        check_actions = {
            "default": default_check_actions["default"] + [ExecutionDatabaseAction],
            "checks": {},
        }
        scheduler = BackgroundScheduler()
        for suite_name, suite in suites_to_run.items():
            schedule = suite.suite_config().get(
                "schedule", settings["DEFAULT_SCHEDULE"]
            )
            print(f"[CRON JOB - {schedule}] {suite_name}")
            suite = suite()
            update_actions(suite, suite_actions, check_actions)
            scheduler.add_job(
                start_suite_deployment,
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

    if not args.deploy:
        run_suites(
            suites_to_run=suites_to_run,
            actions=default_suite_actions,
            check_actions={
                "default": default_check_actions["default"],
                "checks": {},
            },
            is_async=args.parallel,
        )
