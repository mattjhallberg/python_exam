from django.shortcuts import render, redirect
from .models import User, Plan, JoinTrip
import bcrypt
import datetime


def index(request):
	
	return render(request, 'travels/index.html')

def login(request):
	if request.method == "POST":
		username = request.POST["username"]
		userPassword = request.POST["password"]
		if(len(username) < 3 or len(userPassword) < 8):
			print("Username must be greater than 3 characters, and password greater than 8!")
			return redirect('/')
		userPassword = b""+userPassword
		username = User.objects.filter(username = username)
		if not username:
			print("Invalid Username!")
			return redirect('/')
		else:
			username = username[0]
			if bcrypt.hashpw(userPassword.encode(), username.password.encode()) == username.password.encode():
				request.session['user_id'] = username.id
				request.session['name'] = username.name
				print("It Matches!")
			else:
				print("No Match!")
	return redirect('/')

def register(request):
	if request.method == "POST":
		username = request.POST["username"]
		multiUsernameCheck = User.objects.filter(username = username)
		if multiUsernameCheck:
			print "Pick a different name!"
			return redirect('/')
		name = request.POST["name"]
		userPassword = request.POST["password"]
		c_password = request.POST["c_password"]
		if(userPassword == c_password):
			print "Password match!"
		else:
			print "Password does not match!"
			return redirect('/')
		if(len(username) < 3 or len(name) < 3 or len(userPassword) < 8):
			print("Username and Name must be greater than 3 characters, and password greater than 8!")
			return redirect('/')
		if not'username' in request.session:
			request.session['username'] = username
		if not'name' in request.session:
			request.session['name'] = name
		if not'password' in request.session:
			password = b""+userPassword
			request.session['password'] = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
			
		new_user = User.objects.create(
			username = request.session['username'],
			name = request.session['name'],
			password = request.session['password'],
			user_level = 1)
		request.session['user_id'] = new_user.id


	print(User.objects.all())
	return redirect('/')

def add_trip(request):
	return render(request, 'travels/add_trip.html')

def travel_dashboard(request):
	my_plan_query = Plan.objects.filter(user=User.objects.filter(id=request.session['user_id']))
	query_results = Plan.objects.all()
	context = {
		'my_plan' : my_plan_query,
		'all_users': query_results
	}
	return render(request, 'travels/travels.html', context)

def process_trip(request):
	if request.method == "POST":
		destination = request.POST["destination"]
		description = request.POST["description"]
		travel_date_from = request.POST["travel_date_from"]
		travel_date_to = request.POST["travel_date_to"]
		user = User.objects.get(id=request.session['user_id'])
	if destination is not None and destination != '':
		if description is not None and destination != '':

			Plan.objects.create(
			user = user,
			destination = destination,
			plan = description,
			travel_start_date = travel_date_from,
			travel_end_date = travel_date_to)

			return redirect('/travels')
	return render(request, 'travels/add_trip.html')


def destination(request, id):
	if request.method == "GET":
		print "Link clicked"
	query_result = Plan.objects.get(id=id)
	others = JoinTrip.objects.filter(plan = query_result)
	context = {
		'destination_result': query_result,
		'others' : others
	}
	return render(request, 'travels/destination.html',context)

def join_trip(request, id):
	query_result = Plan.objects.get(id=id)
	JoinTrip.objects.create(
		name = request.session['name'],
		plan = query_result)
	return redirect('/travels')

def logout(request):
	request.session.clear()
	return redirect('/')






















