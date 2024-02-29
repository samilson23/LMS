from django.apps import AppConfig


class AdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Admin'

    def ready(self):
        import User.signals
        import Faculty.signals
        import Student.signals
