# Data Checks
![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Python](https://img.shields.io/badge/python-3.7-blue.svg) 

**Create, schedule, and deploy data quality checks.**

## Overview
Exisiting data observability solutions are painfully static. **data_checks** provides a dynamic data observability framework that allows you to reuse existing Python code and/or write new Python code to define data quality checks. Inspired by Python's [unittest](https://docs.python.org/3/library/unittest.html), data_checks allows you to write data quality checks as easily and seamlessly as you would write unittests on your code.

Some reason you might use this library:
- Reuse existing Python code
- Greater control over how check definition and execution
- Infinitely extendible and customizable for any data quality use case
- Connect any database to store data related to checks and executions
- Async execution
- CRON scheduling
- Silencing
- Alerting to a specified endpoint
- Storage of all logs

Some additional features that are in the works (in order of priority):
1) Custom pre-built analytics and visualizations
2) More flexibility in specifying the parallelization options (see [Warning on Fully Async Executions](#warning-on-fully-async-executions))
3) Define before, after, on success and on failure actions based on data checks
4) Automatically generate data checks from the command line (as you would generate a database migration) and Jupyter Notebooks

## Define Settings
Before you can use the package, you need to first set up your settings. Create a settings file (e.g. `settings.py`) and define the following variables:
```python
# URL to the database where check and execution data will be stored
CHECKS_DATABASE_URL = None
# Module where checks are defined
CHECKS_MODULE = None
# Module where suites are defined
SUITES_MODULE = None
# Endpoint URL where alerts will be sent
ALERTING_ENDPOINT = None
# Default CRON schedule for suites
DEFAULT_SCHEDULE = None
```
Then, set the `CHECK_SETTINGS_MODULE` environment variable to your settings file (e.g. `my_data_checks.settings`):
```bash
export CHECK_SETTINGS_MODULE=my_data_checks.settings
```
or in Python:
```python
os.environ["CHECK_SETTINGS_MODULE"] = "my_data_checks.settings"
```
Now you're ready to start defining checks and suites!
## Create Checks
The library exposes the `DataCheck` class (defined in `data_checks.data_check`) which you can use to write your checks. Begin by subclassing the `DataCheck` class:
```python
from data_checks.data_check import DataCheck

class MyFirstDataCheck(DataCheck):
    pass
```
Then define methods (i.e. rules) that check the data and will be executed when the check is run:

```python
from data_checks.data_check import DataCheck

class MyFirstDataCheck(DataCheck):
    def my_first_successful_rule(self, data="Hello World"):
        # Call functions to check the data
        assert data == "Hello World"
        # Return nothing if the rule passes
    
    def my_first_failed_rule(self):
        # Call functions to check the data
        # Throw an exception if the rule fails
        assert False
```

