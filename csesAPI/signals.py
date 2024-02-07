from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import import_problems


@receiver(post_migrate)
def setupDB(sender, **kwargs):
    import_problems()
