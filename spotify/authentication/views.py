from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from spotipy.oauth2 import SpotifyOAuth
from django.http import JsonResponse
import spotipy, json, requests

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

def generatePlaylistName():
    response = requests.get("https://random-word-api.herokuapp.com/word?number=2")
    words = []
    if response.status_code == 200:
        words = response.json()
    else: 
        words = ["Cool", "Tunes"]
    playlist_name = f"{words[0].capitalize()} {words[1].capitalize()}"
    print(f"Generated playlist name: {playlist_name}")
    return playlist_name

def getPlaylist(request):
    base_url = "https://api.spotify.com/v1/recommendations"
    try:
        access_token = request.session.get('spotify_token')
        sliders = json.loads(request.body).get('sliders', {})

        recommendations = sp.recommendations(
            seed_genres = sp.recommendation_genre_seeds()['genres'][:5], # send the actual genres you want
            limit = 13,
            target_valence = sliders['melancholic'],  # mapping melancholic to valence
            target_danceability = sliders['electronic'],  # mapping electronic to danceability
            target_energy = sliders['energy']
        )
        tracks = []
        for track in recommendations["tracks"]:
            track_info = {
                "name": track["name"],
                "artists": [artist["name"] for artist in track["artists"]],
                "album": track["album"]["name"],
                # "preview_url": track["preview_url"]
            }
            tracks.append(track_info)

        # Generate a unique and cool name for the playlist (e.g., "My Awesome Playlist")
        playlist_name = generatePlaylistName()
        # # Create a new playlist for the user
        # user_id = sp.me()['id']  # Get the user's Spotify ID
        # playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
        # # Extract the playlist ID from the response
        # playlist_id = playlist['id']
        # # Get the track URIs from the recommendations
        # track_uris = [track['uri'] for track in recommendations['tracks']]
        # # Add tracks to the created playlist
        # sp.playlist_add_items(playlist_id=playlist_id, items=track_uris)
        print(f"Playlist '{playlist_name}' created and tracks added successfully!")
        
        return JsonResponse({'message': 'got data!'})
    except json.JSONDecodeError as e:
        print('Error decoding JSON:', str(e))  # Print JSON decode error for debugging
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)