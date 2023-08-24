import pandas as pd
from adtk.data import validate_series
from adtk.detector import PersistAD
from pyod.models.iforest import IForest
from pyod.models.ocsvm import OCSVM
from hamcrest import assert_that, equal_to
from data_checks import DataCheck


class AnomalyDetectionCheck(DataCheck):
    time_series_data = pd.read_csv(
        "examples/general/anomaly_detection/data.csv",
        index_col="timestamp",
        parse_dates=True,
    )

    def detect_with_adtk(self):
        s_train = validate_series(self.time_series_data)
        persist_ad = PersistAD()
        anomalies = persist_ad.fit_detect(s_train).dropna()
        assert_that(
            (anomalies == False).all().squeeze(), equal_to(True), "Anomalies detected"
        )

    def detect_with_pyod_iforest(self):
        X = self.time_series_data[["value"]]
        model = IForest()
        model.fit(X)
        scores_pred = model.decision_function(X)
        threshold = model.threshold_
        labels_pred = scores_pred > threshold
        detected_anomalies = self.time_series_data[labels_pred]

        assert_that(
            detected_anomalies.empty,
            equal_to(True),
            f"Anomalies detected: {detected_anomalies}",
        )

    def detect_with_pyod_ocsvm(self):
        X = self.time_series_data[["value"]]
        model = OCSVM()
        model.fit(X)
        scores_pred = model.decision_function(X)
        threshold = model.threshold_
        labels_pred = scores_pred > threshold
        detected_anomalies = self.time_series_data[labels_pred]

        assert_that(
            detected_anomalies.empty,
            equal_to(True),
            f"Anomalies detected: {detected_anomalies}",
        )
