from data_checks import DataSuite
from data_checks.base.check import Check
from data_checks.base.check_types import Group
from data_checks.conf.data_check_registry import data_check_registry

"""
Suite of checks that run on a specific pre-defined group of data. For instance you might have checks on each Item in the Items table. 
This suite allows you to pass Item item to each check across all Items and checks.
"""


class GroupDataSuite(DataSuite):
    @classmethod
    def group_name(cls) -> str:
        """
        Identifier for each element in the group. Can be accessed through self.group["name"] in checks.
        """
        raise NotImplementedError

    @classmethod
    def group(cls) -> list:
        """
        List of group's elements. Each element will be passed to the specified checks. Can be accessed through self.group["value"] in checks
        """
        raise NotImplementedError

    @classmethod
    def group_checks(cls) -> list[type[Check] | str | Check]:
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
            if isinstance(check, str):
                registered_check = data_check_registry[check]
                if registered_check is None or not issubclass(registered_check, Check):
                    raise ValueError(f"Check {check} is not registered")
                check = data_check_registry[check]

            for element in cls.group():
                if isinstance(check, Check):
                    updated_check = check
                else:
                    updated_check = check()
                group: Group = {
                    "name": group_name,
                    "value": element,
                }
                updated_check.group = group
                checks.append(updated_check)
        return checks
