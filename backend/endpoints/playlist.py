import requests
from flask import Blueprint, request, jsonify, session
from database import db
from database_helper import get_db_cursor
from spotify_integration import get_or_create_track, search_spotify

playlist_bp = Blueprint('playlist', __name__)

@playlist_bp.route('/playlists', methods=['GET'])
def get_playlists():
    """Get all playlists, optionally filtered by DJ"""
    dj_id = request.args.get('dj_id')
    
    conn, cursor = None, None
    try:
        conn, cursor = get_db_cursor()
        
        if dj_id:
            query = """
                SELECT p.id, p.name, p.description, p.date_created, 
                       p.spotify_playlist_id, d.dj_name, p.posting_dj_id
                FROM Playlist p 
                LEFT JOIN DJ d ON p.posting_dj_id = d.id 
                WHERE p.posting_dj_id = %s AND p.hidden = 0
                ORDER BY p.date_created DESC
            """
            cursor.execute(query, (dj_id,))
        else:
            query = """
                SELECT p.id, p.name, p.description, p.date_created, 
                       p.spotify_playlist_id, d.dj_name, p.posting_dj_id
                FROM Playlist p 
                LEFT JOIN DJ d ON p.posting_dj_id = d.id 
                WHERE p.hidden = 0
                ORDER BY p.date_created DESC
            """
            cursor.execute(query)
        
        playlists = cursor.fetchall()
        return jsonify(playlists)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@playlist_bp.route('/playlists/<int:playlist_id>/tracks', methods=['GET'])
def get_playlist_tracks(playlist_id):
    """Get tracks for a specific playlist using new normalized schema"""
    conn, cursor = None, None
    try:
        conn, cursor = get_db_cursor()
        
        query = """
            SELECT 
                t.id AS track_id,
                t.title,
                t.spotify_track_id,
                a.name AS artist_name,
                al.name AS album_name,
                pt.track_order,
                pt.id AS playlist_track_id
            FROM Playlist_Track pt
            JOIN Track t ON pt.track_id = t.id
            JOIN Artist a ON t.artist_id = a.id
            LEFT JOIN Album al ON t.album_id = al.id
            WHERE pt.playlist_id = %s
            ORDER BY pt.track_order ASC
        """
        cursor.execute(query, (playlist_id,))
        tracks = cursor.fetchall()
        return jsonify(tracks)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

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
        if cursor: cursor.close()
        if conn: conn.close()

# NEW SPOTIFY-POWERED ENDPOINTS

@playlist_bp.route('/search', methods=['GET'])
def search_spotify_tracks():
    """
    A new endpoint to search Spotify.
    This lets the DJ find tracks to add.
    """
    query = request.args.get('q')
    search_type = request.args.get('type', 'track')
    limit = int(request.args.get('limit', 10))
    
    if not query:
        return jsonify({'error': 'Missing "q" query parameter'}), 400
    
    try:
        results = search_spotify(query, search_type, limit)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@playlist_bp.route('/playlists/<int:playlist_id>/tracks', methods=['POST'])
def add_track_to_playlist(playlist_id):
    """
    This is the new "smart" endpoint.
    It accepts a `spotify_track_id` and `track_order`.
    It then uses our helper functions to populate the DB.
    """
    data = request.get_json()
    if not data or 'spotify_track_id' not in data or 'track_order' not in data:
        return jsonify({'error': 'Missing "spotify_track_id" or "track_order"'}), 400

    conn, cursor = None, None
    try:
        conn, cursor = get_db_cursor()
        
        # This is the magic! Get or create track in normalized schema
        local_track_id = get_or_create_track(cursor, data['spotify_track_id'])
        
        if local_track_id is None:
            raise Exception("Could not get or create track.")
        
        # Now, add the local_track_id to the playlist
        sql = "INSERT INTO Playlist_Track (playlist_id, track_id, track_order) VALUES (%s, %s, %s)"
        cursor.execute(sql, (playlist_id, local_track_id, data['track_order']))
        
        conn.commit()
        new_id = cursor.lastrowid
        
        return jsonify({
            'id': new_id,
            'playlist_id': playlist_id,
            'local_track_id': local_track_id,
            **data
        }), 201
        
    except Exception as e:
        if conn: conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@playlist_bp.route('/playlists', methods=['POST'])
