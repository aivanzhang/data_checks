import os
import importlib
from typing import Any
from data_checks.utils.start import init
from data_checks.data_check import *
from data_checks.data_suite import *

settings_module = os.environ.get("CHECK_SETTINGS_MODULE", None)
try:
    if settings_module is None:
        raise ImportError("No settings module found.")
    settings = importlib.import_module(settings_module)
    init(settings.DATABASE_URL, settings.CHECKS_DIR, settings.SUITES_DIR)
except ImportError as e:
    print(f"Error importing module '{settings_module}': {e}")
