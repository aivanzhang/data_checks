import asyncio
from typing import Iterable, Optional, Awaitable
from check import Check
from suite_types import SuiteBase


class Suite(SuiteBase):
    def __init__(
        self, name, checks: list[Check], check_rule_tags: dict[str, Iterable[str]] = {}
    ):
        self.name = name
        self.checks = checks
        self.check_rule_tags = check_rule_tags

    def get_checks_with_tags(self, tags: Optional[Iterable[str]]) -> list[Check]:
        """
        Get checks for a given set of tags
        """
        if tags is None:
            return self.checks
        else:
            return [
                check for check in self.checks if set(tags).intersection(check.tags)
            ]

    def setup(self):
        """
        One time setup for all checks in the suites
        """
        return

    def before(self, check: Check):
        """
        Run before each check
        """
        return

    def run(self, check_tags: Optional[Iterable[str]] = None):
        self.setup()

        checks_to_run = self.get_checks_with_tags(check_tags)
        for index, check in enumerate(checks_to_run):
            print(f"\t[{index + 1}/{len(checks_to_run)}] {check}")
            try:
                self.before(check)
                check.run_all(tags=self.check_rule_tags.get(check.name, None))
                self.on_success(check)
            except Exception as e:
                self.on_failure(e)

        self.teardown()

    def _generate_async_check_runs(
        self, check_tags: Optional[Iterable] = None
    ) -> list[Awaitable]:
        """
        Generate a list of coroutines that can be awaited
        """
        return [
            check.run_all_async(
                tags=self.check_rule_tags.get(check.name, None), should_run=False
            )
            for check in self.get_checks_with_tags(check_tags)
        ]

    async def run_async(
        self, check_tags: Optional[str] = None, should_run: bool = True
    ):
        self.setup()
        if not should_run:
            return self._generate_async_check_runs(check_tags)

        self.setup()
        await asyncio.gather(*self._generate_async_check_runs(check_tags))
        self.teardown()

    def after(self, check: Check):
        """
        Runs after each check
        """
        return

    def on_success(self, check: Check):
        """
        Called when a rule succeeds
        """
        pass

    def on_failure(self, exception: Exception):
        """
        Called when a rule fails
        """
        raise exception

    def teardown(self):
        """
        One time teardown after all checks are run
        """
        return

    def get_all_metadata(self):
        """
        Get all metadata from all checks
        """

        suite_metadata = dict()
        for check in self.checks:
            suite_metadata[check.name] = check.metadata.copy()
        return suite_metadata
