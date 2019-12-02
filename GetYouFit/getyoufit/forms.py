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

class TextInput(forms.TextInput):
	input_type = 'text'

class NumberInput(forms.NumberInput):
	input_type = 'number'

class TimeInput(forms.TimeInput):
	input_type = 'time'

class DateForm(forms.Form):
	startDate = forms.DateField(label="Start Date:", widget=DateInput)
	endDate = forms.DateField(label="End Date:", widget=DateInput)

class DietForm(forms.Form):
	date = forms.DateField(label="Date:", widget=DateInput)
	food = forms.CharField(label="Name of food:", max_length=100)
	calories = forms.IntegerField(label="Calories:")

class EditDietForm(forms.Form):
	date = forms.DateField(label="Date:", widget=DateInput)
	food = forms.CharField(label="Name of food:", max_length=100)
	calories = forms.IntegerField(label="Calories:")
	oldFood = forms.CharField(label="Name of food:", max_length=100, widget=TextInput(attrs={'id':'id_food2'}))
	oldCalories = forms.IntegerField(label="Calories:", widget=NumberInput(attrs={'id':'id_calories2'}))

class DeleteDietForm(forms.Form):
	date = forms.DateField(label="Date:", widget=DateInput(attrs={'id':'id_date3'}))
	food = forms.CharField(label="Name of food:", max_length=100, widget=TextInput(attrs={'id':'id_food3'}))
	calories = forms.IntegerField(label="Calories:", widget=NumberInput(attrs={'id':'id_calories3'}))
	single = forms.ChoiceField(choices=[('single','single'),('day','day')], widget=forms.RadioSelect, initial='single')

class WorkoutForm(forms.Form):
	date = forms.DateField(label="Date:", widget=DateInput)
	exerciseName = forms.CharField(label="Name of exercise:", max_length=100)
	calories = forms.IntegerField(label="Calories burned:")
	typeForm = forms.ChoiceField(label="Type of exercise", choices=[('Strength', 'Strength'),('Running','Running')],widget=forms.RadioSelect, initial="Strength")

	# strength only
	muscle = forms.CharField(label="Muscle(s) used:", max_length=50, required=False)
	weight = forms.IntegerField(label="Weight:", help_text="lb", required=False)
	repetitions = forms.IntegerField(label="Number of repetitions:", required=False)
	
	# running only
	duration = forms.CharField(label="Duration:", max_length=20,help_text=" hh:mm:ss",required=False)
	distance = forms.FloatField(label="Distance:",help_text=" in miles", required=False)
