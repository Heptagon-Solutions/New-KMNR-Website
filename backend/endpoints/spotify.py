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

def make_spotify_request(endpoint, method='GET', params=None, data=None):
    """Helper function to make authenticated Spotify API requests with enhanced error handling"""
    access_token = session.get('spotify_access_token')
    if not access_token:
        return jsonify({
            "error": "Authentication required",
            "message": "Not authenticated with Spotify. Please log in first.",
            "code": "SPOTIFY_AUTH_REQUIRED"
        }), 401
    
    headers = {"Authorization": f"Bearer {access_token}"}
    if data:
        headers["Content-Type"] = "application/json"
    
    url = f"{SPOTIFY_API_BASE}/{endpoint}"
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, params=params, timeout=10)
        elif method == 'POST':
            response = requests.post(url, headers=headers, params=params, json=data, timeout=10)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, params=params, json=data, timeout=10)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, params=params, json=data, timeout=10)
        else:
            return jsonify({
                "error": "Unsupported HTTP method",
                "message": f"Method {method} is not supported",
                "code": "INVALID_HTTP_METHOD"
            }), 400
        
        # Success cases
        if response.status_code in [200, 201, 204]:
            try:
                return response.json() if response.content else {"success": True}
            except ValueError:
                return {"success": True}
        
        # Handle specific Spotify API errors
        try:
            error_data = response.json() if response.content else {}
        except ValueError:
            error_data = {"message": response.text or "Unknown error"}
        
        # Map common Spotify API errors to user-friendly messages
        error_messages = {
            400: "Bad request - invalid parameters",
            401: "Unauthorized - token may be expired or invalid",
            403: "Forbidden - insufficient permissions or rate limited",
            404: "Not found - the requested resource doesn't exist",
            429: "Rate limited - too many requests",
            500: "Spotify server error",
            502: "Spotify service temporarily unavailable",
            503: "Spotify service temporarily unavailable"
        }
        
        user_message = error_messages.get(response.status_code, f"Spotify API error ({response.status_code})")
        
        # Check for specific error codes in Spotify response
        spotify_error = error_data.get('error', {})
        if isinstance(spotify_error, dict):
            if spotify_error.get('status') == 401:
                # Token expired or invalid
                session.pop('spotify_access_token', None)
                session.pop('spotify_refresh_token', None)
                session.pop('spotify_expires_at', None)
                return jsonify({
                    "error": "Token expired",
                    "message": "Your Spotify authentication has expired. Please log in again.",
                    "code": "SPOTIFY_TOKEN_EXPIRED",
                    "details": spotify_error
                }), 401
            elif spotify_error.get('status') == 403 and 'PREMIUM_REQUIRED' in str(spotify_error):
                return jsonify({
                    "error": "Premium required",
                    "message": "This feature requires Spotify Premium",
                    "code": "SPOTIFY_PREMIUM_REQUIRED",
                    "details": spotify_error
                }), 403
        
        return jsonify({
            "error": "Spotify API request failed",
            "message": user_message,
            "code": f"SPOTIFY_API_ERROR_{response.status_code}",
            "details": error_data,
            "endpoint": endpoint,
            "method": method
        }), response.status_code
        
    except requests.exceptions.Timeout:
        return jsonify({
            "error": "Request timeout",
            "message": "The request to Spotify took too long to complete",
            "code": "SPOTIFY_TIMEOUT"
        }), 504
    except requests.exceptions.ConnectionError:
        return jsonify({
            "error": "Connection error",
            "message": "Unable to connect to Spotify servers",
            "code": "SPOTIFY_CONNECTION_ERROR"
        }), 503
    except Exception as e:
        return jsonify({
            "error": "Request failed",
            "message": f"An unexpected error occurred: {str(e)}",
            "code": "SPOTIFY_UNEXPECTED_ERROR"
        }), 500

# ALBUM ENDPOINTS
@spotify_bp.route('/albums/<album_id>', methods=['GET'])
def get_album(album_id):
    """Get Spotify catalog information for a single album"""
    market = request.args.get('market')
    params = {'market': market} if market else None
    return make_spotify_request(f"albums/{album_id}", params=params)

@spotify_bp.route('/albums', methods=['GET'])
def get_albums():
    """Get multiple albums by their IDs"""
    ids = request.args.get('ids')
    market = request.args.get('market')
    if not ids:
        return jsonify({"error": "ids parameter required"}), 400
    params = {'ids': ids, 'market': market} if market else {'ids': ids}
    return make_spotify_request("albums", params=params)

@spotify_bp.route('/albums/<album_id>/tracks', methods=['GET'])
def get_album_tracks(album_id):
    """Get Spotify catalog information about an album's tracks"""
    market = request.args.get('market')
    limit = request.args.get('limit', 50)
    offset = request.args.get('offset', 0)
    params = {
        'market': market,
        'limit': limit,
        'offset': offset
    }
    params = {k: v for k, v in params.items() if v is not None}
    return make_spotify_request(f"albums/{album_id}/tracks", params=params)

# ARTIST ENDPOINTS
@spotify_bp.route('/artists/<artist_id>', methods=['GET'])
def get_artist(artist_id):
    """Get Spotify catalog information for a single artist"""
    return make_spotify_request(f"artists/{artist_id}")

@spotify_bp.route('/artists', methods=['GET'])
def get_artists():
    """Get multiple artists by their IDs"""
    ids = request.args.get('ids')
    if not ids:
        return jsonify({"error": "ids parameter required"}), 400
    return make_spotify_request("artists", params={'ids': ids})

@spotify_bp.route('/artists/<artist_id>/albums', methods=['GET'])
def get_artist_albums(artist_id):
    """Get Spotify catalog information about an artist's albums"""
    include_groups = request.args.get('include_groups')
    market = request.args.get('market')
    limit = request.args.get('limit', 20)
    offset = request.args.get('offset', 0)
    params = {
        'include_groups': include_groups,
        'market': market,
        'limit': limit,
        'offset': offset
    }
    params = {k: v for k, v in params.items() if v is not None}
    return make_spotify_request(f"artists/{artist_id}/albums", params=params)

