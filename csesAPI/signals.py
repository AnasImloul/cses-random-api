from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Problem


@receiver(post_migrate)
def setupDB(sender, **kwargs):
    Problem.retrieve_problems()
    Problem.retrieve_problems_stats()
