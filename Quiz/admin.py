from django.contrib import admin
#from .models import*
from . import models


@admin.register(models.Course)

class CourseAdmin(admin.ModelAdmin):
  list_display = ['course_name',]

@admin.register(models.Question)

class QuestionAdmin(admin.ModelAdmin):
  list_display = ['question','course', 'date_updated',]

@admin.register(models.ScoreBoard)

class ScoreBoardAdmin(admin.ModelAdmin):
  list_display = ['course', 'Date_Answered', 'user', 'score',]
