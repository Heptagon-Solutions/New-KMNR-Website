import requests
from flask import Blueprint, request, jsonify, session
from database import db

playlist_bp = Blueprint('playlist', __name__)

@playlist_bp.route('/playlists', methods=['GET'])
def get_playlists():
    """Get all playlists, optionally filtered by DJ"""
    dj_id = request.args.get('dj_id')
    
    connection = db.connection
    cursor = connection.cursor()
    
    try:
        if dj_id:
            query = """
                SELECT p.id, p.name, p.description, p.date_played, 
                       p.spotify_playlist_id, d.dj_name, p.posting_dj_id
                FROM playlist p 
                LEFT JOIN dj d ON p.posting_dj_id = d.id 
                WHERE p.posting_dj_id = %s AND p.hidden = 0
                ORDER BY p.date_played DESC
            """
            cursor.execute(query, (dj_id,))
        else:
            query = """
                SELECT p.id, p.name, p.description, p.date_played, 
                       p.spotify_playlist_id, d.dj_name, p.posting_dj_id
                FROM playlist p 
                LEFT JOIN dj d ON p.posting_dj_id = d.id 
                WHERE p.hidden = 0
                ORDER BY p.date_played DESC
            """
            cursor.execute(query)
        
        playlists = cursor.fetchall()
        return jsonify(playlists)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@playlist_bp.route('/playlists/<int:playlist_id>/tracks', methods=['GET'])
def get_playlist_tracks(playlist_id):
    """Get tracks for a specific playlist"""
    connection = db.connection
    cursor = connection.cursor()
    
    try:
        query = """
            SELECT track, song, artist, album 
            FROM playlist_track 
            WHERE playlist_id = %s 
            ORDER BY track
        """
        cursor.execute(query, (playlist_id,))
        tracks = cursor.fetchall()
        return jsonify(tracks)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@playlist_bp.route('/playlists/<int:playlist_id>/publish-to-spotify', methods=['POST'])
def publish_to_spotify(playlist_id):
    """Publish a KMNR playlist to Spotify"""
    access_token = session.get('spotify_access_token')
    if not access_token:
        return jsonify({"error": "Not authenticated with Spotify"}), 401
    
    connection = db.connection
    cursor = connection.cursor()
    
    try:
        # Get playlist info
        playlist_query = """
            SELECT p.id, p.name, p.description, p.spotify_playlist_id
            FROM playlist p 
            WHERE p.id = %s
        """
        cursor.execute(playlist_query, (playlist_id,))
        playlist_info = cursor.fetchone()
        
        if not playlist_info:
            return jsonify({"error": "Playlist not found"}), 404
            
        if playlist_info['spotify_playlist_id']:
            return jsonify({"error": "Playlist already published to Spotify"}), 400
        
        # Get tracks for the playlist
        tracks_query = """
            SELECT song, artist, album 
            FROM playlist_track 
            WHERE playlist_id = %s 
            ORDER BY track
        """
        cursor.execute(tracks_query, (playlist_id,))
        tracks = cursor.fetchall()
        
        if not tracks:
            return jsonify({"error": "No tracks found in playlist"}), 400
        
        # Create Spotify playlist
        spotify_name = playlist_info['name'] or f"KMNR Playlist {playlist_id}"
        spotify_description = playlist_info['description'] or "Published from KMNR website"
        
        # Call Spotify API to create playlist
        user_response = requests.get("https://api.spotify.com/v1/me", 
                                   headers={"Authorization": f"Bearer {access_token}"})
        
        if user_response.status_code != 200:
            return jsonify({"error": "Failed to get Spotify user info"}), 400
        
        user_id = user_response.json()['id']
        
        # Create playlist
        playlist_data = {
            "name": spotify_name,
            "description": spotify_description,
            "public": True
        }
        
        create_response = requests.post(
            f"https://api.spotify.com/v1/users/{user_id}/playlists",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            json=playlist_data
        )
        
        if create_response.status_code != 201:
            return jsonify({"error": "Failed to create Spotify playlist"}), 400
        
        spotify_playlist = create_response.json()
        spotify_playlist_id = spotify_playlist['id']
        
        # Search for tracks and add them to playlist
        track_uris = []
        for track in tracks:
            search_query = f"track:{track['song']} artist:{track['artist']}"
            search_response = requests.get(
                "https://api.spotify.com/v1/search",
                headers={"Authorization": f"Bearer {access_token}"},
                params={"q": search_query, "type": "track", "limit": 1}
            )
            
            if search_response.status_code == 200:
                search_results = search_response.json()
                if search_results['tracks']['items']:
                    track_uris.append(search_results['tracks']['items'][0]['uri'])
        
        # Add tracks to Spotify playlist if any were found
        if track_uris:
            add_tracks_response = requests.post(
                f"https://api.spotify.com/v1/playlists/{spotify_playlist_id}/tracks",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                },
                json={"uris": track_uris}
            )
        
        # Update database with Spotify playlist ID
        update_query = """
            UPDATE playlist 
            SET spotify_playlist_id = %s 
            WHERE id = %s
        """
        cursor.execute(update_query, (spotify_playlist_id, playlist_id))
        connection.commit()
        
        return jsonify({
            "success": True,
            "spotify_playlist_id": spotify_playlist_id,
            "spotify_url": spotify_playlist['external_urls']['spotify'],
            "tracks_added": len(track_uris),
            "total_tracks": len(tracks)
        })
        
    except Exception as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()