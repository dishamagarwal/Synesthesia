from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.login, name="login"),
    path("home", views.home, name="home"),
    path("playlist", views.getPlaylist, name='getPlaylist'),
    path('generate_abstract_image', views.generateAbstractImage, name='generateAbstractImage'),
    path('playlist_page', views.playlist_page, name='playlist_page'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)