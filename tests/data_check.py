from data_checks.rule import rule, rule_func
from data_checks.check import Check
import os
import uuid
import pandas as pd
import time
import asyncio
from google.cloud import storage
from google.cloud.storage.bucket import Bucket
from google.cloud.storage.blob import Blob
from google.oauth2 import service_account


def clean_df_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean dataframe column names by: convering to lowercase, removing whitespace, replacing special characters with '_'.
    """
    columns = []
    special_chars = [
        "~",
        ":",
        "'",
        "+",
        "[",
        "\\",
        "@",
        "^",
        "{",
        "%",
        "(",
        "-",
        '"',
        "*",
        "|",
        ",",
        "&",
        "<",
        "`",
        "}",
        ".",
        "_",
        "=",
        "]",
        "!",
        ">",
        ";",
        "?",
        "#",
        "$",
        ")",
        "/",
        " ",
    ]

    for column in df.columns:
        if isinstance(column, str):
            column = column.lower().strip()
            for char in special_chars:
                column = column.replace(char, "_")
            column = "_".join([_ for _ in column.split("_") if _ != ""])

        columns.append(column)

    df.columns = columns
    return df


def get_spend() -> pd.DataFrame:
    """
    Get spend data from GCS bucket.
    """

    dir_path = os.path.dirname(os.path.realpath(__file__))
    GOOGLE_AUTH_SERVICE_ACCOUNT_FILE = os.path.join(
        dir_path, "random-392921-e440758499f0.json"
    )
    credentials = service_account.Credentials.from_service_account_file(
        GOOGLE_AUTH_SERVICE_ACCOUNT_FILE,
        scopes=[
            "https://www.googleapis.com/auth/devstorage.read_write",
        ],
    )
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.get_bucket("data_checks_data")
    file_name = "spend.xlsx"
    blob: storage.Blob = bucket.blob(file_name)
    tmp_path = f"/tmp/{uuid.uuid4().hex}_{file_name}"

    with open(tmp_path, "wb") as f:
        blob.download_to_file(f)

    df = pd.DataFrame()
    if (
        tmp_path.endswith(".csv")
        or tmp_path.endswith(".zip")
        or tmp_path.endswith(".gz")
    ):
        df = pd.read_csv(tmp_path)
    if (
        tmp_path.endswith(".xlsx")
        or tmp_path.endswith(".xls")
        or tmp_path.endswith(".xlsm")
    ):
        df = pd.read_excel(tmp_path)

    df = clean_df_columns(df)
    os.remove(tmp_path)
    return df


def test():
    @rule_func()
    def rule_check_spend_not_empty(a=1, b=1):
        print(a, b)

    rule_check_spend_not_empty()


class CompanyRevenueCheck(Check):
    def __init__(self, name: str):
        super().__init__(name)
        self.rules_params = {
            "rule_check_spend_not_empty": lambda: [
                {"args": (), "kwargs": {"company_id": 1}},
                {"args": (), "kwargs": {"company_id": 2}},
            ]
        }
        self.rules_prefix = "rule_"
        self.tags = {1, 2}

    def setup(self):
        print("Starting CompanyRevenueCheck setup")
        time.sleep(1)
        print("Finished CompanyRevenueCheck setup")

    @rule(tags=[1])
    def rule_check_spend_not_empty(self, company_id=1):
        df = get_spend()
        print(company_id)
        time.sleep(1)
        self.log_metadata(
            {"spend": df},
            write_to_file="/Users/ivanzhang/Desktop/data-checks/tests/metadata/metadata.json",
        )
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


# print(CompanyRevenueCheck(name="CompanyRevenueCheck - Amazon").run_all())
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
