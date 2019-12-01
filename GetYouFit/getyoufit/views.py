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

@login_required
def index(request):
	message = ""
	return render(request, "index.html", {"message": message})

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

	if request.method == "POST":
		form = DateForm(request.POST)
		if form.is_valid():
			print("-----------------",form.cleaned_data['startDate'].year)
			result = retrieveDietEntries(form.cleaned_data, request.user.username)			
			entries = result[0]
			total= result[1]
	else:
		form = DateForm()
	
	return render(request, "diet.html", {"form": form, "entries": entries, "total": total})

@login_required
def create_diet(request):
	
	message =""

	if request.method == "POST":
		form = DietForm(request.POST)
		if form.is_valid():
			print("validaidsid")
			message = createDietEntry(form.cleaned_data, request.user.username)
	else:
		form = DietForm()
	
	return render(request, "create-diet-entry.html", {"form": form, "message": message})
