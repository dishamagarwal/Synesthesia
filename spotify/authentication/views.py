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
    global sp
    scope = "user-library-read playlist-modify-private"
    redirect_uri = "http://127.0.0.1:8080/home"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, redirect_uri=redirect_uri))
    results = sp.current_user_saved_tracks()
    print("Successully logged in", sp)
    return redirect(reverse('home'))

def home(request):
    return render(request, 'index.html')

def getPlaylist(request):
    print('request', request)
    base_url = "https://api.spotify.com/v1/recommendations"
    try:
        access_token = request.session.get('spotify_token')
        data = json.loads(request.body)
        sliders = data.get('sliders', {})
        # print('Slider values:', sliders)
        # sp = spotipy.Spotify(auth=access_token)
        # response = temp.recommendations()
        # print(response)
        # return JsonResponse(response)
        recommendations = sp.recommendations(seed_genres=['pop'], limit=1)
        for i in recommendations["tracks"][0]["artists"]:
            print(i["name"])
        return JsonResponse({'message': 'got data!'})
    except json.JSONDecodeError as e:
        print('Error decoding JSON:', str(e))  # Print JSON decode error for debugging
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)