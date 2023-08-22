from data_checks.base.check import Check


def generate_checks(check_type: type[Check], check_fields: list[dict]) -> list[Check]:
    return [check_type(**check_field) for check_field in check_fields]
