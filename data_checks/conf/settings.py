import importlib
import os
from data_checks.conf import global_settings

ENVIRONMENT_VARIABLE = "CHECK_SETTINGS_MODULE"


class Settings:
    def __init__(self):
        # update this dict from global settings (but only for ALL_CAPS settings)
        for setting in dir(global_settings):
            if setting.isupper():
                setattr(self, setting, getattr(global_settings, setting))

        settings_module = os.environ.get("CHECK_SETTINGS_MODULE", None)

        if settings_module is None:
            raise ImportError("No settings module found.")

        self.CHECK_SETTINGS_MODULE = settings_module

        # store the settings module in case someone later cares
        mod = importlib.import_module(self.CHECK_SETTINGS_MODULE)

        for setting in dir(mod):
            if setting.isupper():
                setting_value = getattr(mod, setting)
                setattr(self, setting, setting_value)

    def __getitem__(self, name):
        return self.__dict__[name]

    def __str__(self) -> str:
        return f"Settings({self.__dict__})"


settings = Settings()
