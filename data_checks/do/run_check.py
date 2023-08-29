if __name__ == "__main__":
    import argparse
    from copy import deepcopy
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.cron import CronTrigger
    from data_checks.conf.data_check_registry import data_check_registry
    from data_checks.base.actions.check import CheckAction
    from data_checks.do.utils.run_check_utils import *

    from data_checks.base.actions.check import (
        MainDatabaseAction as CheckMainDatabaseAction,
        ExecutionDatabaseAction,
        ErrorLoggingCheckAction,
        SkipRuleExecutionAction,
        RuleAlertingAction,
    )

    parser = argparse.ArgumentParser(
        prog="python -m data_checks.do.run_check",
        description="Run data checks.",
    )

    parser.add_argument(
        "checks",
        nargs="+",
        choices=data_check_registry.keys,
        help="One or more checks to run.",
        default=[],
    )

    parser.add_argument(
        "--parallel",
        "-p",
        action="store_true",
        help="Run data checks in parallel. Order is not guaranteed.",
        default=False,
    )

    parser.add_argument(
        "--schedule",
        "-s",
        type=validate_cron_expression,
        help="Schedule and deploy the data checks to run at a specific time based off a specific cron expression.",
        default=None,
    )

    parser.add_argument(
        "--disable_exception_logging",
        "-d",
        action="store_true",
        help="Disable exceptions logs to the console. Set this flag if you see superfluous logs.",
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

    checks_to_run = deepcopy(data_check_registry.checks)
    default_check_actions: list[type[CheckAction]] = []

    if not args.disable_exception_logging:
        default_check_actions.append(ErrorLoggingCheckAction)

    if args.alerting:
        default_check_actions.append(RuleAlertingAction)

    updated_checks_to_run = {}
    for check_name in args.checks:
        if check_name in checks_to_run:
            updated_checks_to_run[check_name] = checks_to_run[check_name]
        else:
            print(f"Check {check_name} not found.")
    checks_to_run = updated_checks_to_run

    if not len(checks_to_run.keys()):
        print("No checks to run.")
        exit(0)

    if args.schedule:
        # Create the checks in the database
        run_checks(
            checks_to_run=checks_to_run,
            check_actions=default_check_actions
            + [
                CheckMainDatabaseAction,
                SkipRuleExecutionAction,
            ],
            is_async=args.parallel,
        )
        print(f"Deploying checks with cron schedule: {args.schedule}")
        scheduler = BackgroundScheduler()
        for check_name, check in checks_to_run.items():
            print(f"[CRON JOB - {args.schedule}] {check_name}")
            check = check()
            update_actions(
                check,
                default_check_actions + [ExecutionDatabaseAction],
            )
            scheduler.add_job(
                start_check_deployment,
                CronTrigger.from_crontab(args.schedule),
                id=check_name,
                args=(
                    check,
                    args.parallel,
                ),
            )

        scheduler.start()

        try:
            while True:
                pass
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
    else:
        run_checks(
            checks_to_run=checks_to_run,
            check_actions=default_check_actions,
            is_async=args.parallel,
        )
