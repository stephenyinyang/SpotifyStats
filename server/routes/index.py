from server import app
from flask import render_template
from flask import request

from flask import Flask, redirect, url_for
import startup
from startup import *
# imports matplotlib package and pyplot module for plotting
#import matplotlib.pyplot as plt

# imports json package for loading file
import json

# installs/imports spotipy package to enable features from the Spotify Web API
import sys
import spotipy
import spotipy.util as util
import os

# current environment variables
#print(os.environ)

# authorizes the user to access information from Spotify Web API
from spotipy.oauth2 import SpotifyOAuth

#token = util.prompt_for_user_token('1279336990')

scope = "streaming user-library-read user-read-playback-state  user-top-read"


# os.environ["SPOTIPY_CLIENT_ID"] = "07babcfeaea747f0967bb1d5145fc21f"
# os.environ["SPOTIPY_CLIENT_SECRET"] = "45e1dbda55da450b808e50aaf728365b"
# os.environ["SPOTIPY_REDIRECT_URI"] = "https://spotify-stats.mybluemix.net/"

# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# results = sp.current_user_saved_tracks()
# yeet = results['items'][0]['artists'][0]['name']
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])

#sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
#print(sp.devices())

# token = util.prompt_for_user_token(scope)
# sp = spotipy.Spotify(auth=token)

#print(request.url)
# code = SpotifyOAuth.parse_response_code(request.url)
# token_info = SpotifyOAuth.get_access_token(code)
# token = token_info['access_token']

# if token:
#     sp = spotipy.Spotify(auth=token)
#     #print(sp.devices())
#     #sp.add_to_queue('4NmVYKJ1IcyODKZBTD0xJ2', '6921e1bc3f5f1ec26998b5ed8a04a864800e703a')
#     me = sp.me()
#     #print(me)
#     #topArtists = sp.current_user_top_artists(limit=50, time_range='medium_term')
#     print(json.dumps(me, sort_keys=True, indent=4))
#     results = sp.current_user_top_tracks(limit=10, time_range='short_term')
#     #print(results['items'])
#     count = 1
#     #print(json.dumps(results['items'][0], sort_keys=True, indent=4))
#     favsong = results['items'][1]['name']
#     for item in results['items']:
#         print(str(count) + ") " + item['name'])
#         count += 1
#         #track = item['track']
#         #print(track['id'])
#         #print(track['name'] + ' - ' + track['artists'][0]['name'])
# else:
#     print("Can't get token for", os.environ['SPOTIPY_CLIENT_ID'])
from flask import session

# @app.before_request
# def before_request_func():
#     return redirect('/')

app.secret_key =  os.urandom(24)

@app.route('/')
def hello_world():
    if (session): 
        session['tok'] = startup.refreshToken(session['ref'])[0]
        print('yaay')
        return redirect('/dashboard')  
    print('hello')
    response = startup.getUser()
    return redirect(response)


@app.route('/callback/')
def callback():
    tokenArray = startup.getUserToken(request.args['code'])
    session['tok'] = tokenArray[0]
    session['ref'] = tokenArray[4]
    print(session['tok'])
    print(session['ref'])
    print('yeet')
    return redirect("/dashboard")

@app.route('/dashboard')
def dashboard():
    #startup.getUserToken(code)
    if (session): 
        session['tok'] = startup.refreshToken(session['ref'])[0]
        sp = spotipy.Spotify(auth=session['tok'])
        print(json.dumps(sp.current_user_top_tracks(limit=10, time_range='short_term')['items'][0]))
        return render_template('index.html', data=sp.current_user_top_tracks(limit=10, time_range='short_term')['items'])
    else:
        return redirect('/') 
    

@app.route('/logout')
def logout():
    startup.clearTokenData()
    return redirect("/")

@app.errorhandler(404)
@app.route("/error404")
def page_not_found(error):
    return app.send_static_file('404.html')

@app.errorhandler(500)
@app.route("/error500")
def requests_error(error):
    return app.send_static_file('500.html')
