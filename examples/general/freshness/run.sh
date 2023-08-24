export CHECK_SETTINGS_MODULE="examples.general.freshness.settings";
python -m data_checks.do.run_check -s "* * * * *" FreshnessCheck;