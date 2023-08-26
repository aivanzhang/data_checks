import pandas as pd
from data_checks.group_data_suite import GroupDataSuite
from examples.operations.inventory.item import Item


class InventorySuite(GroupDataSuite):
    @classmethod
    def group_name(cls) -> str:
        """
        Identifier for each element in the group. Used to access the element
        in checks through self.{group_name}
        """
        return "item"

    @classmethod
    def group(cls) -> list:
        """
        List of group's members. Each element will be subject to the specified
        checks. Can be accessed through self.{group_name} in checks
        """
        items_df = pd.read_csv("examples/operations/inventory/data.csv")

        return [Item(**kwargs) for kwargs in items_df.to_dict(orient="records")]

    @classmethod
    def group_checks(cls):
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
        will run CheckClass1 on element1, CheckClass1 on element2,
        CheckClass2 on element1, and CheckClass2 on element2.
        """
        return ["ItemCheck"]

    @classmethod
    def suite_config(cls) -> dict:
        return {
            "schedule": "* * * * *",
        }