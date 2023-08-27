# Path: CHECKS_MODULE/my_first_data_check.py
from data_checks.classes.data_check import DataCheck


class MyFirstDataCheck(DataCheck):
    def setup(self):
        """
        Setup the check. Use this to load data, initialize models, etc.
        """
        super().setup()  # DON'T FORGET TO CALL SUPER
        self.content = "Apple"

    def rule_my_first_successful_rule(self, data="Hello World"):
        # Call functions to check the data
        assert data == "Hello World"

    def rule_my_first_failed_rule(self):
        # Call functions to check the data
        # Throw an exception if the rule fails
        assert False

    def my_first_helper_function(self):
        # This function will not be run as a rule
        raise Exception("This function will not be run as a rule")