:tada: That's it! :tada: You've created your first DataCheck. Now you can run it from the command line (see [Command Line Interface / Run Checks](#run-checks)).

---

The rules above have default arguments. For checks that are run outside of a suite (see [Create Suites](#advanced-create-suites)), either no arguments (excluding `self` or `cls`) or default arguments are required. For checks that are run within a suite, there are no such requirements as arguments can be specified by the suite.

By default the check runs all the functions defined as rules. However this may lead to issues if you have non-rule functions (i.e. helper functions) within the same class. To address this, the `defined_rules` method in `DataCheck` allows you to specify which methods are rules. For example:

```python
from data_checks.data_check import DataCheck

class MyFirstDataCheck(DataCheck):
    def my_first_successful_rule(self, data="Hello World"):
        # Call functions to check the data
        assert data == "Hello World"
        # Return nothing if the rule passes
    
    def my_first_failed_rule(self):
        # Call functions to check the data
        # Throw an exception if the rule fails
        assert False

    def my_first_helper_function(self):
        # This function will not be run as a rule
        raise Exception("This function will should not be run as a rule")

    @classmethod
    def defined_rules(cls) -> list[str]:
        return ["my_first_successful_rule", "my_first_failed_rule"]
```

> [!IMPORTANT] 
> Your check should be written inside the specified `CHECKS_MODULE` in your settings file. For example, if you set `CHECKS_MODULE = "my_checks"`, then you should write your check in `my_checks/my_first_data_check.py`. Make sure that `CHECK_MODULE` and any nested modules are properly defined as directories (i.e. have an `__init__.py` file).

> [!NOTE] 
> The example above uses assertions to check the data. You can however use any method you want to check the data. If the rule passes, return nothing. If the rule fails, throw an exception.

> [!NOTE] 
> If you have existing check classes, you can still subclass `DataCheck` and use the library in the same manner noted above. Make sure that your class does not accidentally override any of the methods in `Check` (see `data_checks.base.check`) 


> [!NOTE] 
> The `DataCheck` class is a simplified and beginner friendly subclass of the base `Check` class (`data_checks.base.check`). The user can also directly subclass the `Check` class to create more advanced checks (see [Subclassing from the Base Check](#subclassing-from-the-base-check)).

## (Advanced) Create Suites
Checks provide the most basic form of a data check. Suites provide an additional layer of abstraction that allows you to group checks together and run them together on a schedule. Suites also provide additional features like shared datasets. Suites are defined in a similar manner as checks. Begin by subclassing the `DataSuite` class (defined in `data_checks.data_suite`):
```python
from data_checks.data_suite import DataSuite

class MyFirstDataSuite(DataSuite):
    pass
```
Then override the required class methods:
```python
from data_checks.data_suite import DataSuite
from data_checks.dataset import Dataset

class MyFirstDataSuite(DataSuite):
    @classmethod
    def dataset(cls) -> Dataset | None:
        """
        Define a dataset by passing in a dictionary of keys and values. This will be generated once per suite run and passed to all the specified checks. Checks can then access the dataset by calling `self.dataset()` or `cls.dataset()`.
        """
        return Dataset({
            "my_first_dataset": "SELECT * FROM my_first_table"
        })

    @classmethod
    def checks_overrides(cls) -> dict | None:
        """
        Override the parameters of Checks' rules. Dictionary should be in the following format:
        {
            "CheckClass": {
                "rule_1": {
                    "param1": value1,
                    "param2": value2,
                    ...
                },
                "rule_2": {
                    "param1": value1,
                    "param2": value2,
                    ...
                }
                ...
            },
            "..."
        }
        """
        return {
            "MyFirstDataCheck": {
                "my_first_successful_rule": {
                    "data": "Hello World from Suite"
                }
            }
        }

    @classmethod
    def suite_config(cls) -> dict:
        """
        Define the suite's configuration. Dictionary should be in the following format:
        {
            "schedule": "CRON schedule",
        }
        """
        return {
            "schedule": "* * * * *", 
        }

    @classmethod
    def checks(cls) -> list[type | str | Check]:
        """
        Define the checks to be run by the suite. Checks can be specified by passing in the class, the class name, or an instance of the class. If the check is specified by the class or class name, the suite will instantiate the check. If the check is specified by an instance of the class, the suite will use the instance as is.
        """
        return [
            "MyFirstDataCheck"
        ]
```
> [!IMPORTANT] 
> Your suite should be written inside the specified `SUITES_MODULE` in your settings file. For example, if you set `SUITES_MODULE = "my_suites"`, then you should write your check in `my_suites/my_first_data_suite.py`. Make sure that `SUITES_MODULE` and any nested modules are properly defined as directories (i.e. have an `__init__.py` file).

> [!NOTE] 
> The `DataSuite` class is a simplified and beginner friendly subclass of the base `Suite` class (`data_checks.base.suite`). The user can also directly subclass the `Suite` class to create more advanced suites (see [Subclassing from the Base Suite](#subclassing-from-the-base-suite)).

:tada: That's it! :tada: You've created your first DataSuite. Now you can run it from the command line (see [Command Line Interface / Run Suites](#run-suites)).
## (Advanced) Create Group Data Suites
Suppose you want to run the same check over many different objects. For example assume you have `ItemCheck` that checks if a certain `Item` is valid or not via various rules (i.e. quality, price, etc.). You have hundreds of these items. You could:
1) Create a suite for each item and run them individually
2) Pass the item as an argument to each of the check's rules for all items
However both methods are tedious and inefficient. This library provides an abstraction to easily define a group where the pre-defined checks run on each group member. Begin by subclassing the `GroupDataSuite` class (defined in `data_checks.group_data_suite`):
```python
from data_checks.group_data_suite import GroupDataSuite

class MyFirstGroupDataSuite(GroupDataSuite):
    pass
```
Then override the required class methods:
```python
class GroupDataSuite(DataSuite):
    @classmethod
    def group_name(cls) -> str:
        """
        Identifier for each element in the group. Can be accessed through self.group["name"] in checks.
        """
        return "item"

    @classmethod
    def group(cls) -> list:
        """
        List of group's members. Each element will be subject to the specified checks. Can be accessed through self.group["value"] in checks
        """
        return [
            Item("item1", ...),
            Item("item2", ...),
            ...
        ]

    @classmethod
    def group_checks(cls) -> list[type[Check]]:
        """
        Checks to be run on each element in the group. For example:
        [
            CheckClass1,
            CheckClass2,
            ...
        ]
        with group
        [
            element1,
            element2,
            ...
        ]
        will run CheckClass1 on element1, CheckClass1 on element2, CheckClass2 on element1, and CheckClass2 on element2.
        """
        return [
            ItemCheck
        ]
```

> [!IMPORTANT] 
> Note that we are overriding `group_checks` and **NOT** `checks`.

:tada: That's it! :tada: GroupDataSuite can be run in the same manner as DataSuite (see [Command Line Interface / Run Suites](#run-suites)).

## Command Line Interface
After defining your suites and/or checks, you can run them as well as other actions from the command line.

### Run Checks
### Run Suites

### Silencing Checks' Rules

## Warning on TO STRNG

## Warning on Fully Async Executions

## References
### Subclassing from the Base Check
The base `Check` class (`data_checks.base.check`) define methods used to initialize, customize, and execute a check and its rules. It also has methods to store data related to the check and its execution as well as interact with its suite (if any). It is not recommended to directly subclass the `Check` class unless you have a specific use case that requires it. Instead, use the `DataCheck` class (`data_checks.data_check`) which is a simplified and beginner friendly subclass of the `Check` class.

If you truly want to modify the base `Check` class, you can do so by subclassing it and overriding its methods. However be :bangbang: **extremely careful** :bangbang: when doing so as it may break the functionality of the library. If you do so, make sure to test your check thoroughly.

> [!WARNING]  
> Documentation for the base `Check` class is limited and still a work in progress. For now, you can refer to the source code and its corresponding docstrings for more information.
### Subclassing from the Base Suite
The base `Suite` class (`data_checks.base.check`) define methods used to initialize, customize, and execute a suite and its checks. It also has methods to store data related to the suite and its execution as well as interact with its checks. It is not recommended to directly subclass the `Suite` class unless you have a specific use case that requires it. Instead, use the `DataSuite` class (`data_checks.data_suite`) which is a simplified and beginner friendly subclass of the `Suite` class.

If you truly want to modify the base `Suite` class, you can do so by subclassing it and overriding its methods. However be :bangbang: **extremely careful** :bangbang: when doing so as it may break the functionality of the library. If you do so, make sure to test your suite thoroughly.

> [!WARNING]  
> Documentation for the base `Suite` class is limited and still a work in progress. For now, you can refer to the source code and its corresponding docstrings for more information.

### Database
### Hierarchy
### Execution Flow