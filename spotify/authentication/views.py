#!/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11

from django.shortcuts import render, redirect
from django.http import HttpResponse
import spotipy
from django.urls import reverse
from spotipy.oauth2 import SpotifyOAuth
# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the auth index.")

def login(request):
    scope = "user-library-read playlist-modify-private"
    redirect_uri = "http://127.0.0.1:8080/home"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, redirect_uri=redirect_uri))
    results = sp.current_user_saved_tracks()
    print("Successully logged in")
    return redirect(reverse('home'))

def home(request):
    return render(request, 'index.html')