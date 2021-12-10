from django import forms
from apps.home.models import Customer


class SignUpForm(forms.Form):

    firstname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "first name",
                "class": "form-control"
            }
        ))

    lastname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "last name",
                "class": "form-control"
            }
        ))
    
    gender = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "gender (male or female)",
                "class": "form-control"
            }
        ))
    
    card = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "card num",
                "class": "form-control"
            }
        ))

    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "phone num",
                "class": "form-control"
            }
        ))

    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "email",
                "class": "form-control"
            }
        ))
    
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "address",
                "class": "form-control"
            }
        ))

    

    class Meta:
        model = Customer
        fields = ('phone', 'email', 'address', 'card', 'lastname', 'firstname', 'gender')
