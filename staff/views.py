from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from staff.models import Board, DonationOrg
from .forms import BoardForm
from django.shortcuts import redirect

class DonationView(TemplateView):
    template_name ='staff/donationOrg.html'


class PostLV(ListView):
    model = Board
    posts = Board.objects.all()
    template_name = "staff/board_list.html"
    context_object_name = 'posts'
    paginate_by = 5


class PostDV(DetailView):
    model = Board
    template_name = "staff/board_detail.html"
    paginate_by = 2
    context_object_name = 'post'


# def post_detail(request, pk):
#     post = get_object_or_404(Board, pk=pk)
#     return render(request, 'staff/board_detail.html',{'post':post})


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

def post_remove(request, pk):
    post = get_object_or_404(Board, pk=pk)
    post.delete()
    return redirect('staff:board_list')

