from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from djenealogy import views
from djenealogy import rest

router = routers.DefaultRouter()
router.register(r'individuals', rest.IndividualViewSet)
router.register(r'families', rest.FamilyViewSet)


urlpatterns = patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls, namespace='api')),
    
)
