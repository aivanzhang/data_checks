"""
Check class
"""
from typing import Dict, Any, Callable
import time
import inspect
import asyncio
from exceptions import DataCheckException
from check_types import FunctionArgs, RuleContext
from utils._class import get_all_methods


class Check:
    # Default rule context for rules missing fields
    DEFAULT_RULE_CONTEXT: RuleContext = {
        "name": "",
        "description": "",
        "severity": 1.0,
        "args": tuple(),
        "kwargs": dict(),
    }

    def __init__(self, name=None, description="", rules_prefix="", verbose=False):
        """
        Initialize a check object
        """
        self.verbose = verbose
        self.name = self.__class__.__name__ if name is None else name
        self.description = description

        # Prefix for all rules in the check to be automatically run
        self.rules_prefix = rules_prefix

        # Stores all the rules functions in the check
        self.rules: Dict[str, Callable[..., None]] = dict()

        # Stores the params for each rule
        self.rule_params: Dict[str, FunctionArgs | Callable[..., FunctionArgs]] = dict()

        # Find and store all the rules in the check
        for class_method in get_all_methods(self):
            method = getattr(self, class_method)
            if (
                self.rules_prefix != "" and class_method.startswith(self.rules_prefix)
            ) or getattr(method, "is_rule", False):
                self.rules[class_method] = method

        # Stores any metadata generated when a rule runs
        self.rules_context: Dict[str, RuleContext] = dict.fromkeys(
            self.rules,
            self.DEFAULT_RULE_CONTEXT,
        )

    @classmethod
    def init(cls, file_path: str) -> "Check":
        """
        Initialize a check from a JSON file
        """
        return cls()

    def _get_rule_params(self, rule: str) -> FunctionArgs:
        """
        Get the params for a rule
        """
        if rule not in self.rule_params:
            return {
                "args": tuple(),
                "kwargs": dict(),
            }
        else:
            params = self.rule_params[rule]
            if callable(params):
                params = params()
            return params

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
            rule_params = self._get_rule_params(rule)
            rule_func(*rule_params["args"], **rule_params["kwargs"])
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

    def run_all(self):
        """
        Run all the rules in the check
        """
        self.setup()
        for index, rule in enumerate(self.rules):
            print(f"\t[{index + 1}/{len(self.rules)}] {rule}")
            start_time = time.time()
            self.run(rule)
            print(f"\t{time.time() - start_time:.2f} seconds")
        self.teardown()

    async def run_all_async(self, should_run=True):
        """
        Run all the rules in the check asynchronously
        should_run: if False, returns an array of coroutines
        """
        async_rule_runs = [self.run_async(rule) for rule in self.rules]
        if not should_run:
            return async_rule_runs

        self.setup()
        await asyncio.gather(*async_rule_runs)
        self.teardown()

    def on_success(self):
        """
        Called when a rule succeeds
        """
        return

    def on_failure(self, exception: DataCheckException):
        """
        Called when a rule fails
        """
        return

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
        print("logging metadata")
        rule = ""
        curframe = inspect.currentframe()
        # print(inspect.stack()[1][3].startswith(DEFAULT_RULE_PREFIX))
        # calframe = inspect.getouterframes(curframe, 2)
        # print(curframe, calframe)
        # print('caller name:', calframe[1][3])
        # self.rules_context[rule].update(metadata)

    @staticmethod
    def rule(
        name=DEFAULT_RULE_CONTEXT["name"],
        description=DEFAULT_RULE_CONTEXT["description"],
        severity=DEFAULT_RULE_CONTEXT["severity"],
    ):
        """
        Decorator for instantite a rule function
        """

        def wrapper(rule_func):
            rule_name = str(rule_func.__name__)

            def wrapper_func(self: Check, *args, **kwargs):
                self.rules_context[rule_name]["name"] = name
                self.rules_context[rule_name]["description"] = description
                self.rules_context[rule_name]["severity"] = severity
                self.rules_context[rule_name]["args"] = (
                    self.DEFAULT_RULE_CONTEXT["args"] if len(args) == 0 else args
                )
                self.rules_context[rule_name]["kwargs"] = (
                    self.DEFAULT_RULE_CONTEXT["kwargs"]
                    if len(kwargs.keys()) == 0
                    else kwargs
                )
                return rule_func(self, *args, **kwargs)

            wrapper_func.name = name or rule_name
            wrapper_func.is_rule = True
            return wrapper_func

        return wrapper

    def __repr__(self):
        return f"<{self.name}>"


"""
Go from notebook to check
Download and store locally

rules_context without decorator

streaming database
"""
