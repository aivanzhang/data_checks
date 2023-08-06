"""
Check class
"""
import traceback
import time
import asyncio
import copy
import json
import sys
from typing import Iterable, Optional, Callable, Awaitable
from io import StringIO
from .exceptions import DataCheckException
from .check_types import FunctionArgs, CheckBase
from .rule_types import RuleData
from .suite_helper_types import SuiteInternal
from .dataset import Dataset
from .mixins.metadata_mixin import MetadataMixin
from .utils.class_utils import get_all_methods
from .utils import file_utils, class_utils
from .database import (
    CheckManager,
    CheckExecutionManager,
    RuleManager,
    RuleExecutionManager,
)


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
        if dataset is not None:
            self.dataset = dataset
        self.description = description
        self.excluded_rules = set(excluded_rules)
        self.tags = set(tags)
        self._internal = {
            "suite_model": None,
            "check_model": None,
            "check_execution_model": None,
            "rule_models": dict(),
            "rule_execution_id_to_output": dict(),
        }
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

                rule_data = getattr(method, "data", None)
                if rule_data:
                    rule_data = RuleData(**rule_data)
                    self.rules_context[class_method].update(rule_data)
                    # Ensure all tags are stored in the rules_context dict
                    rule_tags = rule_data["tags"]
                    self.rules_context[class_method]["tags"] = rule_tags
                    if getattr(method, "should_prefix_tags", False):
                        self.rules_context[class_method]["tags"] = {
                            f"{self.name}.{tag}" for tag in rule_tags
                        }

    def _update_from_suite_internals(self, suite_internals: SuiteInternal):
        """
        Internal: Set the suite model for the check
        """
        self._internal["suite_model"] = suite_internals["suite_model"]
        if suite_internals["dataset"] is not None:
            self.dataset = suite_internals["dataset"]

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
            rule for rule in self.rules.keys() if rule not in self.excluded_rules
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

        self._internal["check_model"] = CheckManager.create_check(
            name=self.name,
            description=self.description,
            tags=list(self.tags),
            excluded_rules=list(self.excluded_rules),
            code=file_utils.get_current_file_contents(__file__),
        )
        self._internal[
            "check_execution_model"
        ] = CheckExecutionManager.create_check_execution(
            check=self._internal["check_model"], status="running"
        )

    def before(self, rule: str, params: FunctionArgs) -> int:
        """
        Run before each rule
        """
        new_rule = RuleManager.create_rule(
            name=self.rules_context[rule]["name"],
            description=self.rules_context[rule]["description"],
            tags=list(self.rules_context[rule]["tags"]),
            code=class_utils.get_function_code(self, rule),
        )
        new_rule_execution = RuleExecutionManager.create_rule_execution(
            rule=new_rule,
            status="running",
            params=json.dumps(params),
        )

        if self._internal["check_model"] is not None:
            RuleManager.update_check_id(new_rule.id, self._internal["check_model"].id)

        if self._internal["suite_model"] is not None:
            RuleManager.update_suite_id(new_rule.id, self._internal["suite_model"].id)

        self._internal["rule_models"][rule] = new_rule

        rule_output = StringIO()
        self._internal["rule_execution_id_to_output"][
            new_rule_execution.id
        ] = rule_output
        sys.stdout = rule_output

        return new_rule_execution.id

    def _exec_rule(
        self, rule: str, rule_func: Callable[..., None], params: FunctionArgs
    ):
        """
        Execute a rule
        """
        rule_metadata = {"rule": rule, "params": params}
        exec_id = self.before(**rule_metadata)
        try:
            rule_func(*params["args"], **params["kwargs"])
            self.on_success(**rule_metadata, exec_id=exec_id)
        except AssertionError as e:
            print(e)
            self.on_failure(
                DataCheckException.from_assertion_error(e, metadata=rule_metadata),
                exec_id=exec_id,
            )
        except DataCheckException as e:
            print(e)
            self.on_failure(e, exec_id=exec_id)
        self.after(**rule_metadata, exec_id=exec_id)

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

    @staticmethod
    def update_execution(type: str, execution_id: int | None, **kwargs):
        """
        Update the execution of a rule
        """
        if type == "rule" and execution_id:
            RuleExecutionManager.update_execution(execution_id, **kwargs)
        if type == "check" and execution_id:
            CheckExecutionManager.update_execution(execution_id, **kwargs)

    def after(self, rule: str, params: FunctionArgs, **kwargs):
        """
        Runs after each rule
        """
        logs = ""
        if (
            kwargs["exec_id"]
            and self._internal["rule_execution_id_to_output"][kwargs["exec_id"]]
        ):
            logs = self._internal["rule_execution_id_to_output"][
                kwargs["exec_id"]
            ].getvalue()
            sys.stdout = sys.__stdout__
            print(logs)

        self.update_execution(
            type="rule",
            execution_id=kwargs["exec_id"],
            params=json.dumps(params),
            logs=logs,
        )

    def on_success(self, rule: str, params: FunctionArgs, **kwargs):
        """
        Called when a rule succeeds
        """
        self.update_execution(
            type="rule",
            execution_id=kwargs["exec_id"],
            status="success",
            logs="",
        )

    def on_failure(self, exception: DataCheckException, ignore_error=True, **kwargs):
        """
        Called when a rule fails
        Parameters:
            exception: the exception that was raised
            ignore_error: if True, will not raise the exception and continue running
        """
        self.update_execution(
            type="rule",
            execution_id=kwargs["exec_id"],
            status="failure",
            logs="",
            traceback=traceback.format_tb(exception.exception.__traceback__)
            if exception.exception
            else None,
            exception=exception.toJSON(),
        )
        if ignore_error:
            return
        if self._internal["check_execution_model"]:
            self.update_execution(
                type="check",
                execution_id=self._internal["check_execution_model"].id,
                status="failure",
            )
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
        check_execution = self._internal["check_execution_model"]

        if check_execution:
            CheckExecutionManager.update_execution(
                check_execution.id,
                status="success",
            )

    def __str__(self):
        return self.name
