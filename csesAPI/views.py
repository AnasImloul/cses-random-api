from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import Problem, ProblemStatement
from .serializer import ProblemSerializer, ProblemDetailsSerializer, ProblemStatementSerializer
from rest_framework import status
from drf_spectacular.utils import extend_schema


@extend_schema(responses=ProblemSerializer)
@api_view(['GET'])
def get_problems(request):
    problems = Problem.objects.all()
    serializer = ProblemDetailsSerializer(problems, many=True)
    return JsonResponse({'problems': serializer.data}, status=status.HTTP_200_OK)


@extend_schema(responses=ProblemStatementSerializer)
@api_view(['GET'])
def get_problem(request, pk):
    if not Problem.objects.filter(id=pk).exists():
        return JsonResponse({'error': 'Problem not found'}, status=status.HTTP_404_NOT_FOUND)

    problem = Problem.objects.get(id=pk)

    problem.save()

    serializer = ProblemDetailsSerializer(problem)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


@extend_schema(responses=ProblemDetailsSerializer)
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

    serializer = ProblemDetailsSerializer(problem)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


@extend_schema(responses=ProblemStatementSerializer)
@api_view(['GET'])
def get_problem_statement(request, pk):
    if not Problem.objects.filter(id=pk).exists():
        return JsonResponse({'error': 'Problem not found'}, status=status.HTTP_404_NOT_FOUND)

    problem = Problem.objects.get(id=pk)

    if not ProblemStatement.objects.filter(problem=problem).exists():
        return JsonResponse({'error': 'Problem statement not found'}, status=status.HTTP_404_NOT_FOUND)

    problem_statement = ProblemStatement.objects.get(problem=problem)
    serializer = ProblemStatementSerializer(problem_statement)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)
