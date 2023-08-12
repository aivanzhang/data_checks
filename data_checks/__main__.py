import argparse
from copy import deepcopy
from data_checks.conf.data_suite_registry import data_suite_registry
from data_checks.utils.main_utils import run_suites_async

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
    "--exec_async",
    "-a",
    action="store_true",
    help="Run data suites asynchronously. This is useful for running suites in parallel. Order is not guaranteed.",
    default=False,
)

args = parser.parse_args()

suites_to_run = deepcopy(data_suite_registry.suites)


if len(args.exclude) > 0:
    print(f"Excluding the following data suites: {args.exclude}")
    for suite_name in args.exclude:
        del suites_to_run[suite_name]

if args.suite is not None:
    print(f"Running {args.suite}")
    data_suite_registry[args.suite]().run()
else:
    print(f"Running the following data suites: {list(suites_to_run.keys())}")
    if args.exec_async:
        run_suites_async(list(suites_to_run.values()))
    else:
        count = 1
        for suite_name, suite in suites_to_run.items():
            print(f"[{count}/{len(suites_to_run)} Suites] {suite_name}")
            suite().run()
            count += 1