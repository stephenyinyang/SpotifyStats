import os
from flask import Flask, abort, session, request, redirect
from flask.json import jsonify

app = Flask(__name__, template_folder="../public", static_folder="../public", static_url_path='')

from server.routes import *
from server.services import *

initServices(app)
os.environ["SPOTIPY_CLIENT_ID"] = "07babcfeaea747f0967bb1d5145fc21f"
os.environ["SPOTIPY_CLIENT_SECRET"] = "45e1dbda55da450b808e50aaf728365b"
os.environ["SPOTIPY_REDIRECT_URI"] = "https://spotify-stats.mybluemix.net/"

if 'FLASK_LIVE_RELOAD' in os.environ and os.environ['FLASK_LIVE_RELOAD'] == 'true':
	import livereload
	app.debug = True
	server = livereload.Server(app.wsgi_app)
	server.serve(port=os.environ['port'], host=os.environ['host'])
