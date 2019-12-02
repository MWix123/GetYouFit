# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import *

from .login import *
from .user_info import *
from .diet import *
from .workouts import *

from datetime import datetime

@login_required
def index(request):
	entries = ""
	calorieMessage = ""
	

	values = {"username": request.user.username, "startDate":datetime.today(), "endDate":datetime.today()}
	result = retrieveDietEntries(values, request.user.username)	
	entries = result[0]
	

	if len(result[1]) == 0:
		entries = "<br /><h4>No Diet Entries entered for today</h4><br />"
	else:
		entries = "<br /><h4>Diet Entries</h4><br /><section id='diet-results'>" + entries + "</section><br />"

	result = retrieveWorkoutEntries(values, request.user.username)			
	
	if len(result[1]) == 0:
		entries = entries + "<h4>No Workout Entries entered for today</h4>"
	else:
		entries = entries + "<h4>Workout Entries</h4><br /><section id='workout-results'>" + result[0] + "</section>"


	calorieMessage = retrieveCalorieInfo(request.user.username)

	return render(request, "index.html", {"entries": entries, "calorieMessage":calorieMessage})

def signup(request):
	message = ""
	
	if request.user.is_authenticated:
		return redirect('index')

	if request.method == "POST":
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			result = createUser(form.cleaned_data)
			
			if result[0]:
				form.save()
				return redirect('index')
			else:
				message = result[1]
	else:
		form = UserRegistrationForm()
	return render(request, "signup.html", {"form": form, "message": message})

@login_required
def profile(request):
	message = ""
	data = get_profile_info(request.user.username)

	if request.method == "POST":
		form = UserProfileForm(request.POST)
		#print(form)
		if form.is_valid():
			result = update_profile_info(form.cleaned_data)
			message = result[1]
			if result[0]:
				u = User.objects.get(username=request.user.username)
				u.set_password(form.cleaned_data['password'])
				u.save()

	else:
		form = UserProfileForm(initial=data)
	
	return render(request, "profile.html", {"form": form, "message": message})

@login_required
def diet(request):
	
	entries = ""
	total = ""
	message = ""

	if request.method == "POST":
		form = DateForm(request.POST)
		editForm = EditDietForm(request.POST)
		deleteForm = DeleteDietForm(request.POST)

		if deleteForm.is_valid():
			print("test3")
			message = deleteDietEntry(deleteForm.cleaned_data, request.user.username)

		if editForm.is_valid():
			print("test 2")
			print("Edit form:",editForm.cleaned_data)
			message = updateDietEntry(editForm.cleaned_data, request.user.username)
		
		if form.is_valid():
			print("test 1")
			result = retrieveDietEntries(form.cleaned_data, request.user.username)			
			entries = result[0]
			total= result[1]

	else:
		form = DateForm()
		editForm = EditDietForm()
		deleteForm = DeleteDietForm()

	return render(request, "diet.html", {"form": form, "editForm":editForm, "deleteForm":deleteForm, "entries": entries, "total": total, "message": message})

@login_required
def create_diet(request):
	
	message =""

	if request.method == "POST":
		form = DietForm(request.POST)
		if form.is_valid():
			message = createDietEntry(form.cleaned_data, request.user.username)
	else:
		form = DietForm()
	
	return render(request, "create-diet-entry.html", {"form": form, "message": message})

@login_required
def workouts(request):
	
	entries = ""
	total = ""
	message = ""

	if request.method == "POST":
		form = DateForm(request.POST)
		editForm = EditWorkoutForm(request.POST)
		deleteForm = DeleteWorkoutForm(request.POST)
		
		if deleteForm.is_valid():
			print("delete form:",deleteForm.cleaned_data)
			message = deleteWorkoutEntry(deleteForm.cleaned_data, request.user.username)			
		if editForm.is_valid():
			print("edit form:", editForm.cleaned_data)
			message = editWorkoutEntry(editForm.cleaned_data, request.user.username)

		if form.is_valid():
			result = retrieveWorkoutEntries(form.cleaned_data, request.user.username)			
			entries = result[0]
			total= result[1]
	else:
		form = DateForm()
		editForm = EditWorkoutForm()
		deleteForm = DeleteWorkoutForm()
	
	return render(request, "workouts.html", {"form": form, "editForm":editForm, "deleteForm":deleteForm, "entries": entries, "total": total, "message": message})

@login_required
def create_workout(request):
	
	message =""

	if request.method == "POST":
		form = WorkoutForm(request.POST)
		if form.is_valid():
			message = createWorkoutEntry(form.cleaned_data, request.user.username)
	else:
		form = WorkoutForm()
	
	return render(request, "create-workout-entry.html", {"form": form, "message": message})
