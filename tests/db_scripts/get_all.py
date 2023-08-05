from src.data_checks.database.managers.models import Base
from src.data_checks.database.managers.utils.sessions import session_scope

for model in Base.__subclasses__():
    print(f"Model: {model.__name__}")
    with session_scope() as session:
        for record in session.query(model).all():
            record_dict = {
                key: getattr(record, key)
                for key in record.__dict__
                if not key.startswith("_") and not key == "code"
            }
            print(record_dict)
            if (model.__name__ == "Suite" or model.__name__ == "Check") and hasattr(
                record, "rules"
            ):
                print(record.rules)
