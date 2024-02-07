from django.db import models
from enum import Enum
from .utils.html import parse_html, find, get_children, get_attribute, to_string
from requests import get


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

    def __str__(self):
        return f'{self.id}-{self.title}'

    class Meta:
        app_label = 'csesAPI'


def import_problems():
    problems = retrieve_problems()
    for problem in problems:
        if Problem.objects.filter(id=problem['id']).exists():
            continue
        Problem.objects.create(id=problem['id'],
                               title=problem['name'],
                               url=problem['url'],
                               category=problem['category'].upper().replace(' ', '_'))


def retrieve_problems():
    url = 'https://cses.fi/problemset/list/'

    source = get(url).content.decode('utf-8')

    tree = parse_html(source)

    CATEGORY_XPATH_TEMPLATE = '/html/body/div[2]/div[2]/div/h2[ID]'
    PROBLEMS_XPATH_TEMPLATE = '/html/body/div[2]/div[2]/div/ul[ID]'

    categories = list()
    i = 2
    while True:
        try:
            category = find(tree, CATEGORY_XPATH_TEMPLATE.replace('ID', str(i))).text

            problems = find(tree, PROBLEMS_XPATH_TEMPLATE.replace('ID', str(i)))
            for child in get_children(problems):
                href = get_attribute(find(child, 'a'), 'href')
                url = f'https://cses.fi{href}'
                _id = href.split('/')[-1]
                name = find(child, 'a').text
                categories.append({'id': _id, 'name': name, 'url': url, 'category': category})
            i += 1
        except:
            break
    return categories
