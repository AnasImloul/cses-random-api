from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import Problem
from .serializer import ProblemSerializer
from rest_framework import status


@api_view(['GET'])
def get_problems(request):
    problems = Problem.objects.all()
    serializer = ProblemSerializer(problems, many=True)
    return JsonResponse({'problems': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_problem(request, pk):
    problem = Problem.objects.get(id=pk)
    serializer = ProblemSerializer(problem)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_random_problem(request):
    categories = request.GET.get('category', None)
    if categories:
        problem = Problem.objects.filter(category__in=categories.split(','))
    else:
        problem = Problem.objects

    exclude = request.GET.get('exclude', None)
    if exclude:
        problem = problem.exclude(id__in=exclude.split(','))

    if problem.count() == 0:
        return JsonResponse({'error': 'No problems found'}, status=status.HTTP_404_NOT_FOUND)

    problem = problem.order_by('?').first()
    serializer = ProblemSerializer(problem)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)
