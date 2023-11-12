from django import forms

class ContactSellerForm(forms.Form):

    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
