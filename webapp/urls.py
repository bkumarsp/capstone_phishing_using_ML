from django.urls import path
from . import views

app_name = "webapp"

urlpatterns = [
	path('', views.home, name="home"),
	path('test/', views.test, name="test"),

	# basic app urls
	path('home', views.home, name="home"),
	path('dashboard', views.dashboard, name="dashboard"),
	path('adminDashboard', views.adminDashboard, name="adminDashboard"),

	# user specific urls
	path('automaticMode', views.automaticPhishing, name='automaticPhishing'),
	path('automaticAttackLaunch', views.automaticPhishingLaunch, name='automaticPhishingLaunch'),
	path('manualMode', views.manualPhishing, name='manualPhishing'),

	# login system
	path('signup', views.signup, name="signup"),
	path('signin', views.signin, name="signin"),
	path('signout', views.signout, name="signout"),

	# cloned sites for launching phishing
	path('cloned/instagram', views.cloned_instagram, name="cloned_instagram"),
	path('cloned/facebook', views.cloned_facebook, name="cloned_facebook"),
	path('cloned/twitter', views.cloned_twitter, name="cloned_twitter"),
]