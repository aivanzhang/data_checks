export CHECK_SETTINGS_MODULE="examples.consumer.content.settings";
python -m data_checks.do.run_check -s "* * * * *" ContentCheck;