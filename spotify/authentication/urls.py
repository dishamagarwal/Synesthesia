from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.login, name="login"),
    path("home", views.home, name="home"),
    path("playlist", views.getPlaylist, name='getPlaylist'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)