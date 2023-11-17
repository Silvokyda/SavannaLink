from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, UserProfile


class ContactSellerForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['location', 'company_name', 'position', 'work_number', 'mobile_number', 'email_address', 'work_address', 'current_password', 'new_password', 'make_account_public']


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
    quantity = forms.IntegerField(label='Quantity', initial=1, min_value=1)

    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'quantity', 'image']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
