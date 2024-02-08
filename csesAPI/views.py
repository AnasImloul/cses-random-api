from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import Problem
from .serializer import ProblemSerializer, ProblemDetailsSerializer
from rest_framework import status


@api_view(['GET'])
def get_problems(request):
    problems = Problem.objects.all()
    serializer = ProblemSerializer(problems, many=True)
    return JsonResponse({'problems': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_problem(request, pk):
    if not Problem.objects.filter(id=pk).exists():
        return JsonResponse({'error': 'Problem not found'}, status=status.HTTP_404_NOT_FOUND)

    problem = Problem.objects.get(id=pk)

    if problem.success_rate is None:
        problem.success_rate = problem.retrieve_success_rate()
        problem.save()

    serializer = ProblemDetailsSerializer(problem)
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

    if problem.success_rate is None:
        problem.success_rate = problem.retrieve_success_rate()
        problem.save()

    serializer = ProblemDetailsSerializer(problem)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)
