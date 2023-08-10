import os

CHECKS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src/checks")

CHECKS_DATABASE_URL = "postgresql://ivanzhang:@localhost:5432/test_data_checks_2"

SUITES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src/suites")
