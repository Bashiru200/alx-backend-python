from django.apps import AppConfig

class MessagesConfig(AppConfig):
    name = 'messaging'
    
    def ready (self):
        import messaging.signal