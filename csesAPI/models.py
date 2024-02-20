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


class ProblemStatement(models.Model):

    problem = models.ForeignKey('Problem', on_delete=models.CASCADE)
    statement = models.TextField(null=False, blank=False)
    input_format = models.TextField(null=False, blank=False)
    output_format = models.TextField(null=False, blank=False)
    time_limit = models.IntegerField(null=False, blank=False)
    memory_limit = models.IntegerField(null=False, blank=False)
    constraints = models.TextField(null=False, blank=False)
    example_input = models.TextField(null=False, blank=False)
    example_output = models.TextField(null=False, blank=False)

    def __str__(self):
        return f'{self.problem.id}-{self.problem.title}'

    @staticmethod
    def retrieve_problems_statements():
        problems = Problem.objects.all()
        for i, problem in enumerate(problems):
            if ProblemStatement.objects.filter(problem=problem).exists():
                continue

            statement = CSESClient.retrieve_problem_statement(problem.id)

            problem_statement = ProblemStatement.objects.create(problem=problem, **statement)
            problem_statement.save()


class Problem(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=256)
    url = models.CharField(max_length=256)
    category = models.CharField(max_length=256,
                                choices=[(category.name, category.value) for category in ProblemCategory])
    solved_count = models.IntegerField(null=False)
    attempted_count = models.IntegerField(null=False)

    @property
    def difficulty(self):
        if self.success_rate is None:
            return None
        if self.success_rate >= 0.85:
            return 'Medium'
        if self.success_rate >= 0.7:
            return 'Hard'
        return 'Very Hard'

    @property
    def success_rate(self):
        if self.solved_count is None or self.attempted_count is None:
            return None
        return round(self.solved_count / self.attempted_count if self.attempted_count != 0 else 0, 4)

    def __str__(self):
        return f'{self.id}-{self.title}'

    @staticmethod
    def retrieve_problems():
        problems = CSESClient.retrieve_problems()
        for _problem in problems:
            if Problem.objects.filter(id=_problem['id']).exists():
                continue
            problem = Problem.objects.create(**_problem)
            problem.save()
        return Problem.objects.all()
