from __future__ import unicode_literals

from django.apps import AppConfig


class AppNameConfig(AppConfig):
    name = 'app_name'

    # register app signals
    def ready(self):
        import app_name.signals.handler1
