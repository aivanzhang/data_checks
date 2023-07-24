"""
This module contains utility functions for working with rules. 
"""


def get_rule_fields_from_source_code(source_code_file_path: str):
    """
    Get the fields related to a rule from its docstring
    """
    with open(source_code_file_path, "r") as f:
        source_code = f.read()

    return
