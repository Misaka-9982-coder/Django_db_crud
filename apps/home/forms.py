from django import forms
from apps.home.models import Customer, Designer
import re

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# 注册 customer 
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
        widget=forms.EmailInput(
            attrs={
                # "value": "email",
                "placeholder": "email",
                "class": "form-control"
            }
        ),
        label="email",
        )
    
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "address",
                "class": "form-control"
            }
        ))


    def clean_lastname(self):  
        lastname = self.cleaned_data.get("lastname")
        if not lastname.isdigit():
            if re.findall(r"^[A-Za-z0-9_\-\u4e00-\u9fa5]+$", lastname):
                return lastname 
            else:
                raise forms.ValidationError('exists unvalidate char') 
        else:
            raise forms.ValidationError("lastname can't be all nums")


    def clean_firstname(self):  
        firstname = self.cleaned_data.get("firstname")
        if not firstname.isdigit():
            if re.findall(r"^[A-Za-z0-9_\-\u4e00-\u9fa5]+$", firstname):
                return firstname
            else:
                raise forms.ValidationError('exists unvalidate char') 
        else:
            raise forms.ValidationError("firstname can't be all nums")


    def clean_gender(self):
        gender = self.cleaned_data["gender"]

        if gender == "male" or gender == "female" :
            return gender
        else:
            raise forms.ValidationError("enter your gender(male or female)")    


    def clean_card(self):  
        card = self.cleaned_data.get("card")
        if not card.isdigit():
            raise forms.ValidationError('exists unvalidate char')
        else:
            return card


    def clean_phone(self):  
        phone = self.cleaned_data.get("phone")
        if not phone.isdigit():
            raise forms.ValidationError('exists unvalidate char')
        else:
            return phone


    def clean_address(self):  
        address = self.cleaned_data.get("address")
        if address.isdigit():
            raise forms.ValidationError("address can't be all nums")
        else:
            return address

    class Meta:
        model = Customer 
        fields = ('phone', 'email', 'address', 'card', 'lastname', 'firstname', 'gender')


# 重置密码
class ResetForm(UserCreationForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Current Password",
                "class": "form-control"
            }
        ))

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "New Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "New Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('password', 'password1', 'password2')