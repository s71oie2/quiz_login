from django.urls import path
from staff import views

app_name = 'staff'

urlpatterns = [
    path('board/', views.PostLV.as_view(), name='board_list'),
    # path('board/<int:pk>', views.post_detail, name='board_detail'),
    path('board/<int:pk>', views.PostDV.as_view(), name='board_detail'),
    path('board/<int:pk>/edit/', views.post_edit, name='board_edit'),
    path('board/<int:pk>/remove/', views.post_remove, name='board_remove'),
    path('donation/', views.DonationView.as_view(), name='donation'),

]