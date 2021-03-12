from django.contrib import admin
from django.urls import path
from core import views as core_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',core_views.index),
    path('api',core_views.AgoraAPI.as_view()),
    path('api/',core_views.AgoraAPI.as_view()), # to handle append backslash runtime error. 
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)