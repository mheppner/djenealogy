from rest_framework import viewsets, filters
from rest_framework.response import Response
from djenealogy import models
from djenealogy import serializers


class IndividualViewSet(viewsets.ModelViewSet):
    queryset = models.Individual.objects.select_related().all()
    paginate_by = 10
    paginate_by_param = 'page_size'
    max_paginate_by = 250
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_fields = ('surname', 'given_name',)
    search_fields = ('surname', 'given_name',)
    ordering_fields = ('surname', 'given_name',)
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.IndividualDetailSerializer
        
        return serializers.IndividualSerializer



class FamilyViewSet(viewsets.ModelViewSet):
    queryset = models.Family.objects.select_related().all()
    paginate_by = 10
    paginate_by_param = 'page_size'
    max_paginate_by = 250
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_fields = ('husband__surname', 'husband__given_name', 'wife__surname', 'wife__given_name')
    search_fields = ('husband__surname', 'husband__given_name', 'wife__surname', 'wife__given_name')
    ordering_fields = ('husband__surname', 'husband__given_name', 'wife__surname', 'wife__given_name')
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.FamilyDetailSerializer
        
        return serializers.FamilySerializer

