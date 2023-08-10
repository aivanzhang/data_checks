from src.data_checks.database.managers.models import Base
from src.data_checks.database.utils.engine_utils import engine

Base.metadata.drop_all(engine)
