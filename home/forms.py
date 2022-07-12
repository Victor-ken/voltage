from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . models import *

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['full_name','email','message']





class SignupForm(UserCreationForm):
    username = forms.CharField(max_length= 50)
    first_name = forms.CharField(max_length= 100)
    last_name = forms.CharField(max_length= 100)
    email = forms.CharField(max_length= 150)


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

STATE = [
    ('Abia', 'Abia'),
    ('Delta', 'DElta'),
    ('Jigawa', 'Jigawa'),
]

class ProfileUpdate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name','last_name','phone','email','address','state','pix']
        widgets ={
            'first_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}),
            'phone':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}),
            'email':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}),
            'address':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Home Address'}),
            'state':forms.Select(attrs={'class':'form-control', 'placeholder':'state'}, choices=STATE),
            'pix':forms.TextInput(attrs={'class':'form-control'}),
        }

class Shopcart(forms.ModelForm):
    class Meta:
        model = Shopcart
        fields = ['quantity']