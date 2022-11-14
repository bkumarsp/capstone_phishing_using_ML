import re
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


import pandas as pd

#import custom user model
from .models import AppUserModel

#import backend processing files
from templates.backend.DataScrapingModel import scrapeWebpage
from templates.backend.EmailSpamDetector import emailSpamDetector
from templates.backend.EmailMicroService import smtpMail_microservice


##### imports end here ##############

SPAM_FILE =  pd.read_csv("D:\\CapstoneProject\\Btech\\project\\workspace\\"+"aquaphish\\static\\spamResources\\spam.csv", encoding='utf-8')

# Testing url 
def test(request):
	return HttpResponse('<h1>Testing, AquaPhish</h1>')


# Main home Page for all users: index.html
def home(request):
	return render(request, "Web/dashboard.html")


# Dashboard page for logged in users
def dashboard(request):

	'''	to remove
	if request.method == "POST":
		vicitm_id = request.POST["victim"]
		print(vicitm_id)
		if(vicitm_id is None):
			scrapingStatus = scrapeWebpage()
		else:
			scrapingStatus = scrapeWebpage(victimId=vicitm_id)
		print(scrapingStatus)
	'''

	if request.user.is_authenticated: 
		AppUser = request.user
		CustomUser = AppUserModel.objects.get(SRN=AppUser.username)

		# User Attributes
		fullName = AppUser.first_name + " " + AppUser.last_name
		Institution_code = CustomUser.Institution_code
		userRole = CustomUser.Role

		if(userRole =="Student"):
			return render(request, "Web/dashboard.html", {"fullname": fullName, "institution_code": Institution_code, "role": userRole})
		elif(userRole=="Admin"):
			return redirect("/adminDashboard")

		# TODO: redirect to some error page(technical fault)
		return render(request, "Web/dashboard.html")

	else: #illegal access
		return redirect("/home")
	

def adminDashboard(request):
	
	if request.method == "POST":
		verifiedSRNs = request.POST.getlist("verifyUser[]")

		for SRN in verifiedSRNs:
			VerifyStudent = AppUserModel.objects.get(SRN=SRN)
			VerifyStudent.isActive = True 
			VerifyStudent.save()


		print("Student verification approval granted for", verifiedSRNs)

	if request.user.is_authenticated: #illegal access

		AppUser = request.user
		CustomUser = AppUserModel.objects.get(SRN=AppUser.username)

		# User Attributes
		fullName = AppUser.first_name + " " + AppUser.last_name
		Institution_code = CustomUser.Institution_code
		userRole = CustomUser.Role
		

		requestToValidate = None
			
		if(userRole == "Admin"): #redirect to adminDashboard
			requestToValidate = AppUserModel.objects.filter(Institution_code=Institution_code, isActive = False, Role="Student").values()
			return render(request, "Web/adminDashboard.html", {"fullname": fullName, "institution_code": Institution_code, "requestToValidate": requestToValidate, "role": userRole})

		elif userRole=="Student":
			return redirect("/dashboard")

		# TODO: redirect to some error page(technical fault)
		return render(request, "Web/adminDashboard.html")


	else:
		return redirect("/home")
	
def automaticPhishingLaunch(request):
	if request.method == "POST":
		if "victim_email" in request.POST:
			victim_email = request.POST['victim_email']
		else:
			return HttpResponse("invalid victim email...")

		if "victim_number" in request.POST:
			victim_number = request.POST['victim_number']
		
		emailBody = "Hello"
		if "emailBody" in request.POST:
			emailBody = request.POST['emailBody']
		else:
			return HttpResponse("invalid email text...")
		
		# spamFile = pd.read_csv("D:\\CapstoneProject\\Btech\\project\\workspace\\"+"aquaphish\\static\\spamResources\\spam.csv", encoding='utf-8')
		# resultScored, email_class = emailSpamDetector(spamFile, emailBody)
		
		# print(resultScored, email_class)
		if victim_email == '':
			print("Some data missing")
		else:
			# send mail
			email_status = smtpMail_microservice(emailTo=victim_email, emailSubject="Automatic phishing attack", emailBody=emailBody)
			print(email_status)	

			# if email_status == "success":
			# 	res = "<p>Model score: " + str(round(resultScored, 4)*100) +"</p><br><p>Email Classification: "+str(email_class)+"</p><br><p>Email sent to: "+victim_email+"</p><br><p>Status: Success</p><br>"
				
			return HttpResponse(email_status)	

	if request.user.is_authenticated: 
		AppUser = request.user
		CustomUser = AppUserModel.objects.get(SRN=AppUser.username)

		# User Attributes
		fullName = AppUser.first_name + " " + AppUser.last_name
		Institution_code = CustomUser.Institution_code
		userRole = CustomUser.Role

		if(userRole =="Student"):
			return render(request, "Web/automaticPhishing.html", {"fullname": fullName, "institution_code": Institution_code, "role": userRole, "scrapedDataFreq": ""})
		elif(userRole=="Admin"):
			return redirect("/adminDashboard")

		# TODO: redirect to some error page(technical fault)
		return render(request, "Web/dashboard.html")


