from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

class Course(models.Model):
    course_name = models.CharField(max_length=50)

    def __str__(self):
        return self.course_name

class Question(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.TextField(max_length=200)
    answer = models.IntegerField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200, blank=True)
    option4 = models.CharField(max_length=200, blank=True)
    marks = models.IntegerField(default=10)
    
    def __str__(self):
        return self.question
     

class ScoreBoard(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    Date_Answered = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    dated_created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.user.username

    

