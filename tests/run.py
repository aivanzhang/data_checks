# from .suites.consistency_suite import ConsistencySuite
import asyncio

# from tests.src.checks.general_company_check import GeneralCompanyTransactionCheck
from data_checks.conf.check_registry import check_registry
from data_checks.conf.settings import settings
from tests.src.suites.consistency_suite import ConsistencySuite

# from data_checks.base.dataset import Dataset
import pandas as pd
import os
from data_checks.utils import rule_utils


print(check_registry)
print(settings)
ConsistencySuite().run()
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
