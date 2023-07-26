from data_checks.suite import Suite
from data_check import CompanyRevenueCheck, CompanyRevenueCheck2
import asyncio
import time


class CompanySuite(Suite):
    def __init__(self, name):
        self.name = name
        self.checks = [
            CompanyRevenueCheck(name="CompanyRevenueCheck"),
            CompanyRevenueCheck2(name="CompanyRevenueCheck2"),
        ]
        super().__init__(name, self.checks)
        self.check_rule_tags = {"CompanyRevenueCheck": [2]}

    def setup(self):
        print("Starting setup")
        time.sleep(1)
        print("Finished setup")

    def teardown(self):
        print("Starting teardown")
        time.sleep(1)
        print("Finished teardown")


cs = CompanySuite("CVF")


# print(cs.run(check_tags=[1]))
# async def test():
#     await asyncio.gather(cs.run_async(check_tags=[1], should_run=False))


# print(asyncio.run(cs.run_async(check_tags=[2])))
