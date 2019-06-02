from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from staff.models import *
from .forms import *
from django.shortcuts import redirect
from django.utils import timezone
# 기부단체
class DonationView(TemplateView):
    template_name ='staff/donationOrg.html'

# 공지사항 목록
class PostLV(ListView):
    model = Board
    template_name = "staff/board_list.html"
    context_object_name = 'posts'
    paginate_by = 5
    posts = Board.objects.all()

    # 카테고리 목록 추가
    def get_context_data(self, **kwargs):
        context = super(PostLV, self).get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
        return context



# 공지사항 상세
class PostDV(DetailView):
    model = Board
    template_name = "staff/board_detail.html"
    paginate_by = 2
    context_object_name = 'post'


# def post_detail(request, pk):
#     post = get_object_or_404(Board, pk=pk)
#     return render(request, 'staff/board_detail.html',{'post':post})

# 공지사항 수정
def post_edit(request, pk):
    post = get_object_or_404(Board, pk=pk)
    if request.method == "POST":
        form = BoardForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('staff:board_detail', pk=post.pk)
    else:
        form = BoardForm(instance=post)
    return render(request, 'staff/board_edit.html', {'form':form})

# 공지사항 삭제
def post_remove(request, pk):
    post = get_object_or_404(Board, pk=pk)
    post.delete()
    return redirect('staff:board_list')

# 카테고리 필터링
def post_filter(request, pk):
    posts = Board.objects.filter(category_id=pk)
    categories = Category.objects.all()
    return render(request, 'staff/board_list.html', {'posts': posts, 'categories':categories})

# QnA 두번째 게시판
def qnaView(request):
    qnas = QnA.objects.all()
    return render(request, 'staff/QnA.html', {'qnas': qnas})

# QnA 삭제
def qna_remove(request, pk):
    qna = get_object_or_404(QnA, pk=pk)
    qna.delete()
    return redirect('staff:qna')

# 질문 수정
def q_edit(request, pk):
    qna = get_object_or_404(QnA, pk=pk)
    if request.method == "POST":
        form = QForm(request.POST, instance=qna)
        if form.is_valid():
            qna = form.save(commit=False)
            qna.user = request.user
            qna.save()
            return redirect('staff:qna')
    else:
        form = QForm(instance=qna)
    return render(request, 'staff/QnA.html', {'qform':form})

# 답변 수정
def a_edit(request, pk):
    qna = get_object_or_404(QnA, pk=pk)
    if request.method == "POST":
        form = AForm(request.POST, instance=qna)
        if form.is_valid():
            qna = form.save(commit=False)
            qna.user = request.user
            qna.save()
            return redirect('staff:qna')
    else:
        form = AForm(instance=qna)
    return render(request, 'staff/QnA.html', {'aform':form})

# 질문쓰기
def q_new(request):
    if request.method == "POST":
        form = QForm(request.POST)
        if form.is_valid():
            qna = form.save(commit=False)
            qna.user = request.user
            qna.date = timezone.now()
            qna.save()
            return redirect('staff:qna')
    else:
        form = QForm()
    return render(request, 'staff/QnA.html', {'qform': form})