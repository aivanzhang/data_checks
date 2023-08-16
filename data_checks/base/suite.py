from typing import Iterable, Optional
import time
from multiprocessing import Process
from data_checks.base.check import Check
from data_checks.base.dataset import Dataset
from data_checks.base.suite_types import SuiteBase
from data_checks.conf.data_check_registry import data_check_registry
from data_checks.base.mixins.action_mixin import ActionMixin
from data_checks.base.actions.suite import SuiteAction


class Suite(SuiteBase, ActionMixin):
    def __init__(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        self.name = self.__class__.__name__ if name is None else name
        self.description = description or ""
        self._internal = {
            "suite_model": None,
            "suite_execution_model": None,
            "dataset": None,
            "checks_config": None,
        }
        self.actions: list[type[SuiteAction]] = []

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
        Shared fields across checks
        """
        raise NotImplementedError

    @classmethod
    def suite_config(cls) -> dict:
        """
        System configurations for the suite. In the following format:
        {
            "schedules": { # Overrides for check schedules
                "CheckClass": "0 8 * * *", # Overrides the schedule for CheckClass and all its rules
                "CheckClass1": {
                    "rule_1": "0 8 * * *", # Overrides the schedule for rule_1 in CheckClass1
                    ...
                },
                ...
            }
        }
        """
        return {}

    @classmethod
    def checks(cls) -> list[type | str]:
        """
        Checks to be run by the suite
        """
        raise NotImplementedError

    def get_checks(self) -> list[Check]:
        checks: list[Check] = []
        checks_overrides = self.checks_overrides()
        for check in self.checks():
            overrides = {}
            if checks_overrides is not None:
                overrides = checks_overrides.get(
                    check if isinstance(check, str) else check.__name__, {}
                )
            if isinstance(check, str):
                checks.append(
                    data_check_registry[check](
                        rules_params=overrides,
                    )
                )
            elif issubclass(check, Check):
                checks.append(
                    check(
                        rules_params=overrides,
                    )
                )

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

    def run(self, check_tags: Optional[Iterable] = None):
        self.setup()

        checks_to_run = self.get_checks_with_tags(check_tags)
        for index, check in enumerate(checks_to_run):
            print(f"[{index + 1}/{len(checks_to_run)} Checks] {check}")
            context: dict = {
                "check": check,
            }
            self.before(context)
            try:
                start_time = time.time()
                check.run_all()
                print(f"{check} finished in {time.time() - start_time} seconds")
                self.on_success(context)
            except Exception as e:
                context["exception"] = e
                self.on_failure(context)
            self.after(context)

        self.teardown()

    def run_async(self, check_tags: Optional[Iterable] = None):
        """
        Run all checks in the suite asynchronously. Note that order of execution is not guaranteed (aside from setup and teardown).
        Parameters:
            check_tags: Tags to filter checks by
        """
        checks = self.get_checks_with_tags(check_tags)
        running_check_processes = []
        self.setup()

        for index, check in enumerate(checks):
            print(f"[{index + 1}/{len(checks)} Checks] ASYNC RUN {check}")
            process = Process(target=self._exec_async_check, args=(check,))
            process.start()
            running_check_processes.append(process)

        for process in running_check_processes:
            process.join()

        self.teardown()

    def get_all_metadata(self):
        """
        Get all metadata from all checks
        """

        suite_metadata = dict()
        for check in self.get_checks():
            suite_metadata[check.name] = check.metadata.copy()
        return suite_metadata

    def _exec_async_check(self, check: Check):
        """
        Execute a check
        """
        context: dict = {
            "check": check,
        }
        self.before(context)
        try:
            start_time = time.time()
            check.run_all_async()
            print(f"{check} finished in {time.time() - start_time} seconds")
            self.on_success(context)
        except Exception as e:
            context["exception"] = e
            self.on_failure(context)
        self.after(context)
