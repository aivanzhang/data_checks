import os
from data_checks.database.managers.models import Base
from data_checks.database.utils import engine_utils, session_utils
from data_checks.database.managers import *
from data_checks.conf import settings

check_database_url = settings["CHECKS_DATABASE_URL"]
if check_database_url:
    engine = engine_utils.connect(check_database_url)
    Base.metadata.create_all(engine)
    session_utils.configure(engine)
