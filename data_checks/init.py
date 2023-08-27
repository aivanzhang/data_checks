import os
import re
from sqlalchemy import create_engine


def validate_database_url(url):
    engine = create_engine(url)
    engine.connect()


def validate_cron_schedule(schedule):
    return re.match(r"^\s*((\*|[0-9,-]+)\s+){4}(\*|[0-9,-]+)\s*$", schedule)


def generate_settings_file(data):
    settings_content = "\n".join(
        [
            f"{key} = {repr(value) if value != 'None' else value}"
            for key, value in data.items()
        ]
    )
    with open("check_settings.py", "w") as settings_file:
        settings_file.write(settings_content)


def generate_check_file(check_setting_dir):
    with open(check_setting_dir + "/my_first_data_check.py", "w") as check_file:
        check_file.write(MY_FIRST_DATA_CHECK)


def create_init_file(directory_path):
    init_file_path = os.path.join(directory_path, "__init__.py")
    with open(init_file_path, "w") as init_file:
        init_file.write("# This is an autogenerated file.")


def create_module_structure(module_directory_path):
    base_dir = os.getcwd()
    directory_path = os.path.join(base_dir, module_directory_path)
    if not os.path.exists(directory_path):
        print(f"Directory '{directory_path}' does not exist.")
        confirm = input("Would you like to create it? [y/n]: ")
        if confirm.lower() == "y":
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)

    sub_directories = module_directory_path.split("/")
    for i in range(len(sub_directories)):
        directory_path = os.path.join(base_dir, "/".join(sub_directories[: i + 1]))
        if "__init__.py" not in os.listdir(directory_path):
            create_init_file(directory_path)


MY_FIRST_DATA_CHECK = """
# Path: CHECKS_MODULE/my_first_data_check.py
from data_checks.classes.data_check import DataCheck

class MyFirstDataCheck(DataCheck):
    def setup(self):
        \"\"\"
        Setup the check. Use this to load data, initialize models, etc.
        \"\"\"
        super().setup() # DON'T FORGET TO CALL SUPER
        self.content = "Apple"

    def rule_my_first_successful_rule(self, data="Hello World"):
        # Call functions to check the data
        assert data == "Hello World"
    
    def rule_my_first_failed_rule(self):
        # Call functions to check the data
        # Throw an exception if the rule fails
        assert False, "This rule failed"

    def my_first_helper_function(self):
        # This function will not be run as a rule
        raise Exception("This function will not be run as a rule")
"""


def main():
    suite_directory_path = input(
        "Enter the relative file path of the directory where suites will be stored: "
    )
    create_module_structure(suite_directory_path)

    checks_directory_path = input(
        "Enter the relative file path of the directory where checks will be stored: "
    )
    create_module_structure(checks_directory_path)

    default_schedule = input("Enter the default CRON schedule: ")
    if not validate_cron_schedule(default_schedule):
        print("Error: Invalid cron schedule")
        return

    database_url = input("Enter the database URL: ")
    validate_database_url(database_url)

    alerting_endpoint = input("Enter the alerting endpoint URL: ")

    if alerting_endpoint.strip() == "":
        alerting_endpoint = "None"

    # Generate check_settings.py file
    settings_data = {
        "CHECKS_DATABASE_URL": database_url,
        "CHECKS_MODULE": checks_directory_path.replace("/", "."),
        "SUITES_MODULE": suite_directory_path.replace("/", "."),
        "ALERTING_ENDPOINT": alerting_endpoint,
        "DEFAULT_SCHEDULE": default_schedule,
    }
    generate_settings_file(settings_data)
    print("check_settings.py generated.")

    # Generate my_first_data_check.py file
    generate_check_file(os.path.join(os.getcwd(), checks_directory_path))
    print("my_first_data_check.py generated.")


if __name__ == "__main__":
    main()
