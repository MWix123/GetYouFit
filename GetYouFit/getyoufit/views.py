# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserRegistrationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .login import *

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

