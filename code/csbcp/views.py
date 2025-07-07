from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *


def loginView(request):
	if request.method == 'POST':
		username = request.POST["username"]
		password = request.POST["password"]

		if not username or not password:
			return redirect("/")
		
		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect("/main")
		else:
			return redirect("/")

	return render(request, 'login.html')


def signupView(request):
	if request.method == 'POST':
		username = request.POST["username"]
		email = request.POST["email"]
		password = request.POST["password"]

		if not username or not password or not email:
			print('empty')
			print(username)
			print(email)
			print(password)
			return redirect("/signup")
			
		if User.objects.filter(username=username).exists():
			print('exists')
			return redirect("/signup")
	
		user = User.objects.create_user(username=username, email=email, password=password)
		user.save()

		return redirect("/")

	return render(request, 'signup.html')


@login_required
def mainView(request):
	return render(request, 'main.html')


@login_required
def sendMessageView(request):
	return render(request, 'send-message.html')


@login_required
def adminView(request):
# fix 2: remove commenting below
# 	if not request.user.is_superuser:
# 		return redirect("/main")
	return render(request, 'admin.html')


@login_required
def logoutView(request):
	logout(request)
	return redirect("/")


