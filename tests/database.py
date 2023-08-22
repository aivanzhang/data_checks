from src.data_checks.base.database import *
from src.data_checks.base.database.managers import (
    CheckManager,
    RuleManager,
    SuiteManager,
)

# print(is_engine_defined())
# engine = create_engine("postgresql://ivanzhang:@localhost:5432/test_data_checks")
# print(is_engine_defined())


# with Session(engine) as session:
#     new_check = Check(name="test", code="")
#     new_check_execution = CheckExecution(check=new_check)
#     session.add_all([new_check, new_check_execution])
#     session.commit()


new_rule = RuleManager.create_rule(
    name="test",
    readable_name="test",
    description="test",
    code="",
)

new_suite = SuiteManager.create_suite(
    name="test",
    readable_name="test",
    description="test",
    code="",
    executions=[],
)

new_check = CheckManager.create_check(
    name="test",
    readable_name="test",
    description="test",
    code="",
    excluded_rules=[],
    executions=[],
)

new_rule.update(check=new_check)
