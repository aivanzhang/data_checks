if __name__ == "__main__":
    import argparse
    import time
    from datetime import datetime, timedelta, timezone
    from data_checks.do.utils.silence_utils import *
    from data_checks.database import RuleManager

    parser = argparse.ArgumentParser(
        prog="python -m data_checks.do.silence",
        description="Silence a rule(s) given its hash or combination of rule name, check name, and suite name.",
    )

    parser.add_argument(
        "--until",
        "-u",
        type=datetime.fromisoformat,
        help="Date to silence the rule until. ISOformat: YYYY-MM-DD:HH:mm:ss",
        default=None,
    )

    parser.add_argument(
        "--delta",
        "-d",
        help="Time delta from current time to silence the rule until. Format: 1h, 1d, 1m, 1w (hour, day, minute, week). Example: 3h for 3 hours.",
        type=validate_time_delta,
    )

    parser.add_argument(
        "--hash",
        "-hash",
        type=str,
        help="Hash of the rule to silence.",
        default=None,
    )

    args = parser.parse_args()

    if not (args.until or args.delta):
        raise argparse.ArgumentTypeError(
            "Must provide either --until or --delta. See --help for more information."
        )

    if not (args.hash):
        raise argparse.ArgumentTypeError(
            "Must provide either --hash. See --help for more information."
        )
    silence_until_date = (
        datetime.fromtimestamp(time.mktime(args.until.timetuple()), tz=timezone.utc)
        if args.until
        else datetime.now(timezone.utc)
        + timedelta(
            hours=int(args.delta[0]) if args.delta[1] == "h" else 0,
            days=int(args.delta[0]) if args.delta[1] == "d" else 0,
            minutes=int(args.delta[0]) if args.delta[1] == "m" else 0,
            weeks=int(args.delta[0]) if args.delta[1] == "w" else 0,
        )
    )

    print(f"Silencing rule(s) until {silence_until_date}")
    if silence_until_date is None or silence_until_date < datetime.now(timezone.utc):
        raise argparse.ArgumentTypeError(
            "Silence until date not found or must be in the future. See --help for more information."
        )

    if args.hash:
        print(f"Silencing rule with hash:\n{args.hash}")
        if RuleManager.silence(silence_until_date, args.hash):
            print("Successfully silenced rule.")
        else:
            print("Rule not found.")
