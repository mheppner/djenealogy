from rest_framework import views, viewsets, filters, exceptions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
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


class TreeView(views.APIView):
    def _build(self, individual, max_depth=5, depth=0):
        """
        Recursive call to return a tree up to the limit of max_dpeth. The
        starting Individual is minimally serialized. Each parent_family is
        also serialized, and each parent_family's husband and wife are
        recursively serialized.
        
        :param individual: an Individual to build a tree for
        :param max_depth: the maximum level in the tree to reach
        :param depth: the current depth level, used internally
        :rtype: dict
        """
        # start with base individual
        if individual is None:
            return None
        
        indv_ser = serializers.TreeIndividualSerializer(individual).data
        
        # recursive case
        if depth < max_depth:
            depth += 1
            
            # initialize list for parent families
            indv_ser['parent_families'] = []
            
            for p in individual.parent_families.all():
                # recursive call to get trees for husband and wife
                husb_ser = self._build(p.husband, max_depth, depth)
                wife_ser = self._build(p.wife, max_depth, depth)
                
                # add recursive parts to family
                fam_ser = serializers.TreeFamilySerializer(p).data
                fam_ser['husband'] = husb_ser
                fam_ser['wife'] = wife_ser
                
                # save serializerd family
                indv_ser['parent_families'].append(fam_ser)
        
        # base case
        return indv_ser
        
    def get(self, request, format=None):
        # get max_depth value and conver to int
        depth = self.request.query_params.get('depth', 5)
        try:
            depth = int(depth)
        except ValueError:
            raise exceptions.ParseError('Depth must be an integer')
        
        # raise errors if depth is too small or large
        if depth < 1:
            raise exceptions.ParseError('Depth must be greater than 0')
        if depth > 10:
            raise exceptions.ParseError('Depth must not exceed 10')
        
        # get individual and build tree
        indv = get_object_or_404(models.Individual, id=self.request.query_params.get('id', None))
        tree = self._build(indv, max_depth=depth)
        return Response(tree)

