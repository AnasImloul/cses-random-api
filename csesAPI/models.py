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
    statement = models.TextField(null=True, blank=True)
    input_format = models.TextField(null=True, blank=True)
    output_format = models.TextField(null=True, blank=True)
    time_limit = models.IntegerField(null=True, blank=True)
    memory_limit = models.IntegerField(null=True, blank=True)
    example_input = models.TextField(null=True, blank=True)
    example_output = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.problem.id}-{self.problem.title}'

    def retrieve_problem_statement(self):
        statement = CSESClient.retrieve_problem_statement(self.problem.id)
        if statement is None:
            return

        self.statement = statement.get('statement')
        self.input_format = statement.get('input_format')
        self.output_format = statement.get('output_format')
        self.constraints = statement.get('constraints')
        self.example_input = statement.get('example_input')
        self.example_output = statement.get('example_output')
        self.time_limit = statement.get('time_limit')
        self.memory_limit = statement.get('memory_limit')
        self.save()

    @staticmethod
    def retrieve_problems_statements():
        problems = Problem.objects.all()
        for i, problem in enumerate(problems):
            if ProblemStatement.objects.filter(problem=problem).exists():
                problem_statement = ProblemStatement.objects.get(problem=problem)
            else:
                problem_statement = ProblemStatement.objects.create(problem=problem)

            problem_statement.retrieve_problem_statement()
            print(f'{problem.id} statement retrieved ({i + 1}/{problems.count()})')


class Problem(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=256)
    url = models.CharField(max_length=256)
    category = models.CharField(max_length=256,
                                choices=[(category.name, category.value) for category in ProblemCategory])
    solved_count = models.IntegerField(null=True, blank=True)
    attempted_count = models.IntegerField(null=True, blank=True)

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

    def retrieve_problem_stats(self):
        stats = CSESClient.retrieve_problem_stats(self.id)
        if stats is None:
            return

        print(stats)

        self.solved_count = stats.get('solved')
        self.attempted_count = stats.get('attempted')

        self.save()

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
            problem.category = _problem['category'].upper().replace(' ', '_')
            problem.attempted_count = _problem['attempted']
            problem.solved_count = _problem['solved']

            problem.save()

        return Problem.objects.all()

