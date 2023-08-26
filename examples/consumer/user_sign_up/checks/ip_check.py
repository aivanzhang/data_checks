import re
from data_checks import DataCheck
from hamcrest import assert_that, equal_to, is_not


class IpCheck(DataCheck):
    BLACKLISTED = ["192.256.1.1", "192.168.1.1"]

    def rule_not_blacklisted(self):
        ips = self.dataset["data"]["IP Address"]
        for ip in ips:
            assert_that(
                ip in self.BLACKLISTED, equal_to(False), f"IP {ip} is blacklisted"
            )

    def rule_valid_ipv4(self):
        ips = self.dataset["data"]["IP Address"]
        for ip in ips:
            assert_that(
                re.match(
                    r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
                    ip,
                ),
                is_not(None),
                f"IP {ip} is not valid IPv4",
            )
