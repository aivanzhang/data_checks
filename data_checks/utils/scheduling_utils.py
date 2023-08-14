from apscheduler.schedulers.background import BackgroundScheduler
from data_checks import DataSuite


def deploy_scheduled_suites():
    # Get list of scheduled suites

    # For each suite, get the checks to run
    # For each check, get the rules to run
    # For each rule, schedule the rule to run
    scheduler = BackgroundScheduler()
    scheduler.add_job(suite.run, "cron", minute="*")  # Schedule to run every minute

    scheduler.start()

    try:
        # Keep the program running to allow the scheduler to execute the jobs
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        # Shut down the scheduler gracefully when the program is interrupted
        scheduler.shutdown()
