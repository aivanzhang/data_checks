import os
from .managers.models import Base
from .utils.engine_utils import connect
from .utils.session_utils import configure
from .managers import *

check_database_url = os.getenv("CHECKS_DATABASE_URL")
if check_database_url:
    engine = connect(check_database_url)
    Base.metadata.create_all(engine)
    configure(engine)
