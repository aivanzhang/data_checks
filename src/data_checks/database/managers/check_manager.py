from .base_manager import BaseManager
from ..models import Check, CheckExecution, Rule


class CheckManager(BaseManager):
    def create_check(
        self,
        id: int,
        name: str,
        readable_name: str,
        description: str,
        code: str,
        tags: list[str],
        excluded_rules: list[str],
        rules: list["Rule"],
        executions: list["CheckExecution"],
    ) -> Check:
        new_check = Check(
            id=id,
            name=name,
            readable_name=readable_name,
            description=description,
            code=code,
            tags=tags,
            excluded_rules=excluded_rules,
            rules=rules,
            executions=executions,
        )
        self.session.add(new_check)
        self.session.commit()
        return new_check
