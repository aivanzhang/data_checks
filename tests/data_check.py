import sys

sys.path.append("./src")
from data_checks.rule import rule, rule_func
from data_checks.check import Check
import os
import uuid
import pandas as pd
import time
import asyncio


def get_spend():
    return pd.DataFrame()


def test():
    @rule_func()
    def rule_check_spend_not_empty(a=1, b=1):
        print(a, b)

    rule_check_spend_not_empty()


class CompanyRevenueCheck(Check):
    def __init__(self, name: str):
        super().__init__(name)
        self.rules_params = {
            "rule_check_spend_not_empty": [
                {"args": (1,), "kwargs": {}},
                {"args": (2,), "kwargs": {}},
            ]
        }
        # self.rules_prefix = "rule_"
        self.tags = {1, 2}

    def setup(self):
        print("Starting CompanyRevenueCheck setup")
        time.sleep(1)
        print("Finished CompanyRevenueCheck setup")

    @rule(name="Spend Not Empty", tags=[1])
    def rule_check_spend_not_empty(self, company_id):
        df = get_spend()
        print(company_id)
        time.sleep(1)
        # self.log_metadata(
        #     {"spend": df},
        #     write_to_file="/Users/ivanzhang/Desktop/data-checks/tests/metadata/metadata.json",
        # )
        assert len(df) < 0, "Spend data is empty 1"

    @rule(tags=[2])
    def rule_check_spend_not_empty_1(a=2, b=2):
        df = get_spend()
        # print(a, b)
        # self.log_metadata({"spend": df})
        assert len(df) < 0, "Spend data is empty 2"

    @rule(tags=[2])
    def rule_check_spend_not_empty_2(self, a=3, b=3):
        df = get_spend()
        # print(a, b)
        # self.log_metadata({"spend": df})
        assert len(df) < 0, "Spend data is empty 3"

    def after(self, rule: str, params):
        print(rule, self.rules_context)
        return super().after(rule, params)

    def on_failure(self, exception):
        return

    def teardown(self):
        print("Starting CompanyRevenueCheck teardown")
        time.sleep(1)
        print("Finished CompanyRevenueCheck teardown")


class CompanyRevenueCheck2(Check):
    def __init__(self, name: str):
        super().__init__(name)
        self.rules_params = {}
        self.rules_prefix = "rule_"
        self.tags = {2, 3}

    def setup(self):
        print("Starting CompanyRevenueCheck2 setup")
        time.sleep(1)
        print("Finished CompanyRevenueCheck2 setup")

    @rule(tags=[2])
    def rule_check_spend_not_empty_2(self):
        df = get_spend()
        print("HI")
        # print(a, b)
        # self.log_metadata({"spend": df})
        assert len(df) < 0, "Spend data is empty"

    def on_failure(self, exception):
        return

    def teardown(self):
        print("Starting CompanyRevenueCheck2 teardown")
        time.sleep(1)
        print("Finished CompanyRevenueCheck2 teardown")


print(CompanyRevenueCheck(name="CompanyRevenueCheck - Amazon").run_all(tags=[1]))
# CompanyRevenueCheck(name="CompanyRevenueCheck - Amazon").run(
#     "rule_check_spend_not_empty"
# )


# async def test():
#     await asyncio.gather(
#         CompanyRevenueCheck(name="CompanyRevenueCheck - Amazon").run_all_async(
#             # should_run=False,
#             tags=[1],
#         )
#     )


# print(asyncio.run(test()))
# print(asyncio.run(test()))
# print(
#     CompanyRevenueCheck(name="CompanyRevenueCheck - Amazon").log_metadata(
#         {"a": 1}, id="abc"
#     )
# )
