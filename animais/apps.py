from django.apps import AppConfig


class AnimaisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'animais'
    verbose_name = 'Gerenciador de Animais'
    def ready(self):
        import animais.signals
