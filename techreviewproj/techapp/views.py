from django.shortcuts import render, get_object_or_404
from .models import TechType, Product, Review

# Create your views here.
def index(request):
    return render(request, 'techapp/index.html')

def gettypes(request):
    type_list=TechType.objects.all()
    return render(request, 'techapp/types.html', {'type_list' : type_list})

def getproducts(request):
    products_list=Product.objects.all()
    return render(request, 'techapp/products.html', {'products_list': products_list})

def productdetails(request, id):
    prod=get_object_or_404(Product, pk=id)
    reviews=Review.objects.filter(product=id).count()
    context={
        'prod' : prod,
        'reviews' : reviews,
    }
    return render(request, 'techapp/productdetails.html', context=context)
