from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from spotipy.oauth2 import SpotifyOAuth
from django.http import JsonResponse
import spotipy, json, requests
from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFilter
import io, random, colorsys

def index(request):
    return HttpResponse("Hello, world. You're at the auth index.")

def login(request):
    global sp
    scope = "user-library-read playlist-modify-private"
    redirect_uri = "http://127.0.0.1:8080/home"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, redirect_uri=redirect_uri))
    # results = sp.current_user_saved_tracks()
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
    return playlist_name

def getPlaylist(request):
    base_url = "https://api.spotify.com/v1/recommendations"
    try:
        access_token = request.session.get('spotify_token')
        sliders = json.loads(request.body).get('sliders', {})
        # print("sliders", sliders)

        recommendations = sp.recommendations(
            seed_genres = sp.recommendation_genre_seeds()['genres'][:5], # ToDO: filter genres based on color
            limit = 13,
            target_acousticness = sliders.get("neutral", 0.5),  # mapping neutral to acousticness
            target_danceability = sliders.get("darkness", 0.5),  # mapping darkness to danceability
            max_duration_ms = 300000,
            target_energy = sliders.get("darkness", 0.5),  # mapping darkness to energy
            # target_instrumentalness = sliders.get("", 0.5),  # mapping melancholic to instrumentalness
            target_liveness = sliders.get("saturation", 0.5),  # mapping saturation to liveness
            target_loudness = sliders.get("contrast", 0.5),  # mapping contrast to loudness
            # target_popularity = sliders.get("", 0.5),  # calculte popularity based on hex
            target_speechiness = sliders.get("texture", 0.5),  # mapping texture to speechiness
            target_tempo = sliders.get("saturation", 0.5),  # mapping saturation to tempo
            target_valence = sliders.get("darkness", 0.5)  # mapping darkness to valence
        )
        tracks = []
        for track in recommendations["tracks"]:
            track_info = {
                "name": track["name"],
                "artists": [artist["name"] for artist in track["artists"]],
                # "album": track["album"]["name"],
                # "preview_url": track["preview_url"]
            }
            tracks.append(track_info)
        print(tracks)
        return JsonResponse({'tracks': tracks})
    except json.JSONDecodeError as e:
        print('Error decoding JSON:', str(e))  # Print JSON decode error for debugging
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    
def savePlaylistToSpotify(request, recommendations):
    playlist_name = generatePlaylistName()
    user_id = sp.me()['id'] 
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
    playlist_id = playlist['id']
    track_uris = [track['uri'] for track in recommendations['tracks']]
    sp.playlist_add_items(playlist_id=playlist_id, items=track_uris)
    print(f"Playlist '{playlist_name}' created and tracks added successfully!")

def hsl_to_rgb(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h/360.0, l/100.0, s/100.0)
    return int(r*255), int(g*255), int(b*255)

def generateAbstractImage(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            h = float(data['h'])
            s = float(data['s'])
            l = float(data['l'])
        except (ValueError, KeyError) as e:
            return JsonResponse({'error': 'Invalid HSL values'}, status=400)
        
        rgb_color = hsl_to_rgb(h, s, l)
        
        # Create an image with the specified color
        image_size = (500, 500)  # Size of the image
        image = Image.new("RGB", image_size, rgb_color)
        draw = ImageDraw.Draw(image)
        
        # Generate abstract pattern
        for _ in range(10):  # Number of circles
            circle_size = (150, 150)  # Size of each circle
            upper_left = (
                random.randint(0, image_size[0] - circle_size[0]),
                random.randint(0, image_size[1] - circle_size[1]),
            )
            lower_right = (
                upper_left[0] + circle_size[0],
                upper_left[1] + circle_size[1],
            )
            circle_color = tuple([random.randint(0, 255) for _ in range(3)])
            draw.ellipse([upper_left, lower_right], fill=circle_color)
        
        # Apply blur to create a similar effect
        image = image.filter(ImageFilter.GaussianBlur(radius=20))
        
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        return HttpResponse(buffer, content_type='image/png')

    return JsonResponse({'error': 'Invalid request method'}, status=400)