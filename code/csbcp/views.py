from django.shortcuts import render, redirect
from .models import *


def loginView(request):
	if request.method == 'POST':
		print('post on login')
	return render(request, 'login.html')


def mainView(request):
	return render(request, 'main.html')


def signupView(request):
	return render(request, 'signup.html')


def sendMessageView(request):
	return render(request, 'send-message.html')


def adminView(request):
	return render(request, 'admin.html')


