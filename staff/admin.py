from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin  # 추가---------------
from .models import Board, DonationOrg

@admin.register(Board)
class BoardAdmin(SummernoteModelAdmin):  # 수정---------------------------------
    list_display = ['id', 'user', 'title', ]
    list_display_links = ['id', 'user', 'title', ]
    
@admin.register(DonationOrg)
class DonationOrgAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'short_desc', 'url', ]
    list_display_links = ['id', 'name', 'short_desc', ]