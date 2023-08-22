def generate_update_object(**kwargs) -> dict:
    return {k: v for k, v in kwargs.items() if v is not None}