@spotify_bp.route('/artists/<artist_id>/top-tracks', methods=['GET'])
def get_artist_top_tracks(artist_id):
    """Get an artist's top tracks by country"""
    market = request.args.get('market', 'US')
    return make_spotify_request(f"artists/{artist_id}/top-tracks", params={'market': market})

@spotify_bp.route('/artists/<artist_id>/related-artists', methods=['GET'])
def get_artist_related_artists(artist_id):
    """Get artists similar to a given artist"""
    return make_spotify_request(f"artists/{artist_id}/related-artists")

# AUDIOBOOK ENDPOINTS
@spotify_bp.route('/audiobooks/<audiobook_id>', methods=['GET'])
def get_audiobook(audiobook_id):
    """Get Spotify catalog information for a single audiobook"""
    market = request.args.get('market')
    params = {'market': market} if market else None
    return make_spotify_request(f"audiobooks/{audiobook_id}", params=params)

@spotify_bp.route('/audiobooks', methods=['GET'])
def get_audiobooks():
    """Get multiple audiobooks by their IDs"""
    ids = request.args.get('ids')
    market = request.args.get('market')
    if not ids:
        return jsonify({"error": "ids parameter required"}), 400
    params = {'ids': ids, 'market': market} if market else {'ids': ids}
    return make_spotify_request("audiobooks", params=params)

@spotify_bp.route('/audiobooks/<audiobook_id>/chapters', methods=['GET'])
def get_audiobook_chapters(audiobook_id):
    """Get Spotify catalog information about an audiobook's chapters"""
    market = request.args.get('market')
    limit = request.args.get('limit', 20)
    offset = request.args.get('offset', 0)
    params = {
        'market': market,
        'limit': limit,
        'offset': offset
    }
    params = {k: v for k, v in params.items() if v is not None}
    return make_spotify_request(f"audiobooks/{audiobook_id}/chapters", params=params)

# CATEGORY ENDPOINTS
@spotify_bp.route('/browse/categories', methods=['GET'])
def get_categories():
    """Get a list of categories used to tag items in Spotify"""
    country = request.args.get('country')
    locale = request.args.get('locale')
    limit = request.args.get('limit', 20)
    offset = request.args.get('offset', 0)
    params = {
        'country': country,
        'locale': locale,
        'limit': limit,
        'offset': offset
    }
    params = {k: v for k, v in params.items() if v is not None}
    return make_spotify_request("browse/categories", params=params)

@spotify_bp.route('/browse/categories/<category_id>', methods=['GET'])
def get_category(category_id):
    """Get a single category used to tag items in Spotify"""
    country = request.args.get('country')
    locale = request.args.get('locale')
    params = {
        'country': country,
        'locale': locale
    }
    params = {k: v for k, v in params.items() if v is not None}
    return make_spotify_request(f"browse/categories/{category_id}", params=params)

@spotify_bp.route('/browse/categories/<category_id>/playlists', methods=['GET'])
def get_category_playlists(category_id):
    """Get a list of Spotify playlists tagged with a particular category"""
    country = request.args.get('country')
    limit = request.args.get('limit', 20)
    offset = request.args.get('offset', 0)
    params = {
        'country': country,
        'limit': limit,
        'offset': offset
    }
    params = {k: v for k, v in params.items() if v is not None}
    return make_spotify_request(f"browse/categories/{category_id}/playlists", params=params)

# EPISODE ENDPOINTS
@spotify_bp.route('/episodes/<episode_id>', methods=['GET'])
def get_episode(episode_id):
    """Get Spotify catalog information for a single episode"""
    market = request.args.get('market')
    params = {'market': market} if market else None
    return make_spotify_request(f"episodes/{episode_id}", params=params)

@spotify_bp.route('/episodes', methods=['GET'])
def get_episodes():
    """Get multiple episodes by their IDs"""
    ids = request.args.get('ids')
    market = request.args.get('market')
    if not ids:
        return jsonify({"error": "ids parameter required"}), 400
    params = {'ids': ids, 'market': market} if market else {'ids': ids}
    return make_spotify_request("episodes", params=params)

# MARKET ENDPOINTS
@spotify_bp.route('/markets', methods=['GET'])
def get_available_markets():
    """Get the list of markets where Spotify is available"""
    return make_spotify_request("markets")

# ENHANCED PLAYLIST ENDPOINTS
@spotify_bp.route('/playlists/<playlist_id>', methods=['GET'])
def get_playlist(playlist_id):
    """Get a playlist"""
    fields = request.args.get('fields')
    market = request.args.get('market')
    additional_types = request.args.get('additional_types', 'track')
    params = {
        'fields': fields,
        'market': market,
        'additional_types': additional_types
    }
    params = {k: v for k, v in params.items() if v is not None}
    return make_spotify_request(f"playlists/{playlist_id}", params=params)

@spotify_bp.route('/playlists/<playlist_id>/tracks', methods=['GET'])
def get_playlist_tracks(playlist_id):
    """Get a playlist's tracks"""
    fields = request.args.get('fields')
    limit = request.args.get('limit', 100)
    offset = request.args.get('offset', 0)
    market = request.args.get('market')
    additional_types = request.args.get('additional_types', 'track,episode')
    params = {
        'fields': fields,
        'limit': limit,
        'offset': offset,
        'market': market,
        'additional_types': additional_types
    }
    params = {k: v for k, v in params.items() if v is not None}
    return make_spotify_request(f"playlists/{playlist_id}/tracks", params=params)

@spotify_bp.route('/playlists/<playlist_id>/tracks', methods=['DELETE'])
def remove_playlist_tracks(playlist_id):
    """Remove tracks from a playlist"""
    if not request.json:
        return jsonify({"error": "No JSON data provided"}), 400
    
    tracks = request.json.get('tracks', [])
    snapshot_id = request.json.get('snapshot_id')
    
    data = {'tracks': tracks}
    if snapshot_id:
        data['snapshot_id'] = snapshot_id
    
    return make_spotify_request(f"playlists/{playlist_id}/tracks", method='DELETE', data=data)

