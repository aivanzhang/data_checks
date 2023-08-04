from src.data_checks.database.managers.models import Base
from src.data_checks.database.utils import get_engine

Base.metadata.drop_all(get_engine())
