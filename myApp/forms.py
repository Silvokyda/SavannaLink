from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product  


class ContactSellerForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class SignUpForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=15,
        required=True,
        label='Phone Number',  
    )
    class Meta:
        model = User
        fields = ('username', 'phone_number', 'password1', 'password2')

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price']
