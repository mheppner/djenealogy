from rest_framework import serializers
from rest_framework import pagination
from djenealogy import models


class IndividualSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Individual
        exclude = (
            'notes',
        )


class IndividualEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IndividualEvent


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Family
        exclude = (
            'notes',
        )
    
    husband = IndividualSerializer(read_only=True)
    wife = IndividualSerializer(read_only=True)


class FamilyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Family
    
    children = IndividualSerializer(many=True, read_only=True)
    husband = IndividualSerializer(read_only=True)
    wife = IndividualSerializer(read_only=True)


class IndividualDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Individual
    
    events = IndividualEventSerializer(many=True, read_only=True)
    families = FamilyDetailSerializer(many=True, read_only=True)
    parents = IndividualSerializer(many=True, read_only=True)
    mother = IndividualSerializer(read_only=True)
    father = IndividualSerializer(read_only=True)
    siblings = IndividualSerializer(many=True, read_only=True)
    spouses = IndividualSerializer(many=True, read_only=True)

        