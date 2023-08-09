import os


def init_database(database_url: str):
    """
    Initializes the database to store suite and check results and executions
    """
    os.environ["CHECKS_DATABASE_URL"] = database_url


def init_check_dir(check_dir: str):
    """
    Initializes the directory to store user defined checks
    """
    os.environ["CHECK_DIR"] = check_dir


def init_suite_dir(suite_dir: str):
    """
    Initializes the directory to store user defined suites
    """
    os.environ["SUITE_DIR"] = suite_dir


def init(database_url: str, check_dir: str, suite_dir: str):
    """
    Initializes the database, check directory, and suite directory
    """
    init_database(database_url)
    init_check_dir(check_dir)
    init_suite_dir(suite_dir)
