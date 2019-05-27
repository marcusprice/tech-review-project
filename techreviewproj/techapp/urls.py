from django.urls import path
from . import views

#this is a comment
urlpatterns = [
    path('', views.index, name='index'),
    path('gettypes/', views.gettypes, name='types'),
    path('getproducts/', views.getproducts, name='products'),
    path('productdetails/<int:id>', views.productdetails, name='productdetails'),
    path('newProduct/', views.newProduct, name='newproduct'),  
]
