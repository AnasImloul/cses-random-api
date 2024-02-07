from django.apps import AppConfig


class InsuranceAppConfig(AppConfig):
    name = 'csesAPI'

    def ready(self):
        from . import signals