#user specific functions
def automaticPhishing(request):
	# form submission handler
	if request.method == "POST":
		if "victim" in request.POST:
			vicitm_id = request.POST["victim"]
		else:
			vicitm_id = ""

		if "attackVector" in request.POST:
			attackVector = request.POST["attackVector"]
		else:
			attackVector = ""

		print(vicitm_id)

		scrapingResult = None

		staticData = {
			'Aditya': {'social': {'aaha_chat': ['https://www.aahachat.org/profile/Aditya/'], 'about.me': ['https://about.me/Aditya'], 'Airliners': ['https://www.airliners.net/user/Aditya/profile'], 'allmylinks': ['https://allmylinks.com/Aditya']}, 'finance': {'ADVFN': ['https://uk.advfn.com/forum/profile/Aditya']}, 'hobby': {'Archive Of Our O..': ['https://archiveofourown.org/users/Aditya']}, 'tech': {'Arduino': ['https://create.arduino.cc/projecthub/Aditya']}, 'gaming': {'ArmorGames': ['https://armorgames.com/user/Aditya']}, 'music': {'Avid Community': ['https://community.avid.com/members/Aditya/default.aspx']}},
			'bhuvantej': {'social': {'Clubhouse': ['https://www.clubhouse.com/@bhuvantej'], 'Disqus': ['https://disqus.com/by/bhuvantej/'], 'likeevideo': ['https://likee.video/@bhuvantej']}, 'hobby': {'Duolingo': ['https://www.duolingo.com/profile/bhuvantej']}, 'gaming': {'Fortnite Tracker': ['https://fortnitetracker.com/profile/all/bhuvantej'], 'game_debate': ['https://www.game-debate.com/profile/bhuvantej']}, 'coding': {'GitHub': ['https://github.com/bhuvantej'], 'hackerearth': ['https://www.hackerearth.com/@bhuvantej'], 'kaggle': ['https://www.kaggle.com/bhuvantej']}},
			'Elonmusk':{'hobby': {'247sports': ['https://247sports.com/User/Elonmusk/']}, 'finance': {'ADVFN': ['https://uk.advfn.com/forum/profile/Elonmusk']}, 'social': {'Albicla': ['https://albicla.com/Elonmusk']}, 'gaming': {'Apex Legends': ['https://apex.tracker.gg/apex/profile/origin/Elonmusk/overview'], 'Bandcamp': ['https://apex.tracker.gg/apex/profile/origin/Elonmusk/overview'], 'BIGO Live': ['https://www.bigo.tv/user/Elonmusk']}, 'music': {'Bandcamp': ['https://bandcamp.com/Elonmusk'], 'Bandlab': ['https://www.bandlab.com/Elonmusk'], 'BIGO Live': ['https://www.bandlab.com/Elonmusk']}},
			'Bharath': {'social': {'about.me': ['https://www.aahachat.org/profile/bharath/', 'https://about.me/bharath'], 'Airliners': ['https://www.airliners.net/user/bharath/profile']}, 'finance': {'ADVFN': ['https://uk.advfn.com/forum/profile/bharath']}, 'blog': {'Ameblo': ['https://ameblo.jp/bharath']}, 'gaming': {'Apex Legends': ['https://apex.tracker.gg/apex/profile/origin/bharath/overview']}, 'tech': {'Arduino': ['https://create.arduino.cc/projecthub/bharath']}},
			'Vyshak': {'music': {'Bandlab': ['https://www.bandlab.com/Vyshak']}, 'blog': {'Blogspot': ['http://Vyshak.blogspot.com']}},
			'Mark Zuckerberg': {'coding': {'codeforces': ['https://codeforces.com/profile/mark zuckerberg']}, 'social': {'Destructoid': ['https://www.destructoid.com/?name=mark zuckerberg'], 'easyen': ['https://easyen.ru/index/8-0-mark zuckerberg'], 'fotka': ['https://fotka.com/profil/mark zuckerberg'], 'Geocaching': ['https://www.geocaching.com/p/?u=mark zuckerberg'], 'mastodon_api': ['https://mastodon.social/api/v2/search?q=mark zuckerberg'], 'megamodels.pl': ['http://megamodels.pl/mark zuckerberg']}, 'hobby': {'instructables': ['https://www.instructables.com/member/mark zuckerberg/']}, 'misc': {'Internet Archive..': ['https://archive.org/search.php?query=mark zuckerberg']}},
			
			'Any': {'social': {'Clubhouse': ['https://www.clubhouse.com/@bhuvantej'], 'Disqus': ['https://disqus.com/by/bhuvantej/'], 'likeevideo': ['https://likee.video/@bhuvantej']}, 'hobby': {'Duolingo': ['https://www.duolingo.com/profile/bhuvantej']}, 'gaming': {'Fortnite Tracker': ['https://fortnitetracker.com/profile/all/bhuvantej'], 'game_debate': ['https://www.game-debate.com/profile/bhuvantej']}, 'coding': {'GitHub': ['https://github.com/bhuvantej'], 'hackerearth': ['https://www.hackerearth.com/@bhuvantej'], 'kaggle': ['https://www.kaggle.com/bhuvantej']}},
			}

		if(vicitm_id is None or vicitm_id=="" and attackVector == ""):
			# scrape default user data is "Aditya"
			# scrapingResult = scrapeWebpage()
			scrapingResult = staticData['bhuvantej']

		elif attackVector != "":

			emailText = {
				'social': 'Sign in to your facebook account and win exiting meta rewards.',
				'music': 'Check out this new music releases.',
				'gaming': 'Clash of clans have released a new update! Upgrade your townhall to level 15 using these FREE GEMS.',
				'coding': 'Hey coder, start todays coding problems and stand a chance to win exciting rewards',
			}
			
			EmailBody = "Your activity in " + attackVector + " sector is unsecure!"
			if attackVector in emailText:
				EmailBody = emailText[attackVector]
				
			modelScore, emailClass = emailSpamDetector(SPAM_FILE, EmailBody)
			print(EmailBody)
			res = {
				"domain": str(attackVector).capitalize(),
				"score": str(round(modelScore, 4)*100),
				"emailClass": str(emailClass[-1]).capitalize(),
			}
			# res = "<p>Chosen Domain: " + str(attackVector) + "<br><p>Model score: " + str(round(modelScore, 4)*100) +"</p><br><p>Email Classification: "+str(emailClass)+"</p><br>"
			
			return render(request, "Web/automaticPhishingLaunch.html", {"ResultData": res, "EmailBody" : EmailBody})

		
		else:
			print("Scraping", vicitm_id)
			scrapingResult = scrapeWebpage(victimId=vicitm_id)
			

		
		if scrapingResult == None or len(scrapingResult) <= 0:
			print("Python scarping is not working due to internet issue: Loading static data from database.")
			
			if vicitm_id in staticData:
				scrapingResult = staticData[vicitm_id]
			else:
				scrapingResult = staticData['Any']

			
		resultSize = 0
		for res in scrapingResult:
			resultSize += len(scrapingResult[res])

		# calculating the resulting category frequencies.
		Category_frequency = {}
		
		for category in scrapingResult:
			if category not in Category_frequency:
				Category_frequency[category] = len(scrapingResult[category])
			else:
				Category_frequency[category] += len(scrapingResult[category])

		for freq in Category_frequency:
			Category_frequency[freq] = round(Category_frequency[freq]/resultSize, 2)

		print("Frequency: ",Category_frequency)

		return render(request, "Web/automaticPhishing.html", {"scrapedDataFreq": Category_frequency, "victim": vicitm_id, "result": scrapingResult})




	if request.user.is_authenticated: 
		AppUser = request.user
		CustomUser = AppUserModel.objects.get(SRN=AppUser.username)

		# User Attributes
		fullName = AppUser.first_name + " " + AppUser.last_name
		Institution_code = CustomUser.Institution_code
		userRole = CustomUser.Role

		if(userRole =="Student"):
			return render(request, "Web/automaticPhishing.html", {"fullname": fullName, "institution_code": Institution_code, "role": userRole, "scrapedDataFreq": ""})
		elif(userRole=="Admin"):
			return redirect("/adminDashboard")

		# TODO: redirect to some error page(technical fault)
		return render(request, "Web/dashboard.html")

