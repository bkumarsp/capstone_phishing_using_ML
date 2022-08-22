
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

#import custom user model
from .models import AppUserModel

# Testing url 
def test(request):
	return HttpResponse('<h1>Testing, AquaPhish</h1>')


# Main home Page for all users: index.html
def home(request):
	return render(request, "Web/index.html") #correction required


# Dashboard page for logged in users
def dashboard(request):
	if request.method == "POST":
		vicitm_id = request.POST["victim"]
		print(vicitm_id)
	if request.user.is_authenticated: #illegal access
		return render(request, "Web/dashboard.html")
	else:
		return redirect("/home")
	

def adminDashboard(request):
	if request.method == "POST":
		# TODO: Verify student credentials
		print("Student verification approval granted.")

	if request.user.is_authenticated: #illegal access
		return render(request, "Web/adminDashboard.html")
	else:
		return redirect("/home")
	

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

		# Input Validations for all users
		if User.objects.filter(username=SRN):
			messages.error(request, "SRN already exists!")
			return redirect("/home")
		if User.objects.filter(email=email):
			messages.error(request, "Email already registered!")
			return redirect("/home")
		if len(SRN) > 15:
			messages.error(request, "Username must be under 15 characters")
			return redirect("/home")
		if pass1 != pass2:
			messages.error(request, "Passwords didn't match")
			return redirect("/home")
		if not SRN.isalnum():
			messages.error(request, "SRN must be Alpha-Numeric!")
			return redirect("/home")


	### Create a custom user
		CustomAppUser = AppUserModel(SRN=SRN, email=email)
		CustomAppUser.first_name = fname
		CustomAppUser.last_name = lname
		CustomAppUser.Role = role
		CustomAppUser.Institution_code = institution

		CustomAppUser.save()

	### Custom user creation ends here


	#### Create a user auth system
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
		Role = request.POST['role'] #TODO: not necessary to be taken as input
		
		AppUser = authenticate(username=SRN, password=pass1 )

		if AppUser is not None:
			CustomUser = AppUserModel.objects.get(SRN=AppUser.username)
			if CustomUser.Role != Role: #user validation
				messages.error(request, "User not registered for "+Role+" role!")
				return redirect("/home")

			#Validated user, ready to login
			login(request=request, user=AppUser)
			

			fullName = AppUser.first_name + " " + AppUser.last_name
			Institution_code = CustomUser.Institution_code
			userRole = CustomUser.Role
			
			requestToValidate = None
			
			if(userRole == "Admin"): #redirect to adminDashboard
				requestToValidate = AppUserModel.objects.filter(Institution_code=Institution_code, isActive = False, Role="Student").values()
				return render(request, "Web/adminDashboard.html", {"fullname": fullName, "institution_code": Institution_code, "requestToValidate": requestToValidate, "role": Role})

			elif(userRole == "Student"): #redirect to dashboard
				return render(request, "Web/dashboard.html", {"fullname": fullName, "institution_code": Institution_code, "role": userRole})

				
			# TODO: fix index.html page, Add some valid features
			return render(request, "Web/index.html", {"fname": fullName, "institution_code": Institution_code, "requestToValidate": requestToValidate})

		else:
			messages.error(request, "Invalid Credentials!")
			return redirect("/home")

	return render(request, "authentication/signin.html")


def signout(request):
	logout(request)
	messages.success(request, "Logged out successfully")
	return redirect('/home')

