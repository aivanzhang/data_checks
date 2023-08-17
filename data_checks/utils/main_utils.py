from multiprocessing import Process
from data_checks import DataSuite
from data_checks.base.actions.suite import SuiteAction
from data_checks.base.suite import CheckActions


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
