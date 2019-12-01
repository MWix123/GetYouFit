from django import forms
from .models import Post

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
	
	age = forms.IntegerField(required=False)
	height1 = forms.IntegerField(label="Height:", required=False, help_text="feet")
	height2 = forms.IntegerField(label="", required=False, help_text="inches")
	weight = forms.FloatField(required=False, help_text="lb")
	gender = forms.ChoiceField(label='Gender:', choices=[("M","Male"),("F","Female")], required=False)

	class Meta:
		model = User
		fields = ['username', 'password1', 'password2', 'age', 'height1', 'height2', 'weight', 'gender']

class UserProfileForm(forms.ModelForm):

	username = forms.CharField(max_length=50,required=False, help_text="")
	password = forms.CharField(max_length=100,required=False)
	age = forms.IntegerField(required=False)
	height1 = forms.IntegerField(label="Height:", required=False, help_text="feet")
	height2 = forms.IntegerField(label="\t", required=False, help_text="inches")
	weight = forms.FloatField(required=False, help_text="lb")
	gender = forms.ChoiceField(label='Gender:', choices=[("M","Male"),("F","Female")], required=False)

	class Meta:
		model = Post
		#fields = ('textarea',)
		fields = ('username', 'password', 'age', 'height1', 'height2', 'weight', 'gender')

class DateInput(forms.DateInput):
	input_type = 'date'

class DateForm(forms.Form):
	startDate = forms.DateField(label="Start Date:", widget=DateInput)
	endDate = forms.DateField(label="End Date:", widget=DateInput)

class DietForm(forms.Form):
	date = forms.DateField(label="Date:", widget=DateInput)
	food = forms.CharField(label="Name of food:", max_length=100)
	calories = forms.IntegerField(label="Calories:")
