from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Req
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    blood_choices = (('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-'))
    blood_group=forms.ChoiceField(choices=blood_choices)
    class Meta:
        model = Profile
        fields = ('email','blood_group',)

class RequestForm(forms.ModelForm):
    username1 = forms.CharField()
    username2 = forms.CharField()
    text = forms.CharField()
    class Meta:
         model = Req
         fields = {'username1','username2', 'text'}

