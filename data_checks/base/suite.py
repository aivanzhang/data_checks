from typing import Iterable, Optional, TypedDict
import time
from multiprocessing import Process
from data_checks.conf.data_check_registry import data_check_registry
from data_checks.base.check import Check
from data_checks.base.dataset import Dataset
from data_checks.base.suite_types import SuiteBase
from data_checks.base.exceptions import SkipExecutionException
from data_checks.base.mixins.action_mixin import ActionMixin
from data_checks.base.actions.execution_context import ExecutionContext
from data_checks.base.actions.check import CheckAction
from data_checks.base.actions.suite import (
    SuiteAction,
    SetupCheckActionsAction,
    SetupDatasetAction,
)


class CheckActions(TypedDict):
    default: list[type[CheckAction]]
    checks: dict[type[Check], list[type[CheckAction]]]


class Suite(SuiteBase, ActionMixin):
    DEFAULT_ACTIONS: list[type[SuiteAction]] = [
        SetupCheckActionsAction,
        SetupDatasetAction,
    ]

    def __init__(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        actions: list[type[SuiteAction]] = [],
    ):
        self.name = self.__class__.__name__ if name is None else name
        self.description = description or ""
        self._actions: list[type[SuiteAction]] = actions
        self.check_actions: CheckActions = {
            "default": [],
            "checks": {},
        }
        self._internal = {
            "suite_model": None,
            "dataset": None,
        }

    @property
    def actions(self) -> list[type[SuiteAction]]:
        return self.DEFAULT_ACTIONS + self._actions

    @actions.setter
    def actions(self, actions: list[type[SuiteAction]]):
        self._actions = actions

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
    def suite_config(cls) -> dict:
        """
        System configurations for the suite. In the following format:
        {
            "schedule": CRON_STRING, # cron schedule for the suite
        }
        """
        return {}

    @classmethod
    def checks(cls) -> list[type | str | Check]:
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
                check_name: str
                if isinstance(check, str):
                    check_name = check
                elif isinstance(check, type):
                    check_name = check.__name__
                else:
                    check_name = check.name
                overrides = checks_overrides.get(check_name, {})
            if isinstance(check, str):
                checks.append(
                    data_check_registry[check](
                        rules_params=overrides,
                    )
                )
            elif isinstance(check, Check):
                check.rules_params = overrides
                checks.append(check)
            elif issubclass(check, Check):
                checks.append(
                    check(
                        rules_params=overrides,
                    )
                )

        return checks

    def set_actions(self, actions: list[type[SuiteAction]]):
        self.actions = actions

    def set_check_actions(self, check_actions: CheckActions):
        self.check_actions = check_actions

    def run(self):
        self.setup()
        checks_to_run = self.get_checks()
        for index, check in enumerate(checks_to_run):
            print(f"[{index + 1}/{len(checks_to_run)} Checks] {check}")
            context = ExecutionContext()
            context.set_sys("check", check)
            try:
                self.before(context)
            except SkipExecutionException as e:
                return
            try:
                start_time = time.time()
                check.run_all()
                print(f"{check} finished in {time.time() - start_time} seconds")
                self.on_success(context)
            except Exception as e:
                context.set_sys("exception", e)
                self.on_failure(context)
            self.after(context)

        self.teardown()

    def run_async(self):
        """
        Run all checks in the suite asynchronously. Note that order of execution is not guaranteed (aside from setup and teardown).
        """
        checks = self.get_checks()
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

    def _exec_async_check(self, check: Check):
        """
        Execute a check
        """
        context = ExecutionContext()
        context.set_sys("check", check)
        try:
            self.before(context)
        except SkipExecutionException as e:
            return
        try:
            start_time = time.time()
            check.run_all_async()
            print(f"{check} finished in {time.time() - start_time} seconds")
            self.on_success(context)
        except Exception as e:
            context.set_sys("exception", e)
            self.on_failure(context)
        self.after(context)
