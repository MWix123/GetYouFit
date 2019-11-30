from django import forms
from .models import Post

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
	
	age = forms.IntegerField(required=False)
	height1 = forms.IntegerField(label="Height:", required=False)
	height2 = forms.IntegerField(label="", required=False)
	weight = forms.FloatField(required=False)
	gender = forms.ChoiceField(label='Gender:', choices=[("M","Male"),("F","Female")], required=False)

	class Meta:
		model = User
		fields = ['username', 'password1', 'password2', 'age', 'height1', 'height2', 'weight', 'gender']

