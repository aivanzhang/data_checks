"""
This module contains utility functions for running data checks and used in the __main__.py.
"""
from data_checks.data_suite import DataSuite


def run_suites_async(suites: list[type[DataSuite]]):
    import asyncio

    loop = asyncio.get_event_loop()

    async def run_suite_async(index: int, suite: type[DataSuite]):
        suite_obj = suite()
        print(f"[{index}/{len(suites)} Suites] {suite_obj.name}")
        await suite_obj.run_async()

    loop.run_until_complete(
        asyncio.gather(
            *[run_suite_async(index, suite) for index, suite in enumerate(suites, 1)]
        )
    )
