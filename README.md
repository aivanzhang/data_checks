# Data Checks
![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Python](https://img.shields.io/badge/python-3.7-blue.svg) 

**Create, schedule, and deploy data quality checks.**

## Overview
Exisiting data observability solutions are painfully static. **data_checks** provides a dynamic data observability framework that allows you to reuse existing Python code and/or write new Python code to define data quality checks. Inspired by Python's [unittest](https://docs.python.org/3/library/unittest.html), data_checks allows you to write data quality checks as easily and seamlessly as you would write unittests on your code.

Some reason you might use this library:
- Reuse existing Python code
- Greater control over how check are defined and executed
- Infinitely extendible and customizable for any data quality use case
- Connect any database to store data related to checks and executions
- Parallel execution
- CRON scheduling
- Silencing
- Alerting to a specified endpoint
- Storage of all logs

Some additional features that are in the works (in order of priority):
1) Custom pre-built analytics and visualizations
2) More flexibility in specifying the parallelization options (see [Warning on Fully Parallel Executions](#warning-on-fully-parallel-executions))
3) Attach actions to their data checks (i.e. remediation, custom flow if check succeeds or fails, etc.)
4) Automatically generate data checks from the command line (as you would generate a database migration) and Jupyter Notebooks

## Table of Contents
- [Data Checks](#data-checks)
  * [Overview](#overview)
  * [Table of Contents](#table-of-contents)
  * [Define Settings](#define-settings)
  * [Create Checks](#create-checks)
  * [(Advanced) Create Suites](#advanced-create-suites)
  * [(Advanced) Create Group Data Suites](#advanced-create-group-data-suites)
  * [Command Line Interface](#command-line-interface)
    + [Run Checks](#run-checks)
    + [Run Suites](#run-suites)
    + [Silencing Checks' Rules](#silencing-checks--rules)
  * [Warning on Serialization](#warning-on-serialization)
  * [Warning on Fully Parallel Executions](#warning-on-fully-parallel-executions)
  * [References](#references)
    + [Subclassing from the Base Check](#subclassing-from-the-base-check)
    + [Subclassing from the Base Suite](#subclassing-from-the-base-suite)
    + [Database](#database)
      - [Suite Table](#suite-table)
      - [Check Table](#check-table)
      - [Rule Table](#rule-table)
      - [Rule Execution Table](#rule-execution-table)
    + [Architecture](#architecture)
      - [Hierarchy](#hierarchy)
      - [Execution Flow](#execution-flow)

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
        raise Exception("This function should not be run as a rule")

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
        Define a dataset by passing in a dictionary of keys and values. 
        This will be generated once per suite run and passed to all the
        specified checks. Checks can then access the dataset by calling
        `self.dataset()` or `cls.dataset()`.
        """
        return Dataset({
            "my_first_dataset": "SELECT * FROM my_first_table"
        })

    @classmethod
    def checks_overrides(cls) -> dict | None:
        """
        Override the parameters of Checks' rules. Dictionary should 
        be in the following format:
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
        Define the suite's configuration. Dictionary should be
        in the following format:
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
        Define the checks to be run by the suite. Checks can be specified 
        by passing in the class, the class name, or an instance of the class. 
        If the check is specified by the class or class name, the suite will 
        instantiate the check. If the check is specified by an instance 
        of the class, the suite will use the instance as is.
        """
        return [
            "MyFirstDataCheck"
        ]
```
> [!IMPORTANT] 
> Your suite should be written inside the specified `SUITES_MODULE` in your settings file. For example, if you set `SUITES_MODULE = "my_suites"`, then you should write your check in `my_suites/my_first_data_suite.py`. Make sure that `SUITES_MODULE` and any nested modules are properly defined as directories (i.e. have an `__init__.py` file).

> [!IMPORTANT] 
> The params specified in `checks_overrides` will override the default params specified in the check. If no params are specified in `checks_overrides`, then the default params specified in the check will be used. If no default params and no params in `checks_overrides` are specified, then an error will be thrown. Also note that param values need to have a `__str__` method defined (see [Warning on Serialization](#warning-on-serialization)).

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
        Identifier for each element in the group. Can be accessed through 
        self.group["name"] in checks.
        """
        return "item"

    @classmethod
    def group(cls) -> list:
        """
        List of group's members. Each element will be subject to the specified
        checks. Can be accessed through self.group["value"] in checks
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
        will run CheckClass1 on element1, CheckClass1 on element2, 
        CheckClass2 on element1, and CheckClass2 on element2.
        """
        return [
            ItemCheck
        ]
```

> [!IMPORTANT] 
> Note that we are overriding `group_checks` and **NOT** `checks`.

> [!IMPORTANT] 
> Note that group name and values need to have a `__str__` method defined (see [Warning on Serialization](#warning-on-serialization)).

:tada: That's it! :tada: GroupDataSuite can be run in the same manner as DataSuite (see [Command Line Interface / Run Suites](#run-suites)).

## Command Line Interface
After defining your suites and/or checks, you can run them as well as other actions from the command line.

### Run Checks
To run checks, use the `data_checks.do.run_check` command:
```bash
usage: python -m data_checks.do.run_check [-h] [--parallel] [--schedule SCHEDULE] 
                                          [--error_logging]
                                          [--alerting]
                                          {CheckClass1}
                                          [{CheckClass1,CheckClass2, ...} ...]
```
The `run_checks` command takes in the following arguments:
- `checks`: List of checks to run by class name.
- `--parallel`: Run checks and nested rules in parallel. Before enabling see [Warning on Fully Parallel Executions](#warning-on-fully-parallel-executions). If not specified, checks will be run sequentially.
- `--schedule`: CRON schedule for the checks. If not specified, checks will be run once.
- `--error_logging`: Log errors to the console. This may duplicate some error logs in the database. If not specified, errors will only be stored in the database.
- `--alerting`: Send alerts to the specified endpoint. If not specified, no alerts will be sent.

For example to run `MyFirstDataCheck` in parallel every minute, log errors to the console, and send alerts to the specified endpoint we would use the following command:
```bash
python -m data_checks.do.run_check MyFirstDataCheck --error_logging --alerting --parallel --schedule "* * * * *"
```

### Run Suites
To run suites, use the `data_checks` command:
```bash
usage: python -m data_checks [-h] [--only ONLY] 
                             [--exclude {ConsistencySuite} [{ConsistencySuite} ...]]
                             [--parallel] [--scheduling] [--deploy] [--error_logging] [--alerting]
```
The `data_checks` command runs all the suites specified in `SUITES_MODULE`. The command can be customized by passing in the following arguments:
- `--only`: Only run the specified suite. If not specified, all suites will be run.
- `--exclude`: Exclude the specified suites. If not specified, no suites will be excluded.
- `--parallel`: Run suites in parallel. This will run each nested check in parallel and each nested rule in parallel. Before enabling see [Warning on Fully Parallel Executions](#warning-on-fully-parallel-executions). If not specified, suites will be run sequentially.
- `--scheduling`: Run suites on a schedule. If not specified, suites will be run once.
- `--deploy`: Deploy suites. If not specified, suites will not be deployed.
- `--error_logging`: Log errors to the console. This may duplicate some error logs in the database. If not specified, errors will only be stored in the database.

For example to run all suites in every minute, log errors to the console, and deploy the suites with we would use the following command:
```bash
python -m data_checks --error_logging --deploy --scheduling "* * * * *"
```
>[!IMPORTANT]
>To deploy a suite, the suite must have a schedule. If no schedule is specified and no schedule is found in the database, then an error will be thrown.

### Silencing Checks' Rules
To silence rules, use the `data_checks.do.silence_check` command:
```bash
usage: python -m data_checks.do.silence [-h] [--until UNTIL] [--delta DELTA] [--hash HASH]
                                        [--rule_name RULE_NAME] [--check_name CHECK_NAME]
                                        [--suite_name SUITE_NAME]
```
The `silence_check` command takes in the following arguments:
- `--until`: Date until which the rule will be silenced. Format should be `YYYY-MM-DD:HH:mm:ss`.
- `--delta`: Time delta for which the rule will be silenced. Format: 1h, 1d, 1m, 1w (hour, day, minute, week). Example: 3h for 3 hours.
- `--hash`: Hash of the rule (stored in the database) to silence. See [Database](#database) for more information.
- `--rule_name`: Name of the rule to silence.
- `--check_name`: Name of the check to silence.
- `--suite_name`: Name of the suite to silence.

> [!IMPORTANT]
> Either `--until` or `--delta` must be specified. If both are specified, `--until` will be used. If neither are specified, an error will be thrown. 

> [!IMPORTANT]
> Either `--hash` or `--rule_name` must be specified. `--hash` is the preferred method of silencing as it is the most precise. Specifically the hash allows you to silence a specific rule based off its suite, check, rule, **params**, and **group** (if specified within a GroupDataSuite). If `--hash` is not specified then `--suite_name`, `--check_name`, and `--rule_name` will be used together to find the rule(s) to silence.



## Warning on Serialization
To generate a hash for a rule, the library uses the `__str__` method of the rule's params and a rule's group (if defined within a GroupDataSuite). If the params are not serializable, then the hash will not be generated and an error will be thrown.

## Warning on Fully Parallel Executions
The library allows you to run checks and suites fully parallel by spinning off processes. When suites are run in parallel (i.e. with the `--parallel` flag), each suite will be run in its own process. Each check of the suite will be run in its own process. Each rule of the check will be run in its own process. When checks are run in parallel (i.e. with the `--parallel` flag), each check will be run in its own Process. Each rule of the check will be run in its own process. This allows for maximum parallelization and speed. However, there are some caveats to this:
1) This can be very resource intensive. Make sure you have enough resources to run the checks and suites in parallel.
2) Since a database is being used to store suite, check, rule, and execution data, make sure that the database can handle the number of connections (1 per suite, check, and rule).
3) Ensure that the server running the checks and suites has enough resources to handle the number of processes (1 per suite, check, and rule).

Currently there is no way to specify a maximum number of running processes. This is a feature that is in the works.

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
Suites, checks, rules, and rule executions are stored in a database. The database is specified in the `CHECKS_DATABASE_URL` variable in your settings file. Any database that is supported by SQLAlchemy can be used. This library generates the following tables in the database:

#### Suite Table
Stores data related to suites.

| id (INT)         | name (VARCHAR)       | description (VARCHAR)        | code (TEXT)         | schedule (VARCHAR)   | created_at (TIMESTAMPTZ)      |
|------------------|----------------------|------------------------------|---------------------|----------------------|-------------------------------|
| 001              | Suite1               | lorem ipsum dolor sit ...... | def ...             | * */2 * *            | 2023-08-22 00:00:00.359828-00 |
| 002              | Suite2               | lorem ipsum dolor sit ...... | def ...             | * * * * *            | 2023-08-22 01:00:00.359828-00 |
| 003              | Suite3               | lorem ipsum dolor sit ...... | def ...             | * */3 * *            | 2023-08-22 02:00:00.359828-00 |
| 004              | Suite4               | lorem ipsum dolor sit ...... | def ...             | * * * * *            | 2023-08-22 03:00:00.359828-00 |

- `id`: Unique identifier for the suite.
- `name`: Name of the suite.
- `description`: Description of the suite.
- `code`: Code of the suite.
- `schedule`: CRON schedule of the suite.
- `created_at`: Timestamp of when the suite was created.

#### Check Table
Stores data related to checks.

| id (INT)         | name (VARCHAR)       | description (VARCHAR)        | code (TEXT)         | excluded_rules (VARCHAR)         | created_at (TIMESTAMPTZ)      |
|------------------|----------------------|------------------------------|---------------------|----------------------------------|-------------------------------|
| 001              | Check1               | lorem ipsum dolor sit ...... | def ...             | ["rule1", "rule2", "rule3"]      | 2023-08-22 00:00:00.359828-00 |
| 002              | Check2               | lorem ipsum dolor sit ...... | def ...             | ["rule1", "rule2", "rule3"]      | 2023-08-22 01:00:00.359828-00 |
| 003              | Check3               | lorem ipsum dolor sit ...... | def ...             | ["rule1", "rule2", "rule3"]      | 2023-08-22 02:00:00.359828-00 |
| 004              | Check4               | lorem ipsum dolor sit ...... | def ...             | ["rule1", "rule2", "rule3"]      | 2023-08-22 03:00:00.359828-00 |

- `id`: Unique identifier for the check.
- `name`: Name of the check.
- `description`: Description of the check.
- `code`: Code of the check.
- `excluded_rules`: List of rules to exclude from the check.
- `created_at`: Timestamp of when the check was created.

#### Rule Table
Stores data related to rules.

| id (INT)         | check_id (INT)         | suite_id (INT)         | name (VARCHAR)       | hash (TEXT)        | severity (NUMERIC)         | code (TEXT)         | silence_until (TIMESTAMPTZ)      | created_at (TIMESTAMPTZ)      |
|------------------|------------------------|------------------------|----------------------|--------------------|----------------------------|---------------------|----------------------------------|-------------------------------|
| 001              | 001                    | NULL                   | Rule1                | RULE_HASH1         | 1                          | def ...             | NULL                             | 2023-08-22 00:00:00.359828-00 |
| 002              | 002                    | 002                    | Rule2                | RULE_HASH2         | 2                          | def ...             | 2023-08-22 01:00:00.359828-00    | 2023-08-22 01:00:00.359828-00 |
| 003              | 003                    | NULL                   | Rule3                | RULE_HASH3         | 3                          | def ...             | 2023-08-22 02:00:00.359828-00    | 2023-08-22 02:00:00.359828-00 |
| 004              | 004                    | 004                    | Rule4                | RULE_HASH4         | 4                          | def ...             | 2023-08-22 03:00:00.359828-00    | 2023-08-22 03:00:00.359828-00 |

- `id`: Unique identifier for the rule.
- `check_id`: ID of the check the rule belongs to.
- `suite_id`: ID of the suite the rule belongs to.
- `name`: Name of the rule.
- `hash`: Hash of the rule. In the following format:
```
suite:SUITE_NAME::check:CHECK_NAME::group:{name: GROUP_NAME, value: GROUP_VALUE}::rule:RULE_NAME::params:{args: [ARG1, ARG2, ...], kwargs: {key1: value1, key2: value2, ...}}
```
- `severity`: Severity of the rule.
- `code`: Code of the rule.
- `silence_until`: Timestamp of when the rule will be silenced until.
- `created_at`: Timestamp of when the rule was created.

#### Rule Execution Table
Stores data related to rule executions.

| id (INT)         | rule_id (INT)         | status (VARCHAR)         | params (TEXT)              | logs (TEXT)        | traceback (TEXT)          | exception (TEXT)          | created_at (TIMESTAMPTZ)      | finished_at (TIMESTAMPTZ)      |
|------------------|-----------------------|--------------------------|----------------------------|--------------------|---------------------------|---------------------------|-------------------------------|--------------------------------|
| 001              | 001                   | success                  | {"args": [], "kwargs": {}} | hellow world ...   | NULL                      | NULL                      | 2023-08-22 00:00:00.359828-00 | 2023-08-22 00:00:00.359828-00  |
| 002              | 002                   | failed                   | {"args": [], "kwargs": {}} | NULL               | lorem ipsum dolor sit ... | lorem ipsum dolor sit ... | 2023-08-22 01:00:00.359828-00 | 2023-08-22 01:00:00.359828-00  |
| 003              | 003                   | success                  | {"args": [], "kwargs": {}} | hellow world ...   | NULL                      | NULL                      | 2023-08-22 02:00:00.359828-00 | 2023-08-22 02:00:00.359828-00  |
| 004              | 004                   | failed                   | {"args": [], "kwargs": {}} | NULL               | lorem ipsum dolor sit ... | lorem ipsum dolor sit ... | 2023-08-22 03:00:00.359828-00 | 2023-08-22 03:00:00.359828-00  |

- `id`: Unique identifier for the rule execution.
- `rule_id`: ID of the rule the rule execution belongs to.
- `status`: Status of the rule execution.
- `params`: Params of the rule execution.
- `logs`: Logs of the rule execution.
- `traceback`: Traceback of the rule execution.
- `exception`: Exception of the rule execution.
- `created_at`: Timestamp of when the rule execution was created.
- `finished_at`: Timestamp of when the rule execution finished.

### Architecture
This library defines 3 core concepts: suites, checks, and rules. Suites are a collection of checks and/or rules. Checks are groups of organized rules that can be selectively executed. Rule are the atomic unit of this data check library and are functions that check incoming data. In the current version, rules need to be defined within checks. This will be changed in a later version of the library. Rules are the fundamental building block of data checks — every other component in this library is built on top of rules and adds additional functionality around these rules. Furthermore note that a Dataset simplifies how data moves between checks and when defined in a suite can be accessed by its corresponding checks and their rules.
#### Hierarchy
Suites are top level components that group checks. A dataset can be attached to a suite so that the same dataset can be accessed by the underlying checks and rules. Checks are second level components that contain rules. Rules are the lowest level components that actually check data. The following diagram shows the hierarchy of these components: 

![Data Checks Overview](./docs/img/high_level.png)
#### Execution Flow
The execution flow of a suite of data checks proceeds as follows:

![Execution Order](./docs/img/execution_order.png)
