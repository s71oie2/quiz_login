from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from mysite.views import HomeView

urlpatterns = [
  path('admin/', admin.site.urls),
  path('', HomeView.as_view(), name='home'),
  path('user/', include('user.urls'), name='user'),
  path('plant/', include('plant.urls'), name='plant'),
  path('quiz/', include('quiz.urls'), name='quiz'),
  path('staff/', include('staff.urls'), name='staff'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