@spotify_bp.route('/playlists/<playlist_id>/tracks', methods=['PUT'])
def replace_playlist_tracks(playlist_id):
    """Replace all tracks in a playlist"""
    if not request.json:
        return jsonify({"error": "No JSON data provided"}), 400
    
    uris = request.json.get('uris', [])
    return make_spotify_request(f"playlists/{playlist_id}/tracks", method='PUT', data={'uris': uris})

@spotify_bp.route('/playlists/<playlist_id>', methods=['PUT'])
def update_playlist_details(playlist_id):
    """Change a playlist's name and public/private state"""
    if not request.json:
        return jsonify({"error": "No JSON data provided"}), 400
    
    data = {}
    if 'name' in request.json:
        data['name'] = request.json['name']
    if 'public' in request.json:
        data['public'] = request.json['public']
    if 'collaborative' in request.json:
        data['collaborative'] = request.json['collaborative']
    if 'description' in request.json:
        data['description'] = request.json['description']
    
    return make_spotify_request(f"playlists/{playlist_id}", method='PUT', data=data)

@spotify_bp.route('/playlists/<playlist_id>/images', methods=['GET'])
def get_playlist_cover_image(playlist_id):
    """Get cover image for a playlist"""
    return make_spotify_request(f"playlists/{playlist_id}/images")

@spotify_bp.route('/playlists/<playlist_id>/images', methods=['PUT'])
def upload_playlist_cover_image(playlist_id):
    """Replace the image used to represent a specific playlist"""
    if not request.json or 'image' not in request.json:
        return jsonify({"error": "Base64 encoded image required"}), 400
    
    # The image should be base64 encoded JPEG
    image_data = request.json['image']
    return make_spotify_request(f"playlists/{playlist_id}/images", method='PUT', data=image_data)

@spotify_bp.route('/playlists/<playlist_id>/followers', methods=['PUT'])
def follow_playlist(playlist_id):
    """Add the current user as a follower of a playlist"""
    public = request.json.get('public', True) if request.json else True
    return make_spotify_request(f"playlists/{playlist_id}/followers", method='PUT', data={'public': public})

@spotify_bp.route('/playlists/<playlist_id>/followers', methods=['DELETE'])
def unfollow_playlist(playlist_id):
    """Remove the current user as a follower of a playlist"""
    return make_spotify_request(f"playlists/{playlist_id}/followers", method='DELETE')

@spotify_bp.route('/playlists/<playlist_id>/followers/contains', methods=['GET'])
def check_if_users_follow_playlist(playlist_id):
    """Check if users are following a playlist"""
    ids = request.args.get('ids')
    if not ids:
        return jsonify({"error": "ids parameter required"}), 400
    return make_spotify_request(f"playlists/{playlist_id}/followers/contains", params={'ids': ids})

@spotify_bp.route('/browse/featured-playlists', methods=['GET'])
def get_featured_playlists():
    """Get a list of Spotify featured playlists"""
    locale = request.args.get('locale')
    country = request.args.get('country')
    timestamp = request.args.get('timestamp')
    limit = request.args.get('limit', 20)
    offset = request.args.get('offset', 0)
    params = {
        'locale': locale,
        'country': country,
        'timestamp': timestamp,
        'limit': limit,
        'offset': offset
    }
    params = {k: v for k, v in params.items() if v is not None}
    return make_spotify_request("browse/featured-playlists", params=params)

# PLAYER/PLAYBACK ENDPOINTS
@spotify_bp.route('/me/player', methods=['GET'])
def get_playback_state():
    """Get information about the user's current playback state"""
    market = request.args.get('market')
    additional_types = request.args.get('additional_types')
    params = {
        'market': market,
        'additional_types': additional_types
    }
    params = {k: v for k, v in params.items() if v is not None}
    return make_spotify_request("me/player", params=params)

@spotify_bp.route('/me/player/devices', methods=['GET'])
def get_available_devices():
    """Get a list of user's available devices"""
    return make_spotify_request("me/player/devices")

@spotify_bp.route('/me/player/currently-playing', methods=['GET'])
def get_currently_playing():
    """Get the user's currently playing track"""
    market = request.args.get('market')
    additional_types = request.args.get('additional_types')
    params = {
        'market': market,
        'additional_types': additional_types
    }
    params = {k: v for k, v in params.items() if v is not None}
    return make_spotify_request("me/player/currently-playing", params=params)

@spotify_bp.route('/me/player/play', methods=['PUT'])
def start_playback():
    """Start/Resume playback"""
    device_id = request.args.get('device_id')
    params = {'device_id': device_id} if device_id else None
    
    data = {}
    if request.json:
        if 'context_uri' in request.json:
            data['context_uri'] = request.json['context_uri']
        if 'uris' in request.json:
            data['uris'] = request.json['uris']
        if 'offset' in request.json:
            data['offset'] = request.json['offset']
        if 'position_ms' in request.json:
            data['position_ms'] = request.json['position_ms']
    
    return make_spotify_request("me/player/play", method='PUT', params=params, data=data if data else None)

@spotify_bp.route('/me/player/pause', methods=['PUT'])
def pause_playback():
    """Pause playback"""
    device_id = request.args.get('device_id')
    params = {'device_id': device_id} if device_id else None
    return make_spotify_request("me/player/pause", method='PUT', params=params)

@spotify_bp.route('/me/player/next', methods=['POST'])
def skip_to_next():
    """Skip to next track"""
    device_id = request.args.get('device_id')
    params = {'device_id': device_id} if device_id else None
    return make_spotify_request("me/player/next", method='POST', params=params)

@spotify_bp.route('/me/player/previous', methods=['POST'])
def skip_to_previous():
    """Skip to previous track"""
    device_id = request.args.get('device_id')
    params = {'device_id': device_id} if device_id else None
    return make_spotify_request("me/player/previous", method='POST', params=params)

