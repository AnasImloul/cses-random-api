from django.db import models
from enum import Enum
from .utils.web import CSESClient


class ProblemCategory(Enum):
    INTRODUCTORY_PROBLEMS = 'Introductory Problems'
    SORTING_AND_SEARCHING = 'Sorting and Searching'
    DYNAMIC_PROGRAMMING = 'Dynamic Programming'
    GRAPH_ALGORITHMS = 'Graph Algorithms'
    RANGE_QUERIES = 'Range Queries'
    TREE_ALGORITHMS = 'Tree Algorithms'
    MATHEMATICS = 'Mathematics'
    STRING_ALGORITHMS = 'String Algorithms'
    GEOMETRY = 'Geometry'
    ADVANCED_TECHNIQUES = 'Advanced Techniques'
    ADDITIONAL_PROBLEMS = 'Additional Problems'


class Problem(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=256)
    url = models.CharField(max_length=256)
    category = models.CharField(max_length=256,
                                choices=[(category.name, category.value) for category in ProblemCategory])
    solved_count = models.IntegerField(null=True, blank=True)
    attempted_count = models.IntegerField(null=True, blank=True)
    success_rate = models.FloatField(null=True, blank=True)

    @property
    def difficulty(self):
        if self.success_rate is None:
            return None
        if self.success_rate >= 0.85:
            return 'Easy'
        if self.success_rate >= 0.7:
            return 'Medium'
        return 'Hard'

    def __str__(self):
        return f'{self.id}-{self.title}'

    def retrieve_problem_stats(self):
        stats = CSESClient.retrieve_problem_stats(self.id)
        if stats is None:
            return

        self.solved_count = stats.get('solved')
        self.attempted_count = stats.get('attempted')
        self.success_rate = stats.get('success_rate')
        self.save()

    @staticmethod
    def retrieve_problems_stats():
        problems = Problem.objects.all()
        for i, problem in enumerate(problems):
            if problem.solved_count is not None:
                continue
            problem.retrieve_problem_stats()
            print(f'{problem.id} stats retrieved ({i + 1}/{problems.count()})')

    @staticmethod
    def retrieve_problems():
        problems = CSESClient.retrieve_problems()
        for _problem in problems:
            if Problem.objects.filter(id=_problem['id']).exists():
                problem = Problem.objects.get(id=_problem['id'])
            else:
                problem = Problem.objects.create(id=_problem['id'])

            problem.title = _problem['title']
            problem.url = _problem['url']
            problem.category = _problem['category']

        return Problem.objects.all()
