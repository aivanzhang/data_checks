from data_checks.database.managers.models import Base
from data_checks.database.utils.engine_utils import engine

Base.metadata.drop_all(engine)
