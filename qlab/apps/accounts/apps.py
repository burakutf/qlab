from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'qlab.apps.accounts'

    def ready(self):
        import qlab.apps.accounts.signals  # noqa
