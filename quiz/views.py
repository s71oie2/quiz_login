from django.shortcuts import render
from django.views.generic import TemplateView
from quiz.models import *
from user.models import Item, HaveItem
from django.shortcuts import redirect
import datetime
# 퀴즈 주제 190709 예림: 숫자 반복적으로 쓰지 않고도 될수있게 수정하기.
def q_sub(request, uk):
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    if len(MyQuiz.objects.filter(user_id=uk, date=today)) <= 10 and len(MyQuiz.objects.filter(user_id=uk, date=today)) > 0:
        quiz_num = MyQuiz.objects.filter(user_id=uk, date=today).last().quiz_id
        quizSubs = QuizSub.objects.get(id=Quiz.objects.get(id=quiz_num).quizSub_id)
        return redirect('quiz:quiz_real', pk=quizSubs.id, uk=uk)
    elif len(MyQuiz.objects.filter(user_id=uk, date=today)) > 10:
        quiz_num = MyQuiz.objects.filter(user_id=uk, date=today).last().quiz_id
        quizSubs = QuizSub.objects.get(id=Quiz.objects.get(id=quiz_num).quizSub_id)
        count = 0
        item = Item.objects.get(id=quizSubs.item_id)
        for i in MyQuiz.objects.filter(user_id=uk, date=today):
            if i.myAnswer == Quiz.objects.get(id=i.quiz_id).answer:
                count += 1
            else:
                continue
        return render(request, 'quiz/quiz_finish.html',
                          {'uk': uk, 'quizSubs': quizSubs.id, 'date': today, 'count': count, 'qnum': 10, 'item': item})
    else:
        quizSubs = QuizSub.objects.all()
        if request.method == "POST" and 'q_sub1' in request.POST:
            quizSubs = QuizSub.objects.get(id=1)
            return redirect('quiz:quiz_real', pk=quizSubs.pk, uk=uk)
        elif request.method == "POST" and 'q_sub2' in request.POST:
            quizSubs = QuizSub.objects.get(id=2)
            return redirect('quiz:quiz_real', pk=quizSubs.pk, uk=uk)
        elif request.method == "POST" and 'q_sub3' in request.POST:
            quizSubs = QuizSub.objects.get(id=3)
            return redirect('quiz:quiz_real', pk=quizSubs.pk, uk=uk)
        elif request.method == "POST" and 'q_sub4' in request.POST:
            quizSubs = QuizSub.objects.get(id=4)
            return redirect('quiz:quiz_real', pk=quizSubs.pk, uk=uk)
        elif request.method == "POST" and 'q_sub5' in request.POST:
            quizSubs = QuizSub.objects.get(id=5)
            return redirect('quiz:quiz_real', pk=quizSubs.pk, uk=uk)
    return render(request, 'quiz/quiz_sub.html', {'quizSubs': quizSubs})


