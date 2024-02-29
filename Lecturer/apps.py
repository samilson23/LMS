from django.apps import AppConfig


class LecturerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Lecturer'

    def ready(self):
        import Faculty.signals
