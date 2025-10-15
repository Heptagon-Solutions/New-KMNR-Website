import requests
import base64
import json
import os
from flask import Blueprint, request, jsonify, session
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

spotify_bp = Blueprint('spotify', __name__)

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE = "https://api.spotify.com/v1"

@spotify_bp.route('/spotify/auth', methods=['GET'])
def spotify_auth():
    # Start with basic scopes that should work
    scope = "playlist-modify-public playlist-modify-private"
    auth_url = f"{SPOTIFY_AUTH_URL}?response_type=code&client_id={SPOTIFY_CLIENT_ID}&scope={scope}&redirect_uri={SPOTIFY_REDIRECT_URI}"
    return jsonify({"auth_url": auth_url})

@spotify_bp.route('/spotify/callback', methods=['POST'])
def spotify_callback():
    code = request.json.get('code')
    if not code:
        return jsonify({"error": "No authorization code provided"}), 400
    
    auth_header = base64.b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()).decode()
    
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI
    }
    
    response = requests.post(SPOTIFY_TOKEN_URL, headers=headers, data=data)
    
    if response.status_code == 200:
        token_data = response.json()
        session['spotify_access_token'] = token_data['access_token']
        session['spotify_refresh_token'] = token_data.get('refresh_token')
        session['spotify_expires_at'] = datetime.now() + timedelta(seconds=token_data['expires_in'])
        return jsonify({"success": True, "access_token": token_data['access_token']})
    else:
        return jsonify({"error": "Failed to get access token"}), 400

@spotify_bp.route('/spotify/search', methods=['GET'])
def search_spotify():
    query = request.args.get('q')
    search_type = request.args.get('type', 'track')
    limit = request.args.get('limit', 20)
    
    if not query:
        return jsonify({"error": "Query parameter required"}), 400
    
    access_token = session.get('spotify_access_token')
    if not access_token:
        return jsonify({"error": "Not authenticated with Spotify"}), 401
    
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "q": query,
        "type": search_type,
        "limit": limit
    }
    
    response = requests.get(f"{SPOTIFY_API_BASE}/search", headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return jsonify({"error": "Spotify API request failed"}), response.status_code

@spotify_bp.route('/spotify/user', methods=['GET'])
def get_user_profile():
    access_token = session.get('spotify_access_token')
    if not access_token:
        return jsonify({"error": "Not authenticated with Spotify"}), 401
    
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{SPOTIFY_API_BASE}/me", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return jsonify({"error": "Failed to get user profile"}), response.status_code

@spotify_bp.route('/spotify/playlists', methods=['POST'])
def create_playlist():
    access_token = session.get('spotify_access_token')
    if not access_token:
        return jsonify({"error": "Not authenticated with Spotify"}), 401
    
    user_response = requests.get(f"{SPOTIFY_API_BASE}/me", 
                                headers={"Authorization": f"Bearer {access_token}"})
    
    if user_response.status_code != 200:
        return jsonify({"error": "Failed to get user info"}), 400
    
    user_id = user_response.json()['id']
    
    playlist_data = request.json
    name = playlist_data.get('name', 'KMNR Playlist')
    description = playlist_data.get('description', 'Created from KMNR website')
    public = playlist_data.get('public', True)
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "name": name,
        "description": description,
        "public": public
    }
    
    response = requests.post(f"{SPOTIFY_API_BASE}/users/{user_id}/playlists", 
                           headers=headers, json=data)
    
    if response.status_code == 201:
        return response.json()
    else:
        return jsonify({"error": "Failed to create playlist"}), response.status_code

@spotify_bp.route('/spotify/playlists/<playlist_id>/tracks', methods=['POST'])
def add_tracks_to_playlist(playlist_id):
    access_token = session.get('spotify_access_token')
    if not access_token:
        return jsonify({"error": "Not authenticated with Spotify"}), 401
    
    track_uris = request.json.get('uris', [])
    if not track_uris:
        return jsonify({"error": "No track URIs provided"}), 400
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    data = {"uris": track_uris}
    
    response = requests.post(f"{SPOTIFY_API_BASE}/playlists/{playlist_id}/tracks", 
                           headers=headers, json=data)
    
    if response.status_code == 201:
        return response.json()
    else:
        return jsonify({"error": "Failed to add tracks to playlist"}), response.status_code

@spotify_bp.route('/spotify/status', methods=['GET'])
def spotify_status():
    access_token = session.get('spotify_access_token')
    return jsonify({"authenticated": bool(access_token)})

@spotify_bp.route('/spotify/debug', methods=['GET'])
def spotify_debug():
    return jsonify({
        "client_id": SPOTIFY_CLIENT_ID,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "current_scopes": "playlist-modify-public playlist-modify-private",
        "session_keys": list(session.keys()),
        "has_access_token": bool(session.get('spotify_access_token'))
    })