@spotify_bp.route('/me/player/seek', methods=['PUT'])
def seek_to_position():
    """Seek to position in currently playing track"""
    position_ms = request.args.get('position_ms')
    device_id = request.args.get('device_id')
    
    if not position_ms:
        return jsonify({"error": "position_ms parameter required"}), 400
    
    params = {'position_ms': position_ms}
    if device_id:
        params['device_id'] = device_id
    
    return make_spotify_request("me/player/seek", method='PUT', params=params)

@spotify_bp.route('/me/player/repeat', methods=['PUT'])
def set_repeat_mode():
    """Set repeat mode for user's playback"""
    state = request.args.get('state')
    device_id = request.args.get('device_id')
    
    if not state or state not in ['track', 'context', 'off']:
        return jsonify({"error": "state must be 'track', 'context', or 'off'"}), 400
    
    params = {'state': state}
    if device_id:
        params['device_id'] = device_id
    
    return make_spotify_request("me/player/repeat", method='PUT', params=params)

@spotify_bp.route('/me/player/volume', methods=['PUT'])
def set_volume():
    """Set volume for user's playback"""
    volume_percent = request.args.get('volume_percent')
    device_id = request.args.get('device_id')
    
    if not volume_percent:
        return jsonify({"error": "volume_percent parameter required"}), 400
    
    try:
        volume = int(volume_percent)
        if volume < 0 or volume > 100:
            return jsonify({"error": "volume_percent must be between 0 and 100"}), 400
    except ValueError:
        return jsonify({"error": "volume_percent must be an integer"}), 400
    
    params = {'volume_percent': volume}
    if device_id:
        params['device_id'] = device_id
    
    return make_spotify_request("me/player/volume", method='PUT', params=params)

@spotify_bp.route('/me/player/shuffle', methods=['PUT'])
def toggle_shuffle():
    """Toggle shuffle for user's playback"""
    state = request.args.get('state')
    device_id = request.args.get('device_id')
    
    if not state or state not in ['true', 'false']:
        return jsonify({"error": "state must be 'true' or 'false'"}), 400
    
    params = {'state': state}
    if device_id:
        params['device_id'] = device_id
    
    return make_spotify_request("me/player/shuffle", method='PUT', params=params)

@spotify_bp.route('/me/player', methods=['PUT'])
def transfer_playback():
    """Transfer playback to a new device"""
    if not request.json or 'device_ids' not in request.json:
        return jsonify({"error": "device_ids required in request body"}), 400
    
    device_ids = request.json['device_ids']
    play = request.json.get('play', False)
    
    return make_spotify_request("me/player", method='PUT', data={'device_ids': device_ids, 'play': play})

@spotify_bp.route('/me/player/queue', methods=['GET'])
def get_queue():
    """Get the user's queue"""
    return make_spotify_request("me/player/queue")

@spotify_bp.route('/me/player/queue', methods=['POST'])
def add_to_queue():
    """Add item to the user's playback queue"""
    uri = request.args.get('uri')
    device_id = request.args.get('device_id')
    
    if not uri:
        return jsonify({"error": "uri parameter required"}), 400
    
    params = {'uri': uri}
    if device_id:
        params['device_id'] = device_id
    
    return make_spotify_request("me/player/queue", method='POST', params=params)

# RECOMMENDATION ENDPOINTS
@spotify_bp.route('/recommendations', methods=['GET'])
def get_recommendations():
    """Get recommendations based on seed artists, tracks, and genres"""
    seed_artists = request.args.get('seed_artists')
    seed_tracks = request.args.get('seed_tracks')
    seed_genres = request.args.get('seed_genres')
    limit = request.args.get('limit', 20)
    market = request.args.get('market')
    
    # At least one seed is required
    if not any([seed_artists, seed_tracks, seed_genres]):
        return jsonify({"error": "At least one seed parameter required (seed_artists, seed_tracks, or seed_genres)"}), 400
    
    params = {
        'seed_artists': seed_artists,
        'seed_tracks': seed_tracks,
        'seed_genres': seed_genres,
        'limit': limit,
        'market': market
    }
    
    # Add tuning parameters if provided
    tuning_params = [
        'min_acousticness', 'max_acousticness', 'target_acousticness',
        'min_danceability', 'max_danceability', 'target_danceability',
        'min_duration_ms', 'max_duration_ms', 'target_duration_ms',
        'min_energy', 'max_energy', 'target_energy',
        'min_instrumentalness', 'max_instrumentalness', 'target_instrumentalness',
        'min_key', 'max_key', 'target_key',
        'min_liveness', 'max_liveness', 'target_liveness',
        'min_loudness', 'max_loudness', 'target_loudness',
        'min_mode', 'max_mode', 'target_mode',
        'min_popularity', 'max_popularity', 'target_popularity',
        'min_speechiness', 'max_speechiness', 'target_speechiness',
        'min_tempo', 'max_tempo', 'target_tempo',
        'min_time_signature', 'max_time_signature', 'target_time_signature',
        'min_valence', 'max_valence', 'target_valence'
    ]
    
    for param in tuning_params:
        value = request.args.get(param)
        if value is not None:
            params[param] = value
    
    params = {k: v for k, v in params.items() if v is not None}
    return make_spotify_request("recommendations", params=params)

@spotify_bp.route('/recommendations/available-genre-seeds', methods=['GET'])
def get_recommendation_genre_seeds():
    """Get available genre seeds for recommendations"""
    return make_spotify_request("recommendations/available-genre-seeds")

# SHOW ENDPOINTS
@spotify_bp.route('/shows/<show_id>', methods=['GET'])
def get_show(show_id):
    """Get Spotify catalog information for a single show"""
    market = request.args.get('market')
    params = {'market': market} if market else None
    return make_spotify_request(f"shows/{show_id}", params=params)

