from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name',]
    list_display_links = ['id', 'name', ]
    search_fields = ['name']
    ordering = ['name']

@admin.register(Board)
class BoardAdmin(SummernoteModelAdmin):
    list_display = ['id', 'user', 'title', ]
    list_display_links = ['id', 'user', 'title', ]
    list_filter = ['category']

@admin.register(QnA)
class QnAAdmin(SummernoteModelAdmin):
    list_display = ['id', 'user', 'title', ]
    list_display_links = ['id', 'user', 'title', ]

@admin.register(DonationOrg)
class DonationOrgAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'short_desc', 'url', ]
    list_display_links = ['id', 'name', 'short_desc', ]