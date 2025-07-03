from django.shortcuts import render, redirect
from .models import *


def signupView(request):
	print('---------------signupView')
	return render(request, 'signup.html')

