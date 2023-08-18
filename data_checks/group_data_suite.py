from data_checks import DataSuite
from data_checks.base.check import Check

"""
Suite of checks that run on a specific pre-defined group of data
"""


class GroupDataSuite(DataSuite):
    @classmethod
    def group_name(cls) -> str:
        """
        Identifier for each element in the group. Can be accessed through self.group_name in checks
        """
        raise NotImplementedError

    @classmethod
    def group(cls) -> list:
        """
        List of group's elements. Each element will be passed to the specified checks
        """
        raise NotImplementedError

    @classmethod
    def group_checks(cls) -> list[type[Check]]:
        """
        Checks to be run on each element in the group. For example:
        [
            CheckClass1,
            CheckClass2,
            ...
        ]
        with group
        [
            element1,
            element2,
            ...
        ]
        will run CheckClass1 on element1, CheckClass1 on element2, CheckClass2 on element1, and CheckClass2 on element2.
        """
        raise NotImplementedError

    @classmethod
    def checks(cls) -> list[Check]:
        """
        Do not override this method. Override group_checks instead.
        """
        group_name = cls.group_name()
        checks = []
        for check in cls.group_checks():
            for element in cls.group():
                updated_check = check()
                updated_check.group = {
                    "name": group_name,
                    "value": element,
                }
                checks.append(updated_check)
        return checks
