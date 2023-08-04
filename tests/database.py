from src.data_checks.database.utils import *
from src.data_checks.database.models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.data_checks.database.managers import CheckManager

# print(is_engine_defined())
engine = create_engine("postgresql://ivanzhang:@localhost:5432/test_data_checks")
start(engine)
# print(is_engine_defined())


# with Session(engine) as session:
#     new_check = Check(name="test", code="")
#     new_check_execution = CheckExecution(check=new_check)
#     session.add_all([new_check, new_check_execution])
#     session.commit()

CheckManager().create_check(
    id=1,
    name="test",
    readable_name="test",
    description="test",
    code="",
    tags=[],
    excluded_rules=[],
    rules=[],
    executions=[],
)
