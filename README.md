# data_checks 
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
2) More flexibility in specifying the parallelization options (see [Warning on Async Executions](#warning-on-async-executions))
3) Define before, after, on success and on failure actions based on data checks
4) Automatically generate data checks from the command line (as you would generate a database migration) and Jupyter Notebooks

## Define Settings
## Create Checks

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