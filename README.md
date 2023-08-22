# Data Checks
![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Python](https://img.shields.io/badge/python-3.7-blue.svg) 

**Create, schedule, and deploy data quality checks.**

## Overview
Exisiting data observability solutions are painfully static. data_checks provides a dynamic data observability framework that allows you to reuse existing Python code and/or write new Python code to define data quality checks. Inspired by Python's [unittest](https://docs.python.org/3/library/unittest.html), data_checks allows you to write data quality checks as easily and seamlessly as you would write unittests on your code.

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
Then, set the `CHECK_SETTINGS_MODULE` environment variable to the path to your settings file (e.g. `data_checks.settings`):
```bash
export CHECK_SETTINGS_MODULE=data_checks.settings
```
or in Python:
```python
os.environ["CHECK_SETTINGS_MODULE"] = "data_checks.settings"
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
    def my_first_successful_rule(self):
        # Check the data
        assert True
        # Return nothing if the rule passes
    
    def my_first_failed_rule(self):
        # Check the data
        # Throw an exception if the rule fails
        assert False
```

That's it! You've created your first data check. Now you can run it from the command line (see [Command Line Interface](#command-line-interface)).

> [!WARNING] 
Your check should be written inside the specified `CHECKS_MODULE` in your settings file. For example, if you set `CHECKS_MODULE = "my_checks"`, then you should write your check in `my_checks/my_first_data_check.py`. Make sure that `CHECK_MODULE` and any nested modules are properly defined as packages (i.e. have an `__init__.py` file).


The `DataCheck` class is a simplified beginner friendly subclass of the base `Check` class (`data_checks.base.check`). The user can also directly subclass the `Check` class to create more advanced checks (see [(Advanced) Create Checks](#advanced-create-checks)).

## (Advanced) Create Checks
Running checks
Why do you need suites
## (Advanced) Create Suites

Why do you need group data suites
## (Advanced) Create Group Data Suites

## Command Line Interface
After defining your suites and/or checks, you can run them as well as other actions from the command line.

### Run Checks

### Silencing Checks' Rules

### Run Suites


## Warning on Fully Async Executions

## References

### Hierarchy
### Execution Flow