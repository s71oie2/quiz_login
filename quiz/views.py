from django.shortcuts import render
from django.views.generic import TemplateView
from quiz.models import *
from django.shortcuts import redirect

class QuizView(TemplateView):
    template_name ='quiz/quiz.html'

def q_sub(request):
    quizSubs = QuizSub.objects.all()
    if request.method == "POST" and 'q_sub1' in request.POST:
        quizSubs = QuizSub.objects.get(id=1)
        return redirect('quiz:quiz_real', pk=quizSubs.pk)
    elif request.method == "POST" and 'q_sub2' in request.POST:
        quizSubs = QuizSub.objects.get(id=2)
        return redirect('quiz:quiz_real', pk=quizSubs.pk)
    return render(request, 'quiz/quiz_sub.html', {'quizSubs': quizSubs})


# answer = quizs[:2]
#         if request.method == "POST" and 'O' in request.POST:
#             user_answer = MyQuiz.objects.update(quiz=quizs, myAnswer='O')
#             if answer == user_answer.myAnswer:
#                 print("정답입니다.")
#             else:
#                 print("틀렸습니다.")

def quiz_real(request, pk):
    # 퀴즈 주제에 맞는 문제
    quizs = Quiz.objects.filter(quizSub_id=pk)
    # 랜덤으로 첫번째문제(한문제) 뽑기
    content = quizs.order_by('?').first()
    # 문제의 답
    answer = str(content.answer)
    O = "O"
    X = "X"
    # 되돌아올때 퀴즈 주제 pk 전달위해서 있음
    quizSubs = QuizSub.objects.get(id=pk)
    # O 버튼 눌렀을 때
    if request.method == "POST" and "O" in request.POST:
        if answer == O:
        # 정답일 때
            print('정답입니다.')
            return render(request, 'quiz/right.html', {'quizSubs': quizSubs})
        # 틀렸을 때
        elif answer == X:
            print('틀렸습니다.')
            return render(request, 'quiz/wrong.html', {'quizSubs': quizSubs})

    if request.method == "POST" and "X" in request.POST:
        if answer == O:
            print('틀렸습니다.')
            return render(request, 'quiz/wrong.html', {'quizSubs': quizSubs})
        elif answer == X:
            print('정답입니다.')
            return render(request, 'quiz/right.html', {'quizSubs': quizSubs})
        # return redirect('quiz:quiz_real', {'answer': answer})
    return render(request, 'quiz/quiz_real.html', {'quizs':content, 'answer':answer})

class Right(TemplateView):
    template_name ='quiz/right.html'

class Wrong(TemplateView):
    template_name = 'quiz/wrong.html'