@spotify_bp.route('/shows', methods=['GET'])
def get_shows():
    """Get multiple shows by their IDs"""
    ids = request.args.get('ids')
    market = request.args.get('market')
    if not ids:
        return jsonify({"error": "ids parameter required"}), 400
    params = {'ids': ids, 'market': market} if market else {'ids': ids}
    return make_spotify_request("shows", params=params)

@spotify_bp.route('/shows/<show_id>/episodes', methods=['GET'])
def get_show_episodes(show_id):
    """Get Spotify catalog information about a show's episodes"""
    market = request.args.get('market')
    limit = request.args.get('limit', 50)
    offset = request.args.get('offset', 0)
    params = {
        'market': market,
        'limit': limit,
        'offset': offset
    }
    params = {k: v for k, v in params.items() if v is not None}
    return make_spotify_request(f"shows/{show_id}/episodes", params=params)

# TRACK ENDPOINTS
@spotify_bp.route('/tracks/<track_id>', methods=['GET'])
def get_track(track_id):
    """Get Spotify catalog information for a single track"""
    market = request.args.get('market')
    params = {'market': market} if market else None
    return make_spotify_request(f"tracks/{track_id}", params=params)

@spotify_bp.route('/tracks', methods=['GET'])
def get_tracks():
    """Get multiple tracks by their IDs"""
    ids = request.args.get('ids')
    market = request.args.get('market')
    if not ids:
        return jsonify({"error": "ids parameter required"}), 400
    params = {'ids': ids, 'market': market} if market else {'ids': ids}
    return make_spotify_request("tracks", params=params)

@spotify_bp.route('/audio-features/<track_id>', methods=['GET'])
def get_audio_features(track_id):
    """Get audio features for a track"""
    return make_spotify_request(f"audio-features/{track_id}")

@spotify_bp.route('/audio-features', methods=['GET'])
def get_multiple_audio_features():
    """Get audio features for multiple tracks"""
    ids = request.args.get('ids')
    if not ids:
        return jsonify({"error": "ids parameter required"}), 400
    return make_spotify_request("audio-features", params={'ids': ids})

@spotify_bp.route('/audio-analysis/<track_id>', methods=['GET'])
def get_audio_analysis(track_id):
    """Get audio analysis for a track"""
    return make_spotify_request(f"audio-analysis/{track_id}")

# ENHANCED USER PROFILE ENDPOINTS
@spotify_bp.route('/me', methods=['GET'])
def get_current_user_profile():
    """Get current user's profile"""
    return make_spotify_request("me")

@spotify_bp.route('/users/<user_id>', methods=['GET'])
def get_user_profile(user_id):
    """Get a user's profile"""
    return make_spotify_request(f"users/{user_id}")

@spotify_bp.route('/users/<user_id>/playlists', methods=['GET'])
def get_user_playlists(user_id):
    """Get a user's playlists"""
    limit = request.args.get('limit', 50)
    offset = request.args.get('offset', 0)
    params = {
        'limit': limit,
        'offset': offset
    }
    return make_spotify_request(f"users/{user_id}/playlists", params=params)

@spotify_bp.route('/me/playlists', methods=['GET'])
def get_current_user_playlists():
    """Get current user's playlists"""
    limit = request.args.get('limit', 50)
    offset = request.args.get('offset', 0)
    params = {
        'limit': limit,
        'offset': offset
    }
    return make_spotify_request("me/playlists", params=params)

# USER LIBRARY ENDPOINTS (SAVED ITEMS)
@spotify_bp.route('/me/tracks', methods=['GET'])
def get_user_saved_tracks():
    """Get user's saved tracks"""
    market = request.args.get('market')
    limit = request.args.get('limit', 20)
    offset = request.args.get('offset', 0)
    params = {
        'market': market,
        'limit': limit,
        'offset': offset
    }
    params = {k: v for k, v in params.items() if v is not None}
    return make_spotify_request("me/tracks", params=params)

@spotify_bp.route('/me/tracks', methods=['PUT'])
def save_tracks():
    """Save tracks for current user"""
    ids = request.args.get('ids')
    if not ids:
        return jsonify({"error": "ids parameter required"}), 400
    return make_spotify_request("me/tracks", method='PUT', params={'ids': ids})

@spotify_bp.route('/me/tracks', methods=['DELETE'])
def remove_saved_tracks():
    """Remove saved tracks for current user"""
    ids = request.args.get('ids')
    if not ids:
        return jsonify({"error": "ids parameter required"}), 400
    return make_spotify_request("me/tracks", method='DELETE', params={'ids': ids})

@spotify_bp.route('/me/tracks/contains', methods=['GET'])
def check_saved_tracks():
    """Check if tracks are saved for current user"""
    ids = request.args.get('ids')
    if not ids:
        return jsonify({"error": "ids parameter required"}), 400
    return make_spotify_request("me/tracks/contains", params={'ids': ids})

@spotify_bp.route('/me/albums', methods=['GET'])
def get_user_saved_albums():
    """Get user's saved albums"""
    market = request.args.get('market')
    limit = request.args.get('limit', 20)
    offset = request.args.get('offset', 0)
    params = {
        'market': market,
        'limit': limit,
        'offset': offset
    }
    params = {k: v for k, v in params.items() if v is not None}
    return make_spotify_request("me/albums", params=params)

@spotify_bp.route('/me/albums', methods=['PUT'])
def save_albums():
    """Save albums for current user"""
    ids = request.args.get('ids')
    if not ids:
        return jsonify({"error": "ids parameter required"}), 400
    return make_spotify_request("me/albums", method='PUT', params={'ids': ids})

@spotify_bp.route('/me/albums', methods=['DELETE'])
def remove_saved_albums():
    """Remove saved albums for current user"""
    ids = request.args.get('ids')
    if not ids:
        return jsonify({"error": "ids parameter required"}), 400
    return make_spotify_request("me/albums", method='DELETE', params={'ids': ids})

@spotify_bp.route('/me/albums/contains', methods=['GET'])
def check_saved_albums():
    """Check if albums are saved for current user"""
    ids = request.args.get('ids')
    if not ids:
        return jsonify({"error": "ids parameter required"}), 400
    return make_spotify_request("me/albums/contains", params={'ids': ids})