# 문제푸는 화면
def quiz_real(request, pk, uk):
    quizSubs = QuizSub.objects.get(id=pk)
    # 퀴즈 주제에 맞는 문제
    quizs = Quiz.objects.filter(quizSub_id=pk)
    # 문제 맞춘 개수 출력 함수
    today = datetime.datetime.now().strftime('%Y-%m-%d')

    if MyQuiz.objects.filter(user_id=uk, date=today).last().myAnswer == 'N':
        qnum = len(MyQuiz.objects.filter(user_id=uk, date=today))
    else:
        qnum = len(MyQuiz.objects.filter(user_id=uk, date=today))+1
    # 맞춘 문제 개수
    count=0
    # 오늘 회원이 푼 문제
    for myquiz_id in MyQuiz.objects.filter(user_id=uk, date=today):
        # 회원답 정답 비교해서 같으면 +1
        if myquiz_id.myAnswer == Quiz.objects.get(id=myquiz_id.quiz_id).answer:
            count += 1

    # 회원이 처음으로 퀴즈를 풀거나 이전 퀴즈를 풀었다면
    # 마지막 줄에 답이 null이냐 아니냐로 if문 작성 못해서
    # 기본값으로 N을 넣고 이냐 아니냐를 판별
    if not MyQuiz.objects.filter(user_id=uk) or MyQuiz.objects.filter(user_id=uk).last().myAnswer != "N":
        # 랜덤으로 첫번째문제/다음문제 뽑기
        content = quizs.order_by('?').first()
        # 회원문제 테이블에 저장
        user_quiz_id = MyQuiz(myAnswer='N', quiz_id=content.id, user_id=uk)
        user_quiz_id.save()
    else:
        content = Quiz.objects.get(id=MyQuiz.objects.filter(user_id=uk).last().quiz_id)
    # 문제의 답
    # answer = content.answer
    answer = Quiz.objects.get(id=MyQuiz.objects.filter(user_id=uk).last().quiz_id).answer
    # 되돌아올때 퀴즈 주제 pk 전달위해서 있음
    print("문제: ", content.content)

    # O 버튼 눌렀을 때
    if request.method == "POST" and 'O' in request.POST:
        print("O버튼누름", answer, type(answer))
        user_answer = MyQuiz.objects.filter(user_id=uk).last()
        print(user_answer)
        user_answer.myAnswer='O'
        user_answer.save()
        user_answer = MyQuiz.objects.filter(user_id=uk).last().myAnswer
        if answer == user_answer:
            # 정답일 때
            print('정답입니다.')
            return render(request, 'quiz/right.html', {'quizSubs': quizSubs, 'count': count+1, 'qnum':qnum})
        # 틀렸을 때
        else:
            print('틀렸습니다.')
            return render(request, 'quiz/wrong.html', {'quizSubs': quizSubs, 'count': count, 'qnum':qnum})
            # 오늘 풀 수 있는 문제 개수 및 다 풀었을 때

    # X 버튼 눌렀을 때
    elif request.method == "POST" and 'X' in request.POST:
        print("X버튼누름", answer, type(answer))
        user_answer = MyQuiz.objects.filter(user_id=uk).last()
        print(user_answer)
        user_answer.myAnswer="X"
        user_answer.save()

    # 정답 비교
        user_answer = MyQuiz.objects.filter(user_id=uk).last().myAnswer
        if answer == user_answer:
        # 정답일 때
            print('정답입니다.')
            return render(request, 'quiz/right.html', {'quizSubs': quizSubs, 'count': count+1, 'qnum':qnum})
        # 틀렸을 때
        else:
            print('틀렸습니다.')
            return render(request, 'quiz/wrong.html', {'quizSubs': quizSubs, 'count': count, 'qnum':qnum})
        # return redirect('quiz:quiz_real', {'answer': answer})
    if request.method == "POST" and 'next' in request.POST:
        print("다음버튼 누름")
        if MyQuiz.objects.filter(user_id=uk, date=today).count() > 10:
            date = MyQuiz.objects.filter(user_id=uk).last().date
            print("오늘 문제를 모두 풀었습니다.")
            item = Item.objects.get(id=quizSubs.item_id)
            try:
                user_item = HaveItem.objects.get(user_id=uk, item_id=quizSubs.item_id)
                user_item.item_count += count
                user_item.save()
            except HaveItem.DoesNotExist:
                user_item = HaveItem.objects.create(item_count=count, item_id=quizSubs.item_id, user_id=uk)
                user_item.save()
            return render(request, 'quiz/quiz_finish.html',
                          {'uk': uk, 'quizSubs': quizSubs, 'date': date, 'count': count, 'qnum': qnum, 'item': item})
        else:
            pass
    return render(request, 'quiz/quiz_real.html', {'quizs': content, 'quizSubs': quizSubs, 'count': count, 'qnum':qnum})

def quizinfo(request):
    i=1 # 도구 id
    quizinfos=[] # a 담을 리스트
    while i <= QuizSub.objects.all().count():
        a = []  # 주제-도구
        quizSub = QuizSub.objects.get(id=i)
        item = Item.objects.get(id=quizSub.item_id)
        a.append(quizSub)
        a.append(item)
        quizinfos.append(a)
        i = i + 1
    return render(request, 'quiz/quizinfo.html', {'quizinfos':quizinfos})