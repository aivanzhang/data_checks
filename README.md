# data_checks 
![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Python](https://img.shields.io/badge/python-3.6-blue.svg) 

**Program and execute any data quality checks.**

## Overview
Exisiting data observability solutions are painfully static. data_checks provides a dynamic data observability framework that allows you to program and execute any data quality checks. Inspired by Python's [unittest](https://docs.python.org/3/library/unittest.html) approach to writing unittests, data_checks allows you to write data quality checks as easily and seamlessly as you would write unittests on your code.

Some reason you might use this library:
- Use existing Python functions and/or Jupyter Notebooks in data checks
- Greater control over how data checks are defined and executed
- Infinitely extendible and customizable for any data quality use case
- Built-in async execution of data checks
- Connect any database to store data related to checks and executions
- (WIP) Define before, after, on success and on failure actions based on data checks

## Getting Started

## Features
### Suites
### Checks
### Rules
### Dataset
### Database
### Data Check Exceptions
## Requirements
- Python 3.6+
- SQLAlchemy 2.0+
- typing_extensions 4.7+
## Installation
```pip install -i https://test.pypi.org/simple/ data-checks -U```
## Example