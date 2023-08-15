import argparse
from copy import deepcopy
from multiprocessing import Process
from data_checks.conf.data_suite_registry import data_suite_registry

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
    help="Runs the suites in schedule mode. Suites don't execute checks, but instead schedule them.",
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
    print("Running {args.suite}")
    data_suite_registry[args.suite]().run()
else:
    print(f"Running the following data suites: {','.join(list(suites_to_run.keys()))}")
    if getattr(args, "async"):
        running_suite_processes = []
        for suite_name, suite in suites_to_run.items():
            print(f"ASYNC RUN {suite_name}")
            process = Process(target=suite().run_async)
            process.start()
            running_suite_processes.append(process)
        for process in running_suite_processes:
            process.join()
    else:
        count = 1
        for suite_name, suite in suites_to_run.items():
            print(f"[{count}/{len(suites_to_run)} Suites] {suite_name}")
            suite().run()
            count += 1
