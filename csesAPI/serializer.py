from rest_framework.serializers import ModelSerializer
from .models import Problem


class ProblemSerializer(ModelSerializer):
    class Meta:
        model = Problem
        fields = ['id', 'title', 'url', 'category']


class ProblemDetailsSerializer(ModelSerializer):
    class Meta:
        model = Problem
        fields = ['id',
                  'title',
                  'url',
                  'category',
                  'difficulty',
                  'solved_count',
                  'attempted_count',
                  'success_rate']
