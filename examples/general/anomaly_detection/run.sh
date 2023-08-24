export CHECK_SETTINGS_MODULE="examples.general.anomaly_detection.settings";
python -m data_checks.do.run_check -s "* * * * *" AnomalyDetectionCheck;