from django.shortcuts import render
from .models import TechType, Product, Review

# Create your views here.
def index(request):
    return render(request, 'techapp/index.html')

def gettypes(request):
    type_list=TechType.objects.all()
    return render(request, 'techapp/types.html', {'type_list' : type_list})
