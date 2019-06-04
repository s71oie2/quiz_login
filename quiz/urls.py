from django.urls import path
from quiz import views

app_name = 'quiz'

urlpatterns = [
    path('', views.QuizView.as_view(), name='index'),
    path('quiz_subs/', views.q_sub, name='quizSubs'),
    path('quiz_real/<int:pk>/', views.quiz_real, name='quiz_real'),
    path('right/', views.Right.as_view(), name='right'),
    path('wrong/', views.Wrong.as_view(), name='wrong'),
]
