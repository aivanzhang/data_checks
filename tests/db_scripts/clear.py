from src.data_checks.base.database.managers.models import Base
from src.data_checks.base.database.utils.engine import engine

Base.metadata.drop_all(engine)
