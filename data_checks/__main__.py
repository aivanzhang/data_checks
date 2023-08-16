import argparse
from copy import deepcopy
from multiprocessing import Process
from data_checks.conf.data_suite_registry import data_suite_registry
from data_checks.base.suite import Suite
from data_checks.base.actions.suite import SuiteAction, MainDatabaseAction
from data_checks.base.actions.check import (
    MainDatabaseAction as CheckMainDatabaseAction,
)
from data_checks.base.suite import CheckActions

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


def update_actions(suite: Suite):
    # print(f"Updating actions for {suite}")
    suite.add_actions(*suite_actions)
    # print(f"Adding suite actions for {suite, suite_actions}")
    suite.update_check_actions(check_actions)
    # print(f"Adding check actions for {suite, check_actions}")


def run_suite():
    is_async = getattr(args, "async")
    if is_async:
        print("Starting async run")
        running_suite_processes = []
        for suite_name, suite in suites_to_run.items():
            print(f"[Running Suite] {suite_name}")
            suite = suite()
            update_actions(suite)
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
            update_actions(suite)
            suite.run()
            count += 1


if args.scheduling:
    print("Scheduling suites")
    suite_actions = [MainDatabaseAction]
    check_actions["default"] = [CheckMainDatabaseAction]
    run_suite()

    # getattr(suite(), "schedule")()
