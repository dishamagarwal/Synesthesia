#!/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from spotipy.oauth2 import SpotifyOAuth
from django.http import JsonResponse
import spotipy
import json

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

def getPlaylist(request):
    print('Request body:', request.body)  # Print the request body for debugging
    try:
        data = json.loads(request.body)
        sliders = data.get('sliders', {})
        print('Slider values:', sliders)
        # Your code to process the data
        return JsonResponse({'message': 'got data!'})
    except json.JSONDecodeError as e:
        print('Error decoding JSON:', str(e))  # Print JSON decode error for debugging
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)