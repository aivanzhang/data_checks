"""
Check class
"""
from typing import Dict, Any
from constants import DEFAULT_RULE_PREFIX
from exceptions import DataCheckException
from utils.class_utils import get_all_methods
import time


class Check:
    def __init__(
        self, name=None, description="", rules_prefix=DEFAULT_RULE_PREFIX, verbose=False
    ):
        """
        Initialize a check object
        """
        self.verbose = verbose
        self.name = self.__class__.__name__ if name is None else name
        self.description = description
        self.rules_prefix = rules_prefix
        self.rules = [
            rule for rule in get_all_methods(self) if rule.startswith(self.rules_prefix)
        ]
        # Stores any metadata generated when a rule runs
        self.rules_context = dict.fromkeys(self.rules, dict())

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

    def start_subrule(self, subrule_name: str, data: Any):
        self.rules_context[subrule_name] = data

    def run(self, rule: str):
        """
        Runs a single rule
        """
        self.before()
        try:
            data = {}
            rule_func = getattr(self, rule)
            rule_func(data)
            self.on_success()
        except AssertionError as e:
            print(e)
            print(self.rules_context)
            self.on_failure(DataCheckException.from_assertion_error(e))
        except DataCheckException as e:
            print(e)
            self.on_failure(e)
        self.after()

    def after(self):
        return

    def run_all(self):
        """
        Run all the rules in the check based off the rules_prefix
        """
        self.setup()
        print(self.name)
        for index, rule in enumerate(self.rules):
            print(f"\t[{index + 1}/{len(self.rules)}] {rule}")
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

    @staticmethod
    def rule(name="", severity=1.0):
        """
        Decorator for a rule function
        """

        def wrapper(rule_func):
            def wrapper_func(self, *args, **kwargs):
                self.rules_context[rule_func.__name__]["severity"] = severity
                self.rules_context[rule_func.__name__]["args"] = args
                self.rules_context[rule_func.__name__]["kwargs"] = kwargs
                return rule_func(self, *args, **kwargs)

            return wrapper_func

        return wrapper

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
