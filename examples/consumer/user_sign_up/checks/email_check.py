import re
from data_checks import DataCheck
from hamcrest import assert_that, equal_to, is_not


class EmailCheck(DataCheck):
    def rule_does_not_contain_invalid_characters(self):
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        emails = self.dataset["data"]["Email"]
        for email in emails:
            assert_that(
                re.match(email_pattern, email),
                is_not(None),
                f"Invalid email address: {email}",
            )

    def rule_has_unique_emails(self):
        emails = self.dataset["data"]["Email"]
        assert_that(
            len(emails.unique()),
            equal_to(len(emails)),
            "Emails are not unique",
        )

    def rule_has_valid_domains(self):
        domains = self.dataset["data"]["Email"].str.split("@", expand=True)[1]
        for domain in domains:
            assert_that(
                domain in ["gmail.com", "yahoo.com", "hotmail.com"],
                equal_to(True),
                f"Invalid email domain: {domain}",
            )

    def rule_has_valid_tlds(self):
        tlds = self.dataset["data"]["Email"].str.split(".", expand=True)[2]
        for tld in tlds:
            assert_that(
                tld in ["com", "net", "org"],
                equal_to(True),
                f"Invalid email tld: {tld}",
            )