def create_playlist():
    """
    Creates a new *local* playlist.
    Does not touch Spotify.
    """
    data = request.get_json()
    if not data or 'name' not in data or 'posting_dj_id' not in data:
        return jsonify({'error': 'Missing required fields: name, posting_dj_id'}), 400

    conn, cursor = None, None
    try:
        conn, cursor = get_db_cursor()
        sql = "INSERT INTO Playlist (name, description, posting_dj_id, hidden) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (
            data['name'],
            data.get('description'),
            data['posting_dj_id'],
            data.get('hidden', False)
        ))
        conn.commit()
        new_id = cursor.lastrowid
        
        return jsonify({'id': new_id, **data}), 201
        
    except Exception as e:
        if conn: conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@playlist_bp.route('/playlists/<int:id>', methods=['GET'])
def get_playlist_with_tracks(id):
    """
    THIS IS THE PAYOFF!
    This endpoint doesn't change at all. It just reads from
    our perfectly normalized local database.
    """
    conn, cursor = None, None
    try:
        conn, cursor = get_db_cursor()
        
        cursor.execute("SELECT p.*, d.dj_name FROM Playlist p JOIN DJ d ON p.posting_dj_id = d.id WHERE p.id = %s", (id,))
        playlist_info = cursor.fetchone()
        
        if not playlist_info:
            return jsonify({'error': 'Playlist not found'}), 404
            
        sql = """
        SELECT
            t.id AS track_id,
            t.title,
            t.spotify_track_id,
            a.name AS artist_name,
            al.name AS album_name,
            pt.track_order,
            pt.id AS playlist_track_id
        FROM Playlist_Track pt
        JOIN Track t ON pt.track_id = t.id
        JOIN Artist a ON t.artist_id = a.id
        LEFT JOIN Album al ON t.album_id = al.id
        WHERE pt.playlist_id = %s
        ORDER BY pt.track_order ASC
        """
        cursor.execute(sql, (id,))
        tracks = cursor.fetchall()
        
        playlist_info['tracks'] = tracks
        return jsonify(playlist_info), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@playlist_bp.route('/playlists/<int:playlist_id>/tracks/<int:playlist_track_id>', methods=['DELETE'])
def remove_track_from_playlist(playlist_id, playlist_track_id):
    """Remove a track from a playlist"""
    conn, cursor = None, None
    try:
        conn, cursor = get_db_cursor()
        
        cursor.execute("SELECT * FROM Playlist_Track WHERE id = %s AND playlist_id = %s", (playlist_track_id, playlist_id))
        item = cursor.fetchone()
        if not item:
            return jsonify({'error': 'Track not found in playlist'}), 404

        cursor.execute("DELETE FROM Playlist_Track WHERE id = %s", (playlist_track_id,))
        conn.commit()
        
        return jsonify({'message': 'Track removed from playlist'}), 200
        
    except Exception as e:
        if conn: conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@playlist_bp.route('/playlists/<int:id>/publish', methods=['POST'])
def publish_playlist_to_spotify(id):
    """
    This is a STUB endpoint to show how you would
    "publish" your local playlist to Spotify.
    
    This requires the much more complex User Auth (SpotifyOAuth)
    flow, as you are acting on behalf of a user.
    """
    # 1. Get local playlist and all its local track IDs
    # 2. Convert all local track IDs to spotify_track_ids
    # 3. Use `spotipy.Spotify(auth_manager=SpotifyOAuth(...))`
    # 4. Call `sp.user_playlist_create(...)`
    # 5. Call `sp.playlist_add_items(...)` with the list of spotify_track_ids
    # 6. Save the new `spotify_playlist_id` to our Playlist table
    
    return jsonify({'message': 'Endpoint stub for publishing to Spotify. Requires SpotifyOAuth.'}), 501