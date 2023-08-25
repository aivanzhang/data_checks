if __name__ == "__main__":
    import argparse
    from data_checks.do.utils import analytics_utils

    analytic_funcs = [
        "get_executions_since",
        "get_silenced_rules",
        "get_latest_rules",
        "get_prev_next_executions",
        "get_status_counts",
    ]

    parser = argparse.ArgumentParser(
        prog="python -m data_checks.do.analytics",
        description="Run built-in analytics on data checks",
    )

    parser.add_argument(
        "analytic_func",
        metavar="analytic_func",
        type=str,
        nargs="?",
        help=f"Name of analytic function to run. Options: {analytic_funcs}",
    )

    if parser.parse_args().analytic_func:
        analytic_func = parser.parse_args().analytic_func
        if analytic_func not in analytic_funcs:
            raise ValueError(
                f"Invalid analytic_func: {analytic_func}. Options: {analytic_funcs}"
            )
        print(f"Running {analytic_func}")
        getattr(analytics_utils, analytic_func)()
    else:
        for analytic_func in analytic_funcs:
            print(f"Running {analytic_func}")
            getattr(analytics_utils, analytic_func)()
