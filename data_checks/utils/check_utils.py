from data_checks.base.check_types import FunctionArgs


def as_func_args(params: dict | tuple | FunctionArgs) -> FunctionArgs:
    if isinstance(params, tuple):
        return {
            "args": params,
            "kwargs": dict(),
        }
    else:
        new_params = {
            "args": params.get("args", tuple()),
            "kwargs": params.get("kwargs", dict()),
        }

        for key, value in params.items():
            if key != "args" and key != "kwargs":
                new_params["kwargs"][key] = value

        return {
            "args": new_params["args"],
            "kwargs": new_params["kwargs"],
        }
