from django.apps import AppConfig


class CompanyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'qlab.apps.company'

    def ready(self):
        import qlab.apps.company.signals
