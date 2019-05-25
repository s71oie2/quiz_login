from django.contrib import admin
from .models import Board, DonationOrg

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'short_content', ]
    list_display_links = ['id', 'user', 'title', 'short_content', ]
    
@admin.register(DonationOrg)
class DonationOrgAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'short_desc', 'url', ]
    list_display_links = ['id', 'name', 'short_desc', ]