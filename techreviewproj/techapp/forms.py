from django import forms
from .models import Product, TechType, Review

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields='__all__'

class TechTypeForm(forms.ModelForm):
    class Meta:
        model=TechType
        fields='__all__'
