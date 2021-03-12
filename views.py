from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Profile
from django.views import View
from .forms import CreateQuestionForm
from .models import Question
from .models import* 
import json
import uuid


#login for teacher.
def login_teacher(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == '':
            messages.success(request, 'Username is required')
            return redirect('login_teacher')
        
        if password == '':
            messages.success(request, 'Password is required')
            return redirect('login_teacher')

        user_teacher = User.objects.filter(username = username).first()
        if user_teacher is None:
            messages.success(request, 'User not found.')
            return redirect('login_teacher')
        
        
        profile_teacher= Profile.objects.filter(user = user_teacher ).first()

        if not profile_teacher.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('login_teacher')
        

        user_is_teacher = authenticate(username = username , password = password)
        if user_is_teacher is None:
            messages.success(request, 'Wrong password.')
            return redirect('login_teacher')
        
        login(request , user_is_teacher)
        return redirect('teacher_home')

    return render(request , 'login_teacher.html')

def register_teacher(request):

    if request.method == 'POST':
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l-name')
        username = request.POST.get('username')
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)

        try:
            if User.objects.filter(username = username).first():
                messages.success(request, 'Username is taken.')
                return redirect('register_teacher.html')

            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is taken.')
                return redirect('register_teacher')
            
            user_teacher = User(username = username , email = email, first_name = f_name, last_name = l_name)
            user_teacher.set_password(password)
            user_teacher.save()
            auth_token = str(uuid.uuid4())
            profile_teacher = Profile.objects.create(user = user_teacher , auth_token = auth_token)
            profile_teacher.save()
            send_mail_after_registration(email , auth_token)
            return redirect('token/')

        except Exception as e:
            print(e)


    return render(request , 'register_teacher.html')


#This LogIn is for Students.
def login_student(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == '':
            messages.success(request, 'Username is required')
            return redirect('login_teacher')
        
        if password == '':
            messages.success(request, 'Password is required')
            return redirect('login_teacher')


        user_student = User.objects.filter(username = username).first()
        if user_student is None:
            messages.success(request, 'User not found.')
            return redirect('login_student')
        
        
        profile_student = Profile.objects.filter(user = user_student ).first()

        if not profile_student.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('login_student')

        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('login_student')
        
        login(request , user)
        return redirect('home')

    return render(request , 'login_student.html')

#This Register is for Students.
def register_student(request):

    if request.method == 'POST':
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l-name')
        username = request.POST.get('username')
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)

        try:
            if User.objects.filter(username = username).first():
                messages.success(request, 'Username is taken.')
                return redirect('register_student')

            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is taken.')
                return redirect('register_teacher')
            
            user_student = User(username = username , email = email, first_name = f_name, last_name = l_name)
            user_student.set_password(password)
            user_student.save()
            auth_token = str(uuid.uuid4())
            profile_student = Profile.objects.create(user = user_student , auth_token = auth_token)
            profile_student.save()
            send_mail_after_registration(email , auth_token)
            return redirect('token/')

        except Exception as e:
            print(e)

    return render(request , 'register_student.html')


def verify(request , auth_token):
    try:
        profile_teacher = Profile.objects.filter(auth_token = auth_token).first()
        

        if profile_teacher:
            if profile_teacher.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('login_teacher')
            profile_teacher.is_verified = True
            profile_teacher.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('login_teacher')

        else:
            return redirect('error/')

    except Exception as e:
        print(e)
        return redirect('teacher_home')

def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi! click the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )


def teacher_question(request):
    if request.method == 'POST':
        form = CreateQuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_home')
    else:
        form = CreateQuestionForm()

    context = { 
        'form' : form
    }
    return render(request, 'teacher_question.html', context)
    

class ConfirmView(View):
    def get (self, request):
        return render(request, 'confirm.html')

class ChooseUserView(View):
    def get(self, request):
        return render(request, 'chooseUser.html')

def error_page(request):
    return  render(request , 'error.html')

@login_required(login_url='/login_teacher')
def teacher_question(request):
        return render(request, 'teacher_question.html')

class FeaturesView(View):
    def get (self, request):
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        return render(request, 'features.html', {'name': f_name}, {'name' : l_name})

class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')

class SuccessView(View):
    def get (self, request):
        return render(request, 'success.html')

def token_send(request):
    return render(request, 'token_send.html')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('chooseUser')

@login_required(login_url='/login_teacher')
def teacher_home(request):
        return render(request, 'teacher_home.html')

def home(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'home.html', context)

def api_question(request, id):
    raw_questions = Question.objects.filter(course = id)[:20]
    questions = []

    for raw_question in raw_questions:
        question = {}
        question['id'] = raw_question.id
        question['question'] = raw_question.question
        question['answer'] = raw_question.answer
        question['marks'] = raw_question.marks
        options = []
        options.append(raw_question.option1)
        options.append(raw_question.option2)
        if raw_question.option3 !='':
            options.append(raw_question.option3)
        if raw_question.option4 !='':
            options.append(raw_question.option4)

        question['options'] = options
        questions.append(question)

    return JsonResponse(questions, safe=False)
@login_required(login_url='/login_student')
def view_score(request):
    user = request.user
    score = ScoreBoard.objects.filter(user=user)
    context = {'score': score}
    return render(request, 'score.html', context)

@login_required(login_url='/login_student')
def take_quiz (request, id):
        context = {'id' : id}
        return render(request, 'quizz.html', context)  

@csrf_exempt
@login_required(login_url='/login_student')
def check_score(request):
    data = json.loads(request.body)
    user = request.user
    course_id = data.get('course_id')
    solutions = json.loads(data.get('data'))
    course = Course.objects.get(id=course_id)
    score = 0
    for solution in solutions:
        question = Question.objects.filter(id = solution.get('question_id')).first()
        if (question.answer) == solution.get('option'):
            score = score + question.marks

    score_board = ScoreBoard(course = course, score = score, user = user)
    score_board.save()
    return JsonResponse({'message' : 'success', 'status':True})


