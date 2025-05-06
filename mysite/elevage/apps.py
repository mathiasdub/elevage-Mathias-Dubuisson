from django.apps import AppConfig


class ElevageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'elevage'
    def ready(self):
        import elevage.signals