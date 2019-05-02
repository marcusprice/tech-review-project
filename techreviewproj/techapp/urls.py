from django.urls import path
from . import views

#this is a comment
urlpatterns = [
    path('', views.index, name='index'),
    path('gettypes/', views.gettypes, name='types'),
]
