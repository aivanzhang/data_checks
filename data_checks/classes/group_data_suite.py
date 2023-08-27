import json
from data_checks.classes.data_suite import DataSuite
from data_checks.base.check import Check
from data_checks.conf.data_check_registry import data_check_registry

"""
Suite of checks that run on a specific pre-defined group of data. For instance you might have checks on each Item in the Items table. 
This suite allows you to pass Item item to each check across all Items and checks.
"""


class GroupDataSuite(DataSuite):
    @classmethod
    def group_name(cls) -> str:
        """
        Identifier for each element in the group. Used to access the element
        in checks through self.{group_name}
        """
        raise NotImplementedError

    @classmethod
    def group(cls) -> list:
        """
        List of group's members. Each element will be subject to the specified
        checks. Can be accessed through self.{group_name} in checks
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
        checks = []
        for check in cls.group_checks():
            if isinstance(check, str):
                registered_check = data_check_registry[check]
                if registered_check is None or not issubclass(registered_check, Check):
                    raise ValueError(f"Check {check} is not registered")
                check = data_check_registry[check]

            for element in cls.group():
                check_name = f"{check.__name__}::{cls.group_name()}-{json.dumps(element, default=str)}"
                if isinstance(check, Check):
                    updated_check = check
                else:
                    updated_check = check()
                updated_check.name = check_name
                updated_check._set_additional_properties(
                    {
                        cls.group_name(): element,
                    }
                )
                checks.append(updated_check)
        return checks
