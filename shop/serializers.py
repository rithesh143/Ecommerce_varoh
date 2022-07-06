from rest_framework import serializers
from .models import (
    Games,
    ActivityBox,
    SpecialBooks,
    KnowledgeCapsule,
    Standard
)


class GamesSerializer(serializers.ModelSerializer):
    copun = serializers.ReadOnlyField(source="copun.id")
    class Meta:
        model = Games
        fields = '__all__'


class ActivityBoxSerializer(serializers.ModelSerializer):
    copun = serializers.ReadOnlyField(source="copun.id")
    class Meta:
        model = ActivityBox
        fields = '__all__'


class SpecialBooksSerializer(serializers.ModelSerializer):
    copun = serializers.ReadOnlyField(source="copun.id")
    class Meta:
        model = SpecialBooks
        fields = '__all__'


class KnowledgeCapsuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeCapsule
        fields = '__all__'

class StandardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Standard
        fields = ['id', 'name',]