# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm

from .login import *

def index(request):
	formattedEquation = ""
	
	if request.method == "POST":
		loginForm = LoginForm(request.POST)
		if loginForm.is_valid():
			formattedEquation = createUser(loginForm.cleaned_data["textarea"])
	else:
		loginForm = LoginForm()
	return render(request, "index.html", {"form": loginForm, "formattedEquation": formattedEquation})

def login(request):
	formattedEquation = ""

	if request.method == "POST":
		loginForm = LoginForm(request.POST)
		if loginForm.is_valid():
			formattedEquation = loginUser(loginForm.cleaned_data["textarea"])
	else:
		loginForm = LoginForm()


	return render(request, "login.html", {"form": loginForm, "formattedEquation": formattedEquation})
