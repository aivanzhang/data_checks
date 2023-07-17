"""
Check class
"""
from constants import DEFAULT_RULE_PREFIX
from utils.class_utils import get_all_methods


class Check:
    def __init__(self, name="", description="", checks_prefix=DEFAULT_RULE_PREFIX):
        """
        Initialize a check object
        """
        self.name = f"{self.__class__.__name__}: {name}"
        self.description = description
        self.checks_prefix = checks_prefix

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

    def run(self, rule: str):
        """
        Runs a single rule
        """
        try:
            # Run the rule
            self.on_success()
            return
        except AssertionError as e:
            self.on_failure()
            return

    def after(self):
        return

    def run_all(self):
        """
        Run all the rules in the check based off the checks_prefix
        """
        print(self.name)
        rules = [
            rule
            for rule in get_all_methods(self)
            if rule.startswith(self.checks_prefix)
        ]

        for index, rule in enumerate(rules):
            print(f"{rule} ({index + 1}/{len(rules)})")
            rule_func = getattr(self, rule)
            self.run(rule_func)

        return

    def on_success(self):
        """
        Called when a rule succeeds
        """
        return

    def on_failure(self):
        """
        Called when a rule fails
        """
        return

    def teardown(self):
        """
        One time teardown after all rules are run
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
