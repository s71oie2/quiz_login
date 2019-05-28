from django.db import models
from django.urls import reverse
from django.conf import settings
class Board(models.Model):  # 게시판(댓글 기능 없는 공지사항 게시용)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='boards',
                             verbose_name='게시자')
    title = models.CharField('제목', max_length=100)
    content = models.TextField('내용')
    # content = summer_fields.SummernoteTextField('내용', default='')
    date = models.DateTimeField('작성일시', auto_now_add=True)
    hits = models.IntegerField('조회수', default=0)
    # photo = models.ImageField('사진',upload_to='staff/board_img/', null=True, blank=True)  # media 폴더 밑에 staff/board_img/에 저장 (자동 생성)

    def short_content(self):  # 속성으로 존재하는 것처럼 만들기
        if self.content:
            t = self.content[:20] + '...'
        else:
            t = '(내용 없음)'
        return t
    short_content.short_description = '간략 내용'

    def get_absolute_url(self):
        return reverse('staff:board_detail', args=(self.id,))

    def get_newer_board(self):
        newer_board = Board.objects.filter(
            date__gt=self.date
        ).order_by('date').first()
        return newer_board

    def get_older_board(self):
        older_board = Board.objects.filter(
            date__lt=self.date
        ).order_by('-date').first()
        return older_board

    # 조회수
    @property
    def update_counter(self):
        self.hits = self.hits + 1
        self.save()
        return self.hits

    class Meta:
        verbose_name = '게시판'
        verbose_name_plural = '관리자 게시판'
        ordering = ['-date']

class DonationOrg(models.Model):  # 기부단체
    name = models.CharField('기부단체명', max_length=20)
    desc = models.TextField('단체설명')
    photo = models.ImageField('사진',upload_to='staff/donation/')
    url = models.URLField('홈페이지 주소', max_length=250)
    is_donate = models.BooleanField('이달 기부단체', default=False)

    def short_desc(self):
        if self.desc:
            t = self.desc[:20] + '...'
        else:
            t = '(내용 없음)'
        return t
    short_desc.short_description = '간략 단체설명'

    class Meta:
        verbose_name = '기부단체'
        verbose_name_plural = '기부단체'



