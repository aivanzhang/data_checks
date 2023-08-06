import os
from .utils.engine import connect
from .managers.utils import session_utils
from .managers.models import Base
from .managers import *

check_database_url = os.getenv("CHECKS_DATABASE_URL")
if check_database_url:
    engine = connect(check_database_url)
    Base.metadata.create_all(engine)
    session_utils.configure(engine)
