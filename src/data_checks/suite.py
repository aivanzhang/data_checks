import asyncio
from typing import Iterable, Optional
from .check import Check
from .suite_types import SuiteBase


class Suite(SuiteBase):
    def __init__(
        self,
        name: Optional[str] = None,
        checks: list[Check] = [],
        check_rule_tags: dict[str, Iterable] = {},
    ):
        self.name = self.__class__.__name__ if name is None else name
        self.checks = checks
        self.check_rule_tags = check_rule_tags

    def get_checks_with_tags(self, tags: Optional[Iterable]) -> list[Check]:
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

    def run(self, check_tags: Optional[Iterable] = None):
        self.setup()

        checks_to_run = self.get_checks_with_tags(check_tags)
        for index, check in enumerate(checks_to_run):
            print(f"[{index + 1}/{len(checks_to_run)} Checks] {check}")
            try:
                self.before(check)
                check.run_all(tags=self.check_rule_tags.get(check.name, None))
                self.on_success(check)
            except Exception as e:
                self.on_failure(e)
            self.after(check)

        self.teardown()

    async def run_async(
        self, check_tags: Optional[Iterable] = None, should_run: bool = True
    ):
        """
        Run all checks in the suite asynchronously. Note that order of execution is not guaranteed (aside from setup and teardown).
        Parameters:
            check_tags: Tags to filter checks by
            should_run: If False, will only generate async check runs that can be awaited. Skips setup and teardown.
        """
        if not should_run:
            return [
                check._generate_async_rule_runs(
                    tags=self.check_rule_tags.get(check.name, None)
                )
                for check in self.get_checks_with_tags(check_tags)
            ]

        self.setup()
        await asyncio.gather(
            *[
                check.run_all_async(tags=self.check_rule_tags.get(check.name, None))
                for check in self.get_checks_with_tags(check_tags)
            ]
        )
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