@spotify_bp.route('/me/shows', methods=['GET'])
def get_user_saved_shows():
    """Get user's saved shows"""
    limit = request.args.get('limit', 20)
    offset = request.args.get('offset', 0)
    params = {
        'limit': limit,
        'offset': offset
    }
    return make_spotify_request("me/shows", params=params)

@spotify_bp.route('/me/shows', methods=['PUT'])
def save_shows():
    """Save shows for current user"""
    ids = request.args.get('ids')
    if not ids:
        return jsonify({"error": "ids parameter required"}), 400
    return make_spotify_request("me/shows", method='PUT', params={'ids': ids})

@spotify_bp.route('/me/shows', methods=['DELETE'])
def remove_saved_shows():
    """Remove saved shows for current user"""
    ids = request.args.get('ids')
    if not ids:
        return jsonify({"error": "ids parameter required"}), 400
    return make_spotify_request("me/shows", method='DELETE', params={'ids': ids})

@spotify_bp.route('/me/shows/contains', methods=['GET'])
def check_saved_shows():
    """Check if shows are saved for current user"""
    ids = request.args.get('ids')
    if not ids:
        return jsonify({"error": "ids parameter required"}), 400
    return make_spotify_request("me/shows/contains", params={'ids': ids})

@spotify_bp.route('/me/episodes', methods=['GET'])
def get_user_saved_episodes():
    """Get user's saved episodes"""
    market = request.args.get('market')
    limit = request.args.get('limit', 20)
    offset = request.args.get('offset', 0)
    params = {
        'market': market,
        'limit': limit,
        'offset': offset
    }
    params = {k: v for k, v in params.items() if v is not None}
    return make_spotify_request("me/episodes", params=params)

@spotify_bp.route('/me/episodes', methods=['PUT'])
def save_episodes():
    """Save episodes for current user"""
    ids = request.args.get('ids')
    if not ids:
        return jsonify({"error": "ids parameter required"}), 400
    return make_spotify_request("me/episodes", method='PUT', params={'ids': ids})

@spotify_bp.route('/me/episodes', methods=['DELETE'])
def remove_saved_episodes():
    """Remove saved episodes for current user"""
    ids = request.args.get('ids')
    if not ids:
        return jsonify({"error": "ids parameter required"}), 400
    return make_spotify_request("me/episodes", method='DELETE', params={'ids': ids})

@spotify_bp.route('/me/episodes/contains', methods=['GET'])
def check_saved_episodes():
    """Check if episodes are saved for current user"""
    ids = request.args.get('ids')
    if not ids:
        return jsonify({"error": "ids parameter required"}), 400
    return make_spotify_request("me/episodes/contains", params={'ids': ids})

# USER FOLLOW ENDPOINTS
@spotify_bp.route('/me/following', methods=['GET'])
def get_followed_artists():
    """Get user's followed artists"""
    type_param = request.args.get('type', 'artist')
    after = request.args.get('after')
    limit = request.args.get('limit', 20)
    params = {
        'type': type_param,
        'after': after,
        'limit': limit
    }
    params = {k: v for k, v in params.items() if v is not None}
    return make_spotify_request("me/following", params=params)

@spotify_bp.route('/me/following', methods=['PUT'])
def follow_artists_or_users():
    """Follow artists or users"""
    type_param = request.args.get('type')
    ids = request.args.get('ids')
    
    if not type_param or type_param not in ['artist', 'user']:
        return jsonify({"error": "type must be 'artist' or 'user'"}), 400
    if not ids:
        return jsonify({"error": "ids parameter required"}), 400
    
    return make_spotify_request("me/following", method='PUT', params={'type': type_param, 'ids': ids})

@spotify_bp.route('/me/following', methods=['DELETE'])
def unfollow_artists_or_users():
    """Unfollow artists or users"""
    type_param = request.args.get('type')
    ids = request.args.get('ids')
    
    if not type_param or type_param not in ['artist', 'user']:
        return jsonify({"error": "type must be 'artist' or 'user'"}), 400
    if not ids:
        return jsonify({"error": "ids parameter required"}), 400
    
    return make_spotify_request("me/following", method='DELETE', params={'type': type_param, 'ids': ids})

@spotify_bp.route('/me/following/contains', methods=['GET'])
def check_if_user_follows():
    """Check if user follows artists or users"""
    type_param = request.args.get('type')
    ids = request.args.get('ids')
    
    if not type_param or type_param not in ['artist', 'user']:
        return jsonify({"error": "type must be 'artist' or 'user'"}), 400
    if not ids:
        return jsonify({"error": "ids parameter required"}), 400
    
    return make_spotify_request("me/following/contains", params={'type': type_param, 'ids': ids})

# USER ACTIVITY ENDPOINTS
@spotify_bp.route('/me/player/recently-played', methods=['GET'])
def get_recently_played():
    """Get recently played tracks"""
    limit = request.args.get('limit', 20)
    after = request.args.get('after')
    before = request.args.get('before')
    params = {
        'limit': limit,
        'after': after,
        'before': before
    }
    params = {k: v for k, v in params.items() if v is not None}
    return make_spotify_request("me/player/recently-played", params=params)

@spotify_bp.route('/me/top/artists', methods=['GET'])
def get_top_artists():
    """Get user's top artists"""
    time_range = request.args.get('time_range', 'medium_term')
    limit = request.args.get('limit', 20)
    offset = request.args.get('offset', 0)
    
    if time_range not in ['short_term', 'medium_term', 'long_term']:
        return jsonify({"error": "time_range must be 'short_term', 'medium_term', or 'long_term'"}), 400
    
    params = {
        'time_range': time_range,
        'limit': limit,
        'offset': offset
    }
    return make_spotify_request("me/top/artists", params=params)

