import os

CHECKS_DATABASE_URL = "postgresql://ivanzhang:@localhost:5432/test_data_checks_2"
CHECKS_DIR = os.path.join(os.path.dirname(__file__), "src/checks")
SUITES_DIR = os.path.join(os.path.dirname(__file__), "src/suites")
