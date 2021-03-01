from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import JsonResponse
from .models import*
import json


def login_attempt(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email).first()
        if not user:
            message = {'error' : 'user does not exists'}
            context = message
            return render(request, 'auth/login.html', context)
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            message = {'error' : 'Incorrect Email or Password'}
            context = message
            return render(request, 'auth/login.html', context)
    return render(request, 'auth/login.html')

def register_attempt(request):
    if request.method == 'POST':
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(email = email).first()

        if user:
            message = {'error' : 'user already exists'}
            context = message
            return render(request, 'auth/register.html', context)

        user = User(first_name = f_name, last_name = l_name, email = email, username=email)
        user.set_password(password)
        user.save()
    
    return render(request, 'confirm.html')

def confirm(request):
    return render(request, 'confirm.html')

def features(request):
    return render(request, 'features.html')

def about(request):
    return render(request, 'about.html')

def logout_attempt(request):
    logout(request)
    return redirect('login')

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
@login_required(login_url='/login')
def view_score(request):
    user = request.user
    score = ScoreBoard.objects.filter(user=user)
    context = {'score': score}
    return render(request, 'score.html', context)
@login_required(login_url='/login')
def take_quiz(request, id):
    context = {'id' : id}
    return render(request, 'quizz.html', context)  

@csrf_exempt
@login_required(login_url='/login')
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

