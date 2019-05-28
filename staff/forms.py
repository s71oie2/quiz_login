from django import forms
from .models import Board
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
class BoardForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(BoardForm, self).__init__(*args, **kwargs)

    content = forms.CharField(widget=SummernoteWidget())
    class Meta:
        model = Board
        fields = ['id', 'user', 'title', 'content']

