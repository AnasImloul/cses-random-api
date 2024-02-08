from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Problem, ProblemStatement


@receiver(post_migrate)
def setupDB(sender, **kwargs):
    Problem.retrieve_problems()
    ProblemStatement.retrieve_problems_statements()
    print('Database setup complete')
