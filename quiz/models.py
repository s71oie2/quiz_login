from django.db import models
from django.conf import settings


class QuizSub(models.Model):
    name = models.CharField('퀴즈주제', max_length=10)
    photo = models.ImageField('사진',upload_to='quiz/quizSub_img/', null=True)
    def __str__(self):
        return self.name
    
    class Meta: 
        verbose_name = '퀴즈주제'
        verbose_name_plural = '퀴즈주제'
    
    
class Quiz(models.Model):
    quizSub = models.ForeignKey(QuizSub,  # QuizSub 외래키
                                on_delete=models.CASCADE,
                                related_name='quizSubs',
                                verbose_name='퀴즈주제')
    content = models.TextField('퀴즈내용')
    answer = models.CharField('답', max_length=1)  # 각 문제의 정답
    
    def __str__(self):
        return self.content
    
    def short_content(self):
        if self.content:
            t = self.content[:20] + '...'
        else:
            t = '(내용 없음)'
        return t
    short_content.short_description = '간략 퀴즈내용'
    class Meta:
        verbose_name = '퀴즈'
        verbose_name_plural = '퀴즈'
    
class MyQuiz(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  # 유저 외래키
                             on_delete=models.CASCADE,
                             related_name='myQuizs',
                             verbose_name='회원')
    quiz = models.ForeignKey(Quiz,  # 퀴즈 외래키
                             on_delete=models.CASCADE,
                             related_name='quizs',
                             verbose_name='퀴즈')  # 퀴즈번호
                            
    date = models.DateField('퀴즈 푼 날짜', auto_now_add=True)  # 객체가 처음 생성되었을 때 현재 날짜를 자동 생성. update처럼 저장될 때마다 자동 설정은 auto_now
    myAnswer = models.CharField('회원 답', max_length=1)  # 회원이 선택한 답

    class Meta:
        verbose_name = '회원퀴즈'
        verbose_name_plural = '회원퀴즈'

