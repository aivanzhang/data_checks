from constants import DEFAULT_CHECK_PREFIX


class Check:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.checks_prefix = DEFAULT_CHECK_PREFIX

    def setup(self):
        return

    def ingest(self):
        raise NotImplementedError

    def before(self):
        return

    def run(self):
        try:
            assert self.ingest()
            # raise NotImplementedError
        except AssertionError:
            self.on_failure()
            return
        self.on_success()

    def after(self):
        return

    def run_all(self):
        try:
            assert self.ingest()
            # raise NotImplementedError
        except AssertionError:
            self.on_failure()
            return
        self.on_success()

    def on_success(self):
        return

    def on_failure(self):
        return

    def teardown(self):
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
