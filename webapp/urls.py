from django.urls import path
from . import views

app_name = "webapp"

urlpatterns = [
	path('', views.home, name="home"),
	path('home', views.home, name="home"),
	path('test/', views.test, name="test"),
	path('signup', views.signup, name="signup"),
	path('signin', views.signin, name="signin"),
	path('signout', views.signout, name="signout"),
]