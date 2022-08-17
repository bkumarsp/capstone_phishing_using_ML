
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Testing url 
def test(request):
	return HttpResponse('<h1>Testing, AquaPhish</h1>')


# Main home Page : index.html
def home(request):
	return render(request, "Web/index.html") #correction required


# Webapp user funtions


def signup(request):

	if request.method == "POST":
		fname = request.POST['fname']
		lname = request.POST['lname']
		email = request.POST['email']
		SRN = request.POST['SRN'] # === Username
		role = request.POST['role']
		institution = request.POST['institution']
		pass1 = request.POST['password']
		pass2 = request.POST['confirmpassword']

	# Input Validations
		if User.objects.filter(username=SRN):
			messages.error(request, "SRN already exists!")
			return redirect("/home")
		if User.objects.filter(email=email):
			messages.error(request, "Email already registered!")
			return redirect("/home")
		if len(SRN) > 12:
			messages.error(request, "Username must be under 12 characters")
			return redirect("/home")
		if pass1 != pass2:
			messages.error(request, "Passwords didn't match")
			return redirect("/home")
		if not SRN.isalnum():
			messages.error(request, "SRN must be Alpha-Numeric!")
			return redirect("/home")

		

		# Create a user
		AppUser = User.objects.create_user(SRN, email, pass1)
		AppUser.first_name = fname
		AppUser.last_name = lname

		# AppUser.SRN = SRN
		# AppUser.role = role
		# AppUser.institution = institution

		AppUser.save()

		# print success message
		messages.success(request, "Your account has been successfully created.")

		return redirect("/signin")


	return render(request, "authentication/signup.html")


def signin(request):
	if request.method == "POST":
		SRN = request.POST['SRN'] # === Username
		pass1 = request.POST['password']
		
		AppUser = authenticate(username=SRN, password=pass1 )
		if AppUser is not None:
			login(request=request, user=AppUser)
			fname = AppUser.first_name
			return render(request, "Web/index.html", {"fname": fname})

		else:
			messages.error(request, "Invalid Credentials!")
			return redirect("/home")

	return render(request, "authentication/signin.html")


def signout(request):
	logout(request)
	messages.success(request, "Logged out successfully")
	return redirect('/home')

