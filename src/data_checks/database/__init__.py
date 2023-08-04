import os
from .utils.engine import connect, get_session
from .managers.models import Base
from .managers import db

check_database_url = os.getenv("CHECKS_DATABASE_URL")
if check_database_url:
    engine = connect(check_database_url)
    Base.metadata.create_all(engine)
    Base.set_session(get_session())
    db.set_session(get_session())
