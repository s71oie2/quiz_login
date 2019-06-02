from django import forms
from .models import *
from django_summernote.widgets import SummernoteWidget

class BoardForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(BoardForm, self).__init__(*args, **kwargs)

    content = forms.CharField(widget=SummernoteWidget())

    class Meta:
        model = Board
        fields = ['title', 'content']
# 질문 폼
class QForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(QForm, self).__init__(*args, **kwargs)

    question = forms.CharField(widget=SummernoteWidget())

    class Meta:
        model = QnA
        fields = ['title', 'question']

# 답변 폼
class AForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(AForm, self).__init__(*args, **kwargs)

    answer = forms.CharField(widget=SummernoteWidget())

    class Meta:
        model = QnA
        fields = ['answer']

