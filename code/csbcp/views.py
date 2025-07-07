from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import *
import sqlite3


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

# Fix 1 part 3 and fix 2: remove commenting from here..
#	if request.method == 'get':
#		Message.objects.create(user=request.user, content=request.POST['content'])
#		return redirect("/main/")
#
# .. to here and comment or delete from here

	content = request.GET.get('content')
	conn = sqlite3.connect('db.sqlite3')
	cursor = conn.cursor()
	query = f"""
	INSERT INTO csbcp_message (user_id,content)
	VALUES ({request.user.id}, '{content}');
	"""
	cursor.executescript(query)
	conn.commit()
	conn.close()

# to here

	messages = Message.objects.all()
	return render(request, 'main.html', {'messages': messages})


@login_required
def sendMessageView(request):
	return render(request, 'send-message.html')


@login_required
def adminView(request):
# fix 3: remove commenting below
# 	if not request.user.is_superuser:
# 		return redirect("/main")
	return render(request, 'admin.html')


@login_required
def logoutView(request):
	logout(request)
	return redirect("/")


