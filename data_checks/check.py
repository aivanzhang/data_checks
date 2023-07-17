"""
Check class
"""
from typing import Dict, Any
from constants import DEFAULT_RULE_PREFIX
from data_exceptions import DataCheckException
from utils.class_utils import get_all_methods
import time


class Check:
    def __init__(self, name=None, description="", checks_prefix=DEFAULT_RULE_PREFIX):
        """
        Initialize a check object
        """
        self.name = self.__class__.__name__ if name is None else name
        self.description = description
        self.checks_prefix = checks_prefix
        # Stores any metadata generated when a rule runs
        self.rules_context: Dict[str, Any] = dict()

    @classmethod
    def init(cls, file_path: str) -> "Check":
        """
        Initialize a check from a JSON file
        """
        return cls()

    def setup(self):
        """
        One time setup for all rules in the check
        """
        return

    def before(self):
        """
        Run before each rule
        """
        return

    def ingest_from(self, source: str):
        return

    def run(self, rule: str):
        """
        Runs a single rule
        """
        try:
            self.before()
            rule_func = getattr(self, rule)
            rule_func()
            self.on_success()
        except DataCheckException as e:
            print(e)
            self.on_failure(e)
        self.after()

    def after(self):
        return

    def run_all(self):
        """
        Run all the rules in the check based off the checks_prefix
        """
        self.setup()
        rules = [
            rule
            for rule in get_all_methods(self)
            if rule.startswith(self.checks_prefix)
        ]
        print(self.name)
        for index, rule in enumerate(rules):
            print(f"\t[{index + 1}/{len(rules)}] {rule}")
            start_time = time.time()
            self.run(rule)
            print(f"\t{time.time() - start_time:.2f} seconds")
        self.teardown()

    def on_success(self):
        """
        Called when a rule succeeds
        """
        return

    def on_failure(self, exception: DataCheckException):
        """
        Called when a rule fails
        """
        return

    def teardown(self):
        """
        One time teardown after all rules are run
        """
        return

    def save_to_file(self, file_path: str):
        """
        Save the check to a file
        """
        return

    def __repr__(self):
        return f"<{self.name}>"


"""

check_prefix = "rule_"
ingestor_prefix = "ingest_"

@ingestor("ingestor name")
def ingest_template():

@rule("rule name", "rule description")
def rule_template():

Go from notebook to check
Download and store locally
"""
