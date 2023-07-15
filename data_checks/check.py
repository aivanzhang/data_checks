from constants import DEFAULT_RULE_PREFIX


class Check:
    def __init__(self, name, description):
        """
        Initialize a check object
        """
        self.name = name
        self.description = description
        self.checks_prefix = DEFAULT_RULE_PREFIX

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
        Run all the rules in the check
        """
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
"""
