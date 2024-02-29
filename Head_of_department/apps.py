from django.apps import AppConfig


class HodConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Head_of_department'

    def ready(self):
        import Faculty.signals
