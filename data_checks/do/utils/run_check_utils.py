import argparse
import re
from multiprocessing import Process
from data_checks.base.actions.check import CheckAction
from data_checks.classes.data_check import DataCheck


def validate_cron_expression(value):
    # Regular expression to match a cron expression
    cron_pattern = r"^\s*((\*|[0-9,-]+)\s+){4}(\*|[0-9,-]+)\s*$"

    if re.match(cron_pattern, value):
        return value
    else:
        raise argparse.ArgumentTypeError("Invalid cron expression")


def start_check_deployment(check: DataCheck, is_async: bool = False):
    """
    Each check is run in a separate process so that stdout don't get mixed up
    """
    process = Process(target=check.run_all if not is_async else check.run_all_async)
    process.start()
    process.join()


def update_actions(check: DataCheck, check_actions: list[type[CheckAction]]):
    check.set_actions(check_actions)


def run_checks(
    checks_to_run: dict[str, type[DataCheck]],
    check_actions: list[type[CheckAction]],
    is_async: bool,
):
    if is_async:
        print("Starting async run")
        running_check_processes = []
        for check_name, check in checks_to_run.items():
            check = check()
            update_actions(check, check_actions)
            process = Process(target=check.run_all_async)
            process.start()
            running_check_processes.append(process)
        for process in running_check_processes:
            process.join()
    else:
        count = 1
        for check_name, check in checks_to_run.items():
            check = check()
            print(f"[{count}/{len(checks_to_run)} checks] {check_name}")
            update_actions(check, check_actions)
            check.run_all()
            count += 1
    return
