from django.contrib import admin
from django.urls import path
from .views import*


urlpatterns = [
    path('home', home, name="home"),
    path('', ConfirmView.as_view(), name="confirm"),
    path('about/',  AboutView.as_view(), name="about"),
    path('features/', FeaturesView.as_view(), name="features"),
    path('chooseUser/', ChooseUserView.as_view(), name="chooseUser"),
    path('logout/', LogoutView.as_view(), name="logout"),
    
    path('teacher_question', teacher_question, name="teacher_question"),
    path('register_teacher', register_teacher, name="register_teacher"),
    path('login_teacher', login_teacher, name="login_teacher"),
    path('teacher_home', teacher_home, name="teacher_home"),
    
    path('register_student', register_student, name="register_student"),
    path('login_student', login_student, name="login_student"),
    
    path('api/check_score', check_score, name="check_score"),
    path('api/<id>', api_question, name="api_question"),
    path('view_score', view_score, name="view_score"),
    path('<id>', take_quiz, name="take_quiz"),
    
    path('success/', SuccessView.as_view(), name="success"),
    path('verify/<auth_token>' , verify , name="verify"),
    path('token/', token_send, name="token_send"),
    path('error/' , error_page , name="error"),
]