@spotify_bp.route('/me/top/tracks', methods=['GET'])
def get_top_tracks():
    """Get user's top tracks"""
    time_range = request.args.get('time_range', 'medium_term')
    limit = request.args.get('limit', 20)
    offset = request.args.get('offset', 0)
    
    if time_range not in ['short_term', 'medium_term', 'long_term']:
        return jsonify({"error": "time_range must be 'short_term', 'medium_term', or 'long_term'"}), 400
    
    params = {
        'time_range': time_range,
        'limit': limit,
        'offset': offset
    }
    return make_spotify_request("me/top/tracks", params=params)

# BROWSE ENDPOINTS
@spotify_bp.route('/browse/new-releases', methods=['GET'])
def get_new_releases():
    """Get a list of new album releases"""
    country = request.args.get('country')
    limit = request.args.get('limit', 20)
    offset = request.args.get('offset', 0)
    params = {
        'country': country,
        'limit': limit,
        'offset': offset
    }
    params = {k: v for k, v in params.items() if v is not None}
    return make_spotify_request("browse/new-releases", params=params)

# DOCUMENTATION ENDPOINT
@spotify_bp.route('/spotify/endpoints', methods=['GET'])
def list_spotify_endpoints():
    """List all available Spotify API endpoints"""
    endpoints = {
        "authentication": {
            "auth": "GET /spotify/auth - Get authorization URL",
            "callback": "GET|POST /spotify/callback - Handle OAuth callback",
            "status": "GET /spotify/status - Check authentication status",
            "debug": "GET /spotify/debug - Debug authentication info"
        },
        "albums": {
            "get_album": "GET /albums/<album_id> - Get single album",
            "get_albums": "GET /albums?ids=... - Get multiple albums",
            "get_album_tracks": "GET /albums/<album_id>/tracks - Get album tracks"
        },
        "artists": {
            "get_artist": "GET /artists/<artist_id> - Get single artist",
            "get_artists": "GET /artists?ids=... - Get multiple artists",
            "get_artist_albums": "GET /artists/<artist_id>/albums - Get artist albums",
            "get_artist_top_tracks": "GET /artists/<artist_id>/top-tracks - Get artist top tracks",
            "get_artist_related": "GET /artists/<artist_id>/related-artists - Get related artists"
        },
        "audiobooks": {
            "get_audiobook": "GET /audiobooks/<audiobook_id> - Get single audiobook",
            "get_audiobooks": "GET /audiobooks?ids=... - Get multiple audiobooks",
            "get_audiobook_chapters": "GET /audiobooks/<audiobook_id>/chapters - Get audiobook chapters"
        },
        "browse": {
            "get_categories": "GET /browse/categories - Get browse categories",
            "get_category": "GET /browse/categories/<category_id> - Get single category",
            "get_category_playlists": "GET /browse/categories/<category_id>/playlists - Get category playlists",
            "get_featured_playlists": "GET /browse/featured-playlists - Get featured playlists",
            "get_new_releases": "GET /browse/new-releases - Get new releases"
        },
        "episodes": {
            "get_episode": "GET /episodes/<episode_id> - Get single episode",
            "get_episodes": "GET /episodes?ids=... - Get multiple episodes"
        },
        "markets": {
            "get_markets": "GET /markets - Get available markets"
        },
        "playlists": {
            "get_playlist": "GET /playlists/<playlist_id> - Get playlist",
            "get_playlist_tracks": "GET /playlists/<playlist_id>/tracks - Get playlist tracks",
            "create_playlist": "POST /spotify/playlists - Create new playlist",
            "add_tracks": "POST /spotify/playlists/<playlist_id>/tracks - Add tracks to playlist",
            "remove_tracks": "DELETE /playlists/<playlist_id>/tracks - Remove tracks from playlist",
            "replace_tracks": "PUT /playlists/<playlist_id>/tracks - Replace all tracks in playlist",
            "update_playlist": "PUT /playlists/<playlist_id> - Update playlist details",
            "get_cover_image": "GET /playlists/<playlist_id>/images - Get playlist cover",
            "upload_cover": "PUT /playlists/<playlist_id>/images - Upload playlist cover",
            "follow_playlist": "PUT /playlists/<playlist_id>/followers - Follow playlist",
            "unfollow_playlist": "DELETE /playlists/<playlist_id>/followers - Unfollow playlist",
            "check_followers": "GET /playlists/<playlist_id>/followers/contains - Check playlist followers"
        },
        "player": {
            "get_playback_state": "GET /me/player - Get current playback state",
            "get_devices": "GET /me/player/devices - Get available devices",
            "get_currently_playing": "GET /me/player/currently-playing - Get currently playing",
            "start_playback": "PUT /me/player/play - Start/resume playback",
            "pause_playback": "PUT /me/player/pause - Pause playback",
            "skip_next": "POST /me/player/next - Skip to next track",
            "skip_previous": "POST /me/player/previous - Skip to previous track",
            "seek": "PUT /me/player/seek - Seek to position",
            "set_repeat": "PUT /me/player/repeat - Set repeat mode",
            "set_volume": "PUT /me/player/volume - Set volume",
            "toggle_shuffle": "PUT /me/player/shuffle - Toggle shuffle",
            "transfer_playback": "PUT /me/player - Transfer playback to device",
            "get_queue": "GET /me/player/queue - Get user's queue",
            "add_to_queue": "POST /me/player/queue - Add item to queue"
        },
        "recommendations": {
            "get_recommendations": "GET /recommendations - Get track recommendations",
            "get_genre_seeds": "GET /recommendations/available-genre-seeds - Get available genre seeds"
        },
        "search": {
            "search": "GET /spotify/search - Search for tracks, artists, albums, etc."
        },
        "shows": {
            "get_show": "GET /shows/<show_id> - Get single show",
            "get_shows": "GET /shows?ids=... - Get multiple shows",
            "get_show_episodes": "GET /shows/<show_id>/episodes - Get show episodes"
        },
        "tracks": {
            "get_track": "GET /tracks/<track_id> - Get single track",
            "get_tracks": "GET /tracks?ids=... - Get multiple tracks",
            "get_audio_features": "GET /audio-features/<track_id> - Get track audio features",
            "get_multiple_audio_features": "GET /audio-features?ids=... - Get multiple audio features",
            "get_audio_analysis": "GET /audio-analysis/<track_id> - Get track audio analysis"
        },
        "user_profile": {
            "get_current_user": "GET /me - Get current user profile",
            "get_user": "GET /users/<user_id> - Get user profile",
            "get_user_playlists": "GET /users/<user_id>/playlists - Get user playlists",
            "get_current_user_playlists": "GET /me/playlists - Get current user playlists",
            "get_legacy_profile": "GET /spotify/user - Legacy user profile endpoint"
        },
        "user_library": {
            "saved_tracks": {
                "get": "GET /me/tracks - Get saved tracks",
                "save": "PUT /me/tracks - Save tracks",
                "remove": "DELETE /me/tracks - Remove saved tracks",
                "check": "GET /me/tracks/contains - Check if tracks are saved"
            },
            "saved_albums": {
                "get": "GET /me/albums - Get saved albums",
                "save": "PUT /me/albums - Save albums",
                "remove": "DELETE /me/albums - Remove saved albums",
                "check": "GET /me/albums/contains - Check if albums are saved"
            },
            "saved_shows": {
                "get": "GET /me/shows - Get saved shows",
                "save": "PUT /me/shows - Save shows",
                "remove": "DELETE /me/shows - Remove saved shows",
                "check": "GET /me/shows/contains - Check if shows are saved"
            },
            "saved_episodes": {
                "get": "GET /me/episodes - Get saved episodes",
                "save": "PUT /me/episodes - Save episodes",
                "remove": "DELETE /me/episodes - Remove saved episodes",
                "check": "GET /me/episodes/contains - Check if episodes are saved"
            }
        },
        "user_follow": {
            "get_followed": "GET /me/following - Get followed artists",
            "follow": "PUT /me/following - Follow artists or users",
            "unfollow": "DELETE /me/following - Unfollow artists or users",
            "check_following": "GET /me/following/contains - Check if user follows"
        },
        "user_activity": {
            "recently_played": "GET /me/player/recently-played - Get recently played tracks",
            "top_artists": "GET /me/top/artists - Get user's top artists",
            "top_tracks": "GET /me/top/tracks - Get user's top tracks"
        }
    }
    
    return jsonify({
        "message": "Spotify Web API endpoints implemented in this backend",
        "total_categories": len(endpoints),
        "endpoints": endpoints,
        "base_url": "/api",  # Adjust based on your API base path
        "authentication_required": "Most endpoints require Spotify authentication via /spotify/auth"
    })

