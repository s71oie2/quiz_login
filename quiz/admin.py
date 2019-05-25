from django.contrib import admin
from .models import QuizSub, Quiz, MyQuiz

@admin.register(QuizSub)
class QuizSubAdmin(admin.ModelAdmin):
    list_display =['id', 'name',
                   ]
    list_display_links = ['id', 'name', ]
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'quizSub', 'short_content', 'answer',
                    ]
    list_display_links = ['id', 'quizSub', 'short_content', ]
@admin.register(MyQuiz)
class MyQuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'quiz', 'date', 'myAnswer',
                    ]
    list_display_links = ['id', 'user', 'quiz', ]