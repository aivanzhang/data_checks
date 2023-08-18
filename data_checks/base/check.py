"""
Check class
"""
import copy
import sys
import time
from typing import Iterable, Optional, Callable
from multiprocessing import Process
from data_checks.base.exceptions import DataCheckException, SkipExecutionException
from data_checks.base.check_types import FunctionArgs, CheckBase, Group
from data_checks.base.suite_helper_types import SuiteInternal
from data_checks.base.dataset import Dataset
from data_checks.base.mixins.metadata_mixin import MetadataMixin
from data_checks.base.mixins.action_mixin import ActionMixin
from data_checks.utils import class_utils, check_utils
from data_checks.base.actions.check import CheckAction


class Check(CheckBase, MetadataMixin, ActionMixin):
    DEFAULT_ACTIONS: list[type[CheckAction]] = []

    def __init__(
        self,
        name: Optional[str] = None,
        metadata_dir: Optional[str] = None,
        description="",
        rules_params=dict(),
        excluded_rules: Iterable = [],
        tags: Iterable = [],
        actions: list[type[CheckAction]] = [],
        verbose=False,
        group: Optional[Group] = None,
        dataset: Optional[Dataset] = None,
        only_run_specified_rules=False,
    ):
        """
        Initialize a check object
        """
        super().__init__()
        self.verbose = verbose
        self.name = self.__class__.__name__ if name is None else name
        if dataset is not None:
            self.dataset = dataset
        self.description = description
        self.excluded_rules = set(excluded_rules)
        self.tags = set(tags)
        self._internal = {
            "suite_model": None,
            "check_model": None,
        }
        self.set_metadata_dir(metadata_dir)
        self._actions: list[type[CheckAction]] = actions
        self.rules = dict()
        self.rules_params = rules_params
        self.group = group

        self._set_rules(self.defined_rules())
        if only_run_specified_rules:
            self.only_run_specified_rules()

    @property
    def actions(self) -> list[type[CheckAction]]:
        return self.DEFAULT_ACTIONS + self._actions

    @actions.setter
    def actions(self, actions: list[type[CheckAction]]):
        self._actions = actions

    @classmethod
    def defined_rules(cls) -> list[str]:
        """
        Generate rules based off of the decorator and rules_prefix
        """
        return list(
            filter(
                lambda method_name: getattr(
                    getattr(cls, method_name), "is_rule", False
                ),
                class_utils.get_all_methods(cls()),
            )
        )

    def set_actions(self, actions: list[type[CheckAction]]):
        """
        Set the actions for the check
        """
        self.actions = actions

    def only_run_specified_rules(self):
        """
        Appends to self.exclude_rules so that only rules in self.rules_params.keys() are run
        """
        self.excluded_rules = self.excluded_rules.union(
            set(self.rules.keys()) - set(self.rules_params.keys())
        )

    def use_dataset(self, dataset: Dataset):
        """
        Sets the dataset for the check
        """
        self.dataset = dataset

    def get_rules_to_run(self) -> set[str]:
        """
        Find rules and exclude certain rules
        """
        return set(
            [rule for rule in self.rules.keys() if rule not in self.excluded_rules]
        )

    def run(self, rule: str):
        """
        Runs a rule once with one set of params or multiple times with multiple sets of params
        """
        rule_func = self.rules[rule]
        rules_params = self._get_rules_params(rule)
        for params in rules_params:
            self._exec_rule(rule, rule_func, params)

    def run_async(self, rule: str, wait_for_completion=True) -> list[Process]:
        """
        Asynchronously runs a rule once with one set of params or multiple times with multiple sets of params
        """
        rule_func = self.rules[rule]
        rules_params = self._get_rules_params(rule)

        running_rule_processes = []
        for params in rules_params:
            process = Process(target=self._exec_rule, args=(rule, rule_func, params))
            process.start()
            running_rule_processes.append(process)

        if wait_for_completion:
            for process in running_rule_processes:
                process.join()
            return []
        else:
            return running_rule_processes

    def run_all(self):
        """
        Run all the rules in the check
        """
        self.setup()

        rules_to_run = self.get_rules_to_run()

        for index, rule in enumerate(rules_to_run):
            print(f"\t[{index + 1}/{len(rules_to_run)} Rules] {rule}")
            self.run(rule)

        self.teardown()

    def run_all_async(self):
        """
        Run all the rules in the check asynchronously. Note that order of execution is not guaranteed (aside from setup and teardown).
        """

        self.setup()
        rules_to_run = self.get_rules_to_run()
        running_rule_processes: list[tuple[str, list[Process]]] = []
        for index, rule in enumerate(rules_to_run):
            print(f"\t[{index + 1}/{len(rules_to_run)} Rules] ASYNC RUN {rule}")
            running_rule_processes.append(
                (rule, self.run_async(rule, wait_for_completion=False))
            )

        for rule, processes in running_rule_processes:
            for process in processes:
                process.join()

        # await asyncio.gather(*self._generate_async_rule_runs(tags))
        self.teardown()

    def __str__(self):
        return self.name

    def _exec_rule(
        self, rule: str, rule_func: Callable[..., None], params: FunctionArgs
    ):
        """
        Execute a rule
        """
        rule_metadata = {"rule": rule, "params": params}
        context = copy.deepcopy(rule_metadata)

        try:
            self.before(context)
        except SkipExecutionException as e:
            return

        try:
            start_time = time.time()
            rule_func(*params["args"], **params["kwargs"])
            print(f"\t\t{rule} took {time.time() - start_time} seconds")
            self.on_success(context)
        except AssertionError as e:
            print(e)
            context["exception"] = DataCheckException.from_assertion_exception(
                e, metadata=rule_metadata
            )
            self.on_failure(
                context,
            )
        except DataCheckException as e:
            print(e)
            context["exception"] = e
            self.on_failure(context)
        except Exception as e:
            print(e)
            context["exception"] = DataCheckException.from_exception(e)
            self.on_failure(
                context,
            )
        self.after(context)

    def _set_rules(self, rule_methods: list[str]):
        """
        Internal: Set the rules for the check
        """
        for class_method in rule_methods:
            # Ensure all rules are stored in the rules dict
            method = getattr(self, class_method)
            self.rules[class_method] = method

    def _update_from_suite_internals(self, suite_internals: SuiteInternal):
        """
        Internal: Set the suite model for the check
        """
        self._internal["suite_model"] = suite_internals["suite_model"]
        if suite_internals["dataset"] is not None:
            self.dataset = suite_internals["dataset"]

    def _get_rules_params(self, rule: str) -> list[FunctionArgs]:
        """
        Get the params for a rule
        """
        if rule not in self.rules_params:
            return [
                {
                    "args": tuple(),
                    "kwargs": dict(),
                }
            ]
        else:
            params = self.rules_params[rule]

            if callable(params):
                params = params()

            if not isinstance(params, list):
                params = [check_utils.as_func_args(params)]

            new_params = []
            for param in params:
                if "args" not in param or "kwargs" not in param:
                    param = check_utils.as_func_args(param)
                new_params.append(param)

            return new_params
