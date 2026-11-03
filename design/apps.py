from django.apps import AppConfig

class DesignConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'design'

    def ready(self):
        from . import signals