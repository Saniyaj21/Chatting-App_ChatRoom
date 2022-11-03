from dataclasses import fields
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from tkinter import Widget
from django.forms import ModelForm

from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participents', ]
        labels={
            'name':'Room Name',
            'password':'Enter Password',
        }

        widgets={
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'password': forms.TextInput(attrs={'class':'form-control'}),
        }
class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']        

        widgets ={
            'username':forms.TextInput(attrs={'id':'form-input1'}),
            'password1':forms.TextInput(attrs={'id':'id_password1'}),
            'password2':forms.TextInput(attrs={'id':'id_password2'}),
        }

