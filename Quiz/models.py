from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    course_name = models.CharField(max_length=50)

    def __str__(self):
        return self.course_name
        
class Updated(models.Model):
    date_updated = models.DateTimeField(verbose_name=("Last Update"), auto_now=True)
    class Meta:
        abstract = True,

class Question(Updated):

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    answer = models.IntegerField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200, blank=True)
    option4 = models.CharField(max_length=200, blank=True)
    #date_created = models.DateTimeField(auto_now_add=True, verbose_name=("Date Created")) 

    marks = models.IntegerField(default=1)
    
    def __str__(self):
        return self.question

class ScoreBoard(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    Date_Answered = models.DateTimeField(auto_now_add=True)
    

    

