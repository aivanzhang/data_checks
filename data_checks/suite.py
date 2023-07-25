class CheckSuite:
    def __init__(self, name, checks):
        self.name = name
        self.checks = checks

    # def run(self):
    #     print(f"Running {self.name}...")
    #     for check in self.checks:
    #         check.run()
    #     print(f"Finished {self.name}.")


"""
TODO
- Add a run method to the CheckSuite class that runs all the checks in the suite (with specific tags)
- running sync and async
- before and after methods for the CheckSuite class
- setup and teardown methods for the CheckSuite class
- aggregating all relevant check data after running the suite
"""
