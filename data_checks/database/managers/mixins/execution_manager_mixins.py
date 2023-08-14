from typing import Optional, TypeVar, Generic
from datetime import datetime
from data_checks.database.managers.models.classes import Base
from data_checks.database.utils.database_utils import generate_update_object
from data_checks.database.utils.session_utils import session_scope

ExecutionType = TypeVar("ExecutionType", bound=Base)


class ExecutionManagerMixin(Generic[ExecutionType]):
    model: ExecutionType

    @classmethod
    def create_execution(
        cls,
        main_model: Base,
        status: Optional[str] = None,
    ) -> ExecutionType:
        new_execution = cls.model.create(
            main_model=main_model,
            status=status,
        )
        with session_scope() as session:
            session.add(new_execution)
        return new_execution

    @classmethod
    def update_execution(
        cls,
        execution_id: int,
        finished_at: datetime = datetime.now(),
        status: Optional[str] = None,
    ):
        with session_scope() as session:
            session.query(cls.model).filter_by(id=execution_id).update(
                generate_update_object(
                    finished_at=finished_at,
                    status=status,
                )
            )