def manualPhishing(request):
	if request.method == "POST":
		vicitm_mail = request.POST["victimMail"]
		vicitm_number = request.POST["victimNumber"]
		vicitm_emailSubject = request.POST["emailSubject"]
		vicitm_emailBody = request.POST["emailBody"]
		
		
		if(vicitm_number == ''):
			vicitm_number = 0

		print("Data collected: ", vicitm_mail, vicitm_number, vicitm_emailSubject, vicitm_emailBody)
		
		spamFile = pd.read_csv("D:\\CapstoneProject\\Btech\\project\\workspace\\"+"aquaphish\\static\\spamResources\\spam.csv", encoding='utf-8')
		resultScored, email_class = emailSpamDetector(spamFile, vicitm_emailBody)
		
		print(resultScored, email_class)
		if vicitm_mail == '' or vicitm_emailSubject == '' or vicitm_emailBody == '':
			print("Some data missing")
		else:
			# send mail
			email_status = smtpMail_microservice(emailTo=vicitm_mail, emailSubject=vicitm_emailSubject, emailBody=vicitm_emailBody)
			print(email_status)	

			if email_status == "success":
				res = "<p>Model score: " + str(round(resultScored, 4)*100) +"</p><br><p>Email Classification: "+str(email_class)+"</p><br><p>Email sent to: "+vicitm_mail+"</p><br><p>Status: Success</p><br>"
				
				return HttpResponse(res)		
		

	if request.user.is_authenticated: 
		AppUser = request.user
		CustomUser = AppUserModel.objects.get(SRN=AppUser.username)

		# User Attributes
		fullName = AppUser.first_name + " " + AppUser.last_name
		Institution_code = CustomUser.Institution_code
		userRole = CustomUser.Role

		if(userRole =="Student"):
			return render(request, "Web/manualPhishing.html", {"fullname": fullName, "institution_code": Institution_code, "role": userRole})
		elif(userRole=="Admin"):
			return redirect("/adminDashboard")

		# TODO: redirect to some error page(technical fault)
		return render(request, "Web/dashboard.html")



# Webapp user-login funtions
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
			if CustomUser.isActive == False and Role == "Student":
				messages.error(request, "Account is inactive! Please contact your institute admin.")
				return redirect("/home")

			#Validated user, ready to login
			login(request=request, user=AppUser)
			
			fullName = AppUser.first_name + " " + AppUser.last_name
			Institution_code = CustomUser.Institution_code
			userRole = CustomUser.Role
			
			requestToValidate = None
			
			if(userRole == "Admin"): #redirect to adminDashboard
				return redirect("/adminDashboard")
				
			elif(userRole == "Student"): #redirect to dashboard
				return redirect("/dashboard")
				
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




# urls to access social media cloned pages
def cloned_instagram(request):
	return render(request, "Web/clonedLoginPages/instaClone.html")

def cloned_facebook(request):
	return render(request, "Web/clonedLoginPages/facebookClone.html")

def cloned_twitter(request):
	return render(request, "Web/clonedLoginPages/twitterClone.html")