from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', confirm, name="confirm"),
    path('login', login_attempt, name="login_attempt"),
    path('register', register_attempt, name="register_attempt"),
    path('logout', logout_attempt, name="logout_attempt"),
    path('features', features, name="features"),
    path('about', about, name="about"),
    path('home', home, name="home"),
    path('view_score', view_score, name="view_score"),
    path('api/check_score', check_score, name="check_score"),
    path('<id>', take_quiz, name="take_quiz"),
    path('api/<id>', api_question, name="api_question"),
]
