from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/graph/', views.api_graph, name='api_graph'),
    path('api/find-path/', views.find_path, name='find_path'),
    path('api/compare/', views.compare_algorithms, name='compare_algorithms'),
]