@spotify_bp.route('/spotify/auth', methods=['GET'])
def spotify_auth():
    # Comprehensive scopes for all implemented endpoints
    scope = " ".join([
        "playlist-modify-public",
        "playlist-modify-private", 
        "playlist-read-private",
        "playlist-read-collaborative",
        "user-read-playback-state",
        "user-modify-playback-state",
        "user-read-currently-playing",
        "user-read-recently-played",
        "user-read-playback-position",
        "user-top-read",
        "user-library-read",
        "user-library-modify",
        "user-follow-read",
        "user-follow-modify",
        "user-read-private",
        "user-read-email",
        "streaming",
        "app-remote-control"
    ])
    auth_url = f"{SPOTIFY_AUTH_URL}?response_type=code&client_id={SPOTIFY_CLIENT_ID}&scope={scope}&redirect_uri={SPOTIFY_REDIRECT_URI}"
    return jsonify({"auth_url": auth_url})

@spotify_bp.route('/spotify/callback', methods=['GET', 'POST'])
def spotify_callback():
    print(f"DEBUG: Received callback request")
    print(f"DEBUG: Method: {request.method}")
    print(f"DEBUG: Args: {request.args}")
    print(f"DEBUG: Content-Type: {request.headers.get('Content-Type')}")
    
    if request.method == 'GET':
        # Handle Spotify's GET callback - redirect to frontend to handle PKCE
        code = request.args.get('code')
        error = request.args.get('error')
        
        if error:
            return f'<script>window.location.href="http://localhost:4200/callback?error={error}";</script>'
        
        if not code:
            return f'<script>window.location.href="http://localhost:4200/callback?error=no_code";</script>'
        
        # Redirect to frontend with the code
        return f'<script>window.location.href="http://localhost:4200/callback?code={code}";</script>'
    else:
        # Handle POST request (from frontend)
        if not request.json:
            return jsonify({"error": "No JSON data provided"}), 400
        
        code = request.json.get('code')
    
    code_verifier = request.json.get('code_verifier') if request.method == 'POST' and request.json else None
    
    print(f"DEBUG: Code: {code}")
    print(f"DEBUG: Code verifier: {code_verifier}")
    
    if not code:
        return jsonify({"error": "No authorization code provided"}), 400
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "client_id": SPOTIFY_CLIENT_ID
    }
    
    # Always require code_verifier for PKCE flow (more secure)
    if not code_verifier:
        return jsonify({"error": "code_verifier required for PKCE flow"}), 400
    
    data["code_verifier"] = code_verifier
    
    response = requests.post(SPOTIFY_TOKEN_URL, headers=headers, data=data)
    
    if response.status_code == 200:
        token_data = response.json()
        session['spotify_access_token'] = token_data['access_token']
        session['spotify_refresh_token'] = token_data.get('refresh_token')
        session['spotify_expires_at'] = datetime.now() + timedelta(seconds=token_data['expires_in'])
        return jsonify({"success": True, "access_token": token_data['access_token']})
    else:
        try:
            error_data = response.json() if 'application/json' in response.headers.get('content-type', '') else {}
        except:
            error_data = {"status_code": response.status_code, "text": response.text}
        return jsonify({"error": "Failed to get access token", "details": error_data}), 400

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
def get_legacy_user_profile():
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
    
    playlist_data = request.json or {}
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
    
    if not request.json:
        return jsonify({"error": "No JSON data provided"}), 400
    
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