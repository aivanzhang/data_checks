"""
Check class
"""
from typing import Dict, Any, Iterable, Optional
import time
import inspect
import asyncio
from exceptions import DataCheckException
from check_types import FunctionArgs, CheckBase
from utils.class_functions import get_all_methods


class Check(CheckBase):
    def __init__(
        self,
        name=None,
        description="",
        rules_prefix="",
        tags: Iterable = [],
        verbose=False,
    ):
        """
        Initialize a check object
        """
        self.verbose = verbose
        self.name = self.__class__.__name__ if name is None else name
        self.description = description
        self.tags = set(tags)

        self.rules_prefix = rules_prefix
        self.rules = dict()
        self.rules_params = dict()
        self.rules_context = dict()
        self.metadata = dict()

        for class_method in get_all_methods(self):
            # Ensure all rules are stored in the rules dict
            method = getattr(self, class_method)
            if (
                self.rules_prefix != "" and class_method.startswith(self.rules_prefix)
            ) or getattr(method, "is_rule", False):
                self.rules[class_method] = method
                self.rules_context[class_method] = self.DEFAULT_RULE_CONTEXT.copy()

                # Ensure all tags are stored in the rules_context dict
                rule_tags = getattr(method, "tags", None)
                if rule_tags is not None:
                    self.rules_context[class_method]["tags"] = rule_tags
                    if getattr(method, "should_prefix_tags", False):
                        self.rules_context[class_method]["tags"] = {
                            f"{self.name}.{tag}" for tag in rule_tags
                        }

    def _get_rules_params(self, rule: str) -> FunctionArgs:
        """
        Get the params for a rule
        """
        if rule not in self.rules_params:
            return {
                "args": tuple(),
                "kwargs": dict(),
            }
        else:
            params = self.rules_params[rule]
            if callable(params):
                params = params()
            return params

    def find_rules_by_tags(self, tags: Optional[Iterable]) -> set:
        """
        Find rules by tags
        """
        if tags is None:
            return set(self.rules.keys())
        return {
            rule
            for rule in self.rules.keys()
            if set(tags).intersection(self.rules_context[rule]["tags"])
        }

    @classmethod
    def init(cls, file_path: str) -> "Check":
        """
        Initialize a check from a JSON file
        """
        return cls()

    def setup(self):
        """
        One time setup for all rules in the check
        """
        return

    def before(self):
        """
        Run before each rule
        """
        return

    def run(self, rule: str):
        """
        Runs a single rule
        """
        self.before()
        try:
            rule_func = self.rules[rule]
            rules_params = self._get_rules_params(rule)
            rule_func(*rules_params["args"], **rules_params["kwargs"])
            self.on_success()
        except AssertionError as e:
            print(e)
            self.on_failure(DataCheckException.from_assertion_error(e))
        except DataCheckException as e:
            print(e)
            self.on_failure(e)
        self.after()

    def run_async(self, rule: str):
        return asyncio.get_event_loop().run_in_executor(None, self.run, rule)

    def after(self):
        return

    def run_all(self, tags: Optional[Iterable]):
        """
        Run all the rules in the check
        Parameters:
            tags: only run rules with these tags will be run
        """
        self.setup()

        tags = None if tags is None else set(tags)
        rules_to_run = self.find_rules_by_tags(tags)

        for index, rule in enumerate(rules_to_run):
            print(f"\t[{index + 1}/{len(rules_to_run)}] {rule}")
            start_time = time.time()
            self.run(rule)
            print(f"\t{time.time() - start_time:.2f} seconds")

        self.teardown()

    async def run_all_async(self, tags: Optional[Iterable], should_run=True):
        """
        Run all the rules in the check asynchronously
        Parameters:
            should_run: if False, returns an array of coroutines that can be awaited
            tags: only run rules with these tags will be run
        """
        async_rule_runs = [
            self.run_async(rule) for rule in self.find_rules_by_tags(tags)
        ]
        if not should_run:
            return async_rule_runs

        self.setup()
        await asyncio.gather(*async_rule_runs)
        self.teardown()

    def on_success(self):
        """
        Called when a rule succeeds
        """
        pass

    def on_failure(self, exception: DataCheckException):
        """
        Called when a rule fails
        """
        raise exception

    def teardown(self):
        """
        One time teardown after all rules are run
        """
        return

    def save_to_file(self, file_path: str):
        """
        Save the check to a file
        """
        return

    def log_metadata(self, metadata: Dict[str, Any]):
        """
        Log metadata with its associated rule
        """
        method = inspect.stack()[1][3]
        self.metadata[method] = metadata

    def __str__(self):
        return self.name


"""
Go from notebook to check
suites
roadmap

Download and store locally

rules_context without decorator

streaming database
"""
