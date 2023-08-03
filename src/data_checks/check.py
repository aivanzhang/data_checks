"""
Check class
"""
from typing import Iterable, Optional, Callable, Awaitable
import time
import asyncio
import copy
from .exceptions import DataCheckException
from .check_types import FunctionArgs, CheckBase
from .dataset import Dataset
from .mixins.metadata_mixin import MetadataMixin
from .utils.class_utils import get_all_methods


class Check(CheckBase, MetadataMixin):
    def __init__(
        self,
        name: Optional[str] = None,
        metadata_dir: Optional[str] = None,
        description="",
        rules_prefix="",
        rules_params=dict(),
        excluded_rules: Iterable = [],
        tags: Iterable = [],
        verbose=False,
        dataset: Optional[Dataset] = None,
    ):
        """
        Initialize a check object
        """
        super().__init__()
        self.verbose = verbose
        self.name = self.__class__.__name__ if name is None else name
        self.dataset = dataset
        self.description = description
        self.excluded_rules = set(excluded_rules)
        self.tags = set(tags)
        self.set_metadata_dir(metadata_dir)

        self.rules_prefix = rules_prefix
        self.rules = dict()
        self.rules_context = dict()
        self.rules_params = rules_params

        for class_method in get_all_methods(self):
            # Ensure all rules are stored in the rules dict
            method = getattr(self, class_method)
            if (
                self.rules_prefix != "" and class_method.startswith(self.rules_prefix)
            ) or getattr(method, "is_rule", False):
                self.rules[class_method] = method
                self.rules_context[class_method] = copy.deepcopy(
                    self.DEFAULT_RULE_CONTEXT
                )
                rule_name = getattr(method, "name", "")
                if rule_name:
                    self.rules_context[class_method]["name"] = rule_name
                run_if_func = getattr(method, "run_if", None)
                if run_if_func is not None:
                    self.rules_context[class_method]["run_if"] = run_if_func
                # Ensure all tags are stored in the rules_context dict
                rule_tags = getattr(method, "tags", None)
                if rule_tags is not None:
                    self.rules_context[class_method]["tags"] = rule_tags
                    if getattr(method, "should_prefix_tags", False):
                        self.rules_context[class_method]["tags"] = {
                            f"{self.name}.{tag}" for tag in rule_tags
                        }

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

    def _get_rules_params(self, rule: str) -> FunctionArgs | list[FunctionArgs]:
        """
        Get the params for a rule
        """
        if rule not in self.rules_params:
            return {
                "args": tuple(),
                "kwargs": dict(),
            }
        else:
            params: FunctionArgs | list[FunctionArgs] | Callable[
                ..., FunctionArgs | list[FunctionArgs]
            ] = self.rules_params[rule]
            if callable(params):
                params = params()
            return params

    def get_rules_to_run(self, tags: Optional[Iterable]) -> set:
        """
        Find rules by tags and exclude rules
        """

        included_rules = [
            rule
            for rule in self.rules.keys()
            if rule not in self.excluded_rules
            and (
                self.rules_context[rule]["run_if"] is None
                or self.rules_context[rule]["run_if"]()
            )
        ]

        if tags is None:
            return set(included_rules)
        return {
            rule
            for rule in included_rules
            if set(tags).intersection(self.rules_context[rule]["tags"])
        }

    def setup(self):
        """
        One time setup for all rules in the check
        """
        return

    def before(self, rule: str, params: FunctionArgs):
        """
        Run before each rule
        """
        return

    def _exec_rule(
        self, rule: str, rule_func: Callable[..., None], params: FunctionArgs
    ):
        """
        Execute a rule
        """
        rule_metadata = {"rule": rule, "params": params}
        self.before(**rule_metadata)
        try:
            rule_func(*params["args"], **params["kwargs"])
            self.on_success(**rule_metadata)
        except AssertionError as e:
            print(e)
            self.on_failure(
                DataCheckException.from_assertion_error(e, metadata=rule_metadata)
            )
        except DataCheckException as e:
            print(e)
            self.on_failure(e)
        self.after(**rule_metadata)

    def run(self, rule: str):
        """
        Runs a rule once with one set of params or multiple times with multiple sets of params
        """
        rule_func = self.rules[rule]
        rules_params = self._get_rules_params(rule)
        if isinstance(rules_params, list):
            for params in rules_params:
                self._exec_rule(rule, rule_func, params)
        else:
            self._exec_rule(rule, rule_func, rules_params)

    def run_async(self, rule: str):
        """
        Asynchronously runs a rule once with one set of params or multiple times with multiple sets of params
        """
        rule_func = self.rules[rule]
        rules_params = self._get_rules_params(rule)

        if isinstance(rules_params, list):
            for params in rules_params:
                yield asyncio.get_event_loop().run_in_executor(
                    None, self._exec_rule, rule, rule_func, params
                )
        else:
            yield asyncio.get_event_loop().run_in_executor(
                None, self._exec_rule, rule, rule_func, rules_params
            )

    def after(self, rule: str, params: FunctionArgs):
        """
        Runs after each rule
        """
        return

    def on_success(self, rule: str, params: FunctionArgs):
        """
        Called when a rule succeeds
        """
        pass

    def on_failure(self, exception: DataCheckException):
        """
        Called when a rule fails
        """
        raise exception

    def run_all(self, tags: Optional[Iterable] = None):
        """
        Run all the rules in the check
        Parameters:
            tags: only run rules with these tags will be run
        """
        self.setup()

        rules_to_run = self.get_rules_to_run(tags)

        for index, rule in enumerate(rules_to_run):
            print(
                f"\t[{index + 1}/{len(rules_to_run)} Rules] {self.rules_context[rule]['name']}"
            )
            start_time = time.time()
            self.run(rule)
            print(f"\t{time.time() - start_time:.2f} seconds")

        self.teardown()

    def _generate_async_rule_runs(
        self, tags: Optional[Iterable] = None
    ) -> list[Awaitable]:
        """
        Generate a list of coroutines that can be awaited
        """
        return [
            async_rule
            for rule_name in self.get_rules_to_run(tags)
            for async_rule in self.run_async(rule_name)
        ]

    async def run_all_async(self, tags: Optional[Iterable] = None, should_run=True):
        """
        Run all the rules in the check asynchronously. Note that order of execution is not guaranteed (aside from setup and teardown).
        Parameters:
            tags: only run rules with these tags will be run
            should_run: if False, will only generate async rules that can be awaited. Skips setup and teardown.
        """
        if not should_run:
            return self._generate_async_rule_runs(tags)

        self.setup()
        await asyncio.gather(*self._generate_async_rule_runs(tags))
        self.teardown()

    def teardown(self):
        """
        One time teardown after all rules are run
        """
        return

    def __str__(self):
        return self.name
