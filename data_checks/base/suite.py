import asyncio
from typing import Iterable, Optional, Awaitable
from data_checks.base.check import Check
from data_checks.base.dataset import Dataset
from data_checks.base.suite_types import SuiteBase
from data_checks.database import SuiteManager, SuiteExecutionManager
from data_checks.utils import class_utils


class Suite(SuiteBase):
    def __init__(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        check_rule_tags: dict[str, Iterable] = {},
    ):
        self.name = self.__class__.__name__ if name is None else name
        self.description = description or ""
        self.check_rule_tags = check_rule_tags
        self._internal = {
            "suite_model": None,
            "suite_execution_model": None,
            "dataset": self.dataset(),
            "checks_config": self.checks_config(),
        }

    @classmethod
    def dataset(cls) -> Dataset | None:
        """
        Get the dataset for the suite
        """
        raise NotImplementedError

    @classmethod
    def checks_overrides(cls) -> dict | None:
        """
        Overrides for rules in checks
        """
        raise NotImplementedError

    @classmethod
    def checks_config(cls) -> dict | None:
        """
        Config shared across checks
        """
        raise NotImplementedError

    @classmethod
    def checks(cls) -> list[type]:
        """
        Checks to be run by the suite
        """
        raise NotImplementedError

    @classmethod
    def get_checks(cls) -> list[Check]:
        checks: list[Check] = []
        checks_overrides = cls.checks_overrides()
        for check in cls.checks():
            overrides = {}
            if checks_overrides is not None:
                overrides = checks_overrides.get(check.__name__, {})

            checks.append(check(rules_params=overrides))
        return checks

    def get_checks_with_tags(self, tags: Optional[Iterable]) -> list[Check]:
        """
        Get checks for a given set of tags
        """
        if tags is None:
            return self.get_checks()
        else:
            return [
                check
                for check in self.get_checks()
                if set(tags).intersection(check.tags)
            ]

    def setup(self):
        """
        One time setup for all checks in the suites
        """
        self._internal["suite_model"] = SuiteManager.create_suite(
            name=self.name,
            description=self.description,
            code=class_utils.get_class_code(self.__class__),
        )
        self._internal[
            "suite_execution_model"
        ] = SuiteExecutionManager.create_suite_execution(
            suite=self._internal["suite_model"],
            status="running",
        )

    def before(self, check: Check):
        """
        Run before each check
        """
        check._update_from_suite_internals(self._internal)

    def run(self, check_tags: Optional[Iterable] = None):
        self.setup()

        checks_to_run = self.get_checks_with_tags(check_tags)
        for index, check in enumerate(checks_to_run):
            print(f"[{index + 1}/{len(checks_to_run)} Checks] {check}")
            self.before(check)
            try:
                check.run_all(tags=self.check_rule_tags.get(check.name, None))
                self.on_success(check)
            except Exception as e:
                self.on_failure(e)
            self.after(check)

        self.teardown()

    async def _exec_async_check(self, check: Check):
        """
        Execute a check
        """
        self.before(check)
        try:
            await check.run_all_async(tags=self.check_rule_tags.get(check.name, None))
            self.on_success(check)
        except Exception as e:
            self.on_failure(e)
        self.after(check)

    def _generate_async_check_runs(
        self, check_tags: Optional[Iterable] = None
    ) -> list[Awaitable]:
        """
        Generate a list of coroutines that can be awaited
        """
        return [
            self._exec_async_check(check)
            for check in self.get_checks_with_tags(check_tags)
        ]

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
            return self._generate_async_check_runs(check_tags)

        self.setup()
        await asyncio.gather(
            *[
                self._exec_async_check(check)
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
        suite_execution = self._internal["suite_execution_model"]

        if suite_execution:
            SuiteExecutionManager.update_execution(
                suite_execution.id,
                status="success",
            )

    def get_all_metadata(self):
        """
        Get all metadata from all checks
        """

        suite_metadata = dict()
        for check in self.get_checks():
            suite_metadata[check.name] = check.metadata.copy()
        return suite_metadata
