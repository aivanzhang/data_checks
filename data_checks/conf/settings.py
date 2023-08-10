# class Settings:
#     def __init__(self, settings_module):
#         # update this dict from global settings (but only for ALL_CAPS settings)
#         for setting in dir(global_settings):
#             if setting.isupper():
#                 setattr(self, setting, getattr(global_settings, setting))

#         # store the settings module in case someone later cares
#         self.SETTINGS_MODULE = settings_module

#         mod = importlib.import_module(self.SETTINGS_MODULE)

#         tuple_settings = (
#             "ALLOWED_HOSTS",
#             "INSTALLED_APPS",
#             "TEMPLATE_DIRS",
#             "LOCALE_PATHS",
#             "SECRET_KEY_FALLBACKS",
#         )
#         self._explicit_settings = set()
#         for setting in dir(mod):
#             if setting.isupper():
#                 setting_value = getattr(mod, setting)

#                 if setting in tuple_settings and not isinstance(
#                     setting_value, (list, tuple)
#                 ):
#                     raise ImproperlyConfigured(
#                         "The %s setting must be a list or a tuple." % setting
#                     )
#                 setattr(self, setting, setting_value)
#                 self._explicit_settings.add(setting)
