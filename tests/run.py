# from .suites.consistency_suite import ConsistencySuite
import asyncio

from tests.src.checks.general_company_check import GeneralCompanyTransactionCheck
from data_checks.conf.data_check_registry import data_check_registry
from data_checks.conf.data_suite_registry import data_suite_registry
from data_checks.conf.settings import settings
from tests.src.suites.consistency_suite import ConsistencySuite

# from tests.src.checks.general_company_check import GeneralCompanyTransactionCheck

# from data_checks.base.actions.suite.main_database_action import MainDatabaseAction
# from data_checks.base.actions.suite.execution_database_action import (
#     ExecutionDatabaseAction,
# )

from data_checks.base.actions.check.main_database_action import MainDatabaseAction
from data_checks.base.actions.check.execution_database_action import (
    ExecutionDatabaseAction,
)

# from data_checks.base.dataset import Dataset
from multiprocessing import freeze_support
import pandas as pd
import os


# print(data_suite_registry)
# print(settings)
# ConsistencySuite().run()
# asyncio.run(ConsistencySuite().run_async())
# asyncio.run(
#     GeneralCompanyTransactionCheck(
#         dataset=Dataset(
#             "Payments Dataset",
#             old_payments_df=pd.read_csv(
#                 os.path.dirname(os.path.realpath(__file__)) + "/old_payments.csv"
#             ),
#             new_payments_df=pd.read_csv(
#                 os.path.dirname(os.path.realpath(__file__)) + "/new_payments.csv"
#             ),
#         )
#     ).run_all_async()
# )

# async def test():
#     runs = await ConsistencySuite().run_async(
#         should_run=False,
#     )
#     await asyncio.gather(*runs)


# asyncio.run(test())
# GeneralCompanyTransactionCheck(
# dataset=Dataset(
#     "Payments Dataset",
#     old_payments_df=pd.read_csv(
#         os.path.dirname(os.path.realpath(__file__)) + "/old_payments.csv"
#     ),
#     new_payments_df=pd.read_csv(
#         os.path.dirname(os.path.realpath(__file__)) + "/new_payments.csv"
#     ),
# )
# ).run_all()
if __name__ == "__main__":
    freeze_support()
    # suite = ConsistencySuite()
    # suite.add_actions(MainDatabaseAction, ExecutionDatabaseAction)
    # suite.run_async()

    check = GeneralCompanyTransactionCheck()
    check.add_actions(MainDatabaseAction)
    check.add_actions(ExecutionDatabaseAction)
    check.run_all_async()
