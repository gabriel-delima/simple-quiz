from django.contrib import admin
from quiz.base.models import Question, User, Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "enunciado", "disponivel")

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "create_time")

@admin.register(Answer)
class UserAdmin(admin.ModelAdmin):
    list_display = ("answered_time", "user", "question", "points")