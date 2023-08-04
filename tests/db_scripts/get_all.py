from src.data_checks.database.managers.models import Base
from src.data_checks.database.utils import get_session

for model in Base.__subclasses__():
    print(f"Model: {model.__name__}")
    for record in get_session().query(model).all():
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
