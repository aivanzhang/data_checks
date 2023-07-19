"""
Check class
"""
from typing import Dict, Any, Callable
import time
import inspect
from exceptions import DataCheckException
from check_types import FunctionArgs
from utils.class_utils import get_all_methods
from ingestors import ingest_from_registry


class Check:
    def __init__(self, name=None, description="", rules_prefix="", verbose=False):
        """
        Initialize a check object
        """
        self.verbose = verbose
        self.name = self.__class__.__name__ if name is None else name
        self.description = description
        self.rules_prefix = rules_prefix
        self.rules: Dict[str, Callable[..., None]] = dict()
        self.rule_params: Dict[str, FunctionArgs | Callable[..., FunctionArgs]] = dict()
        self.ingestor_params: Dict[
            str, Dict[str, FunctionArgs | Callable[..., FunctionArgs]]
        ] = dict()

        self.ingestors: Dict[str, Callable[..., Any]] = dict()
        for class_method in get_all_methods(self):
            method = getattr(self, class_method)
            if (
                self.rules_prefix != "" and class_method.startswith(self.rules_prefix)
            ) or getattr(method, "is_rule", False):
                self.rules[class_method] = method
            elif getattr(method, "is_ingestor", False):
                self.ingestors[class_method] = method

        # Stores any metadata generated when a rule runs
        self.rules_context = dict.fromkeys(self.rules, dict())

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

    def ingest_from(self, source: str) -> Callable:
        """
        Check for class-specific ingestors and then check for global ingestors
        """
        if source in self.ingestors:
            return self.ingestors[source]
        else:
            return ingest_from_registry(source)

    # def _get_params(self, rule) -> FunctionArgs:
    #     """
    #     Get the parameters for a rule
    #     """
    #     if rule in self.rule_params:
    #         if callable(self.rule_params[rule]):
    #             return self.rule_params[rule]()
    #         return self.rule_params[rule]
    #     return None

    def run(self, rule: str):
        """
        Runs a single rule
        """
        self.before()
        try:
            rule_func = self.rules[rule]
            rule_func()
            self.on_success()
        except AssertionError as e:
            print(e)
            self.on_failure(DataCheckException.from_assertion_error(e))
        except DataCheckException as e:
            print(e)
            self.on_failure(e)
        self.after()

    def after(self):
        return

    def run_all(self):
        """
        Run all the rules in the check based off the rules_prefix
        """
        self.setup()
        for index, rule in enumerate(self.rules):
            print(f"\t[{index + 1}/{len(self.rules)}] {rule}")
            start_time = time.time()
            self.run(rule)
            print(f"\t{time.time() - start_time:.2f} seconds")
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
    def rule(name="", severity=1.0):
        """
        Decorator for a rule function
        """

        def wrapper(rule_func):
            rule_name = rule_func.__name__

            def wrapper_func(self, *args, **kwargs):
                self.rules_context[rule_name]["name"] = name
                self.rules_context[rule_name]["severity"] = severity
                self.rules_context[rule_name]["args"] = args
                self.rules_context[rule_name]["kwargs"] = kwargs
                return rule_func(self, *args, **kwargs)

            wrapper_func.name = name or rule_name
            wrapper_func.is_rule = True
            return wrapper_func

        return wrapper

    @staticmethod
    def ingestor(name=""):
        """
        Decorator for a ingestor function
        """

        def wrapper(ingestor_func):
            ingestor_func.name = name or ingestor_func.__name__
            ingestor_func.is_ingestor = True
            return ingestor_func

        return wrapper

    def __repr__(self):
        return f"<{self.name}>"


"""

check_prefix = "rule_"
ingestor_prefix = "ingest_"

@ingestor("ingestor name")
def ingest_template():

@rule("rule name", "rule description")
def rule_template():

Go from notebook to check
Download and store locally

rules_context withut decorator
ingestor params

streaming database
"""
