"""
New Spotify-Powered Playlist API
Following the tutorial's normalized database approach with spotipy integration.
"""

import os
from flask import Flask, jsonify, request
import pymysql
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Database helper function
def get_db_cursor():
    """
    Get database connection and cursor.
    Replace with your actual database connection logic.
    """
    try:
        connection = pymysql.connect(
            host='localhost',
            user=os.environ.get('DB_USER', 'kwip'),
            password=os.environ.get('DB_PASS', 'kwip-password'),
            database='kwip',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False
        )
        return connection, connection.cursor()
    except Exception as e:
        print(f"Database connection error: {e}")
        raise

# Spotipy setup
try:
    if os.environ.get("SPOTIPY_CLIENT_ID") and os.environ.get("SPOTIPY_CLIENT_SECRET"):
        auth_manager = SpotifyClientCredentials()
        sp = spotipy.Spotify(auth_manager=auth_manager)
        print("✅ Spotipy initialized successfully")
    else:
        print("⚠️  Warning: SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET env vars not set. API calls may fail.")
        sp = None
except Exception as e:
    print(f"❌ Error initializing Spotipy: {e}")
    sp = None

# Flask app setup
app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

# ==========================================
# SPOTIPY "GET-OR-CREATE" HELPER FUNCTIONS
# ==========================================

def get_or_create_artist(cursor, sp_artist_data):
    """
    Finds an artist in our DB by spotify_artist_id.
    If not found, creates them.
    Returns our local artist ID.
    """
    spotify_id = sp_artist_data['id']
    name = sp_artist_data['name']
    
    sql = "SELECT id FROM Artist WHERE spotify_artist_id = %s"
    cursor.execute(sql, (spotify_id,))
    artist = cursor.fetchone()
    
    if artist:
        return artist['id']
    else:
        # Artist not in our DB, so create them
        sql = "INSERT INTO Artist (name, spotify_artist_id) VALUES (%s, %s)"
        cursor.execute(sql, (name, spotify_id))
        return cursor.lastrowid

def get_or_create_album(cursor, sp_album_data, local_artist_id):
    """
    Finds or creates an album.
    Requires the local_artist_id from get_or_create_artist.
    Returns our local album ID.
    """
    spotify_id = sp_album_data['id']
    name = sp_album_data['name']
    
    sql = "SELECT id FROM Album WHERE spotify_album_id = %s"
    cursor.execute(sql, (spotify_id,))
    album = cursor.fetchone()
    
    if album:
        return album['id']
    else:
        # Album not in our DB, so create it
        sql = "INSERT INTO Album (name, artist_id, spotify_album_id) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, local_artist_id, spotify_id))
        return cursor.lastrowid

def get_or_create_track(cursor, spotify_track_id):
    """
    This is the main "sync" function.
    Given a spotify_track_id, it fetches data from Spotify
    and populates Artist, Album, and Track tables in our DB.
    Returns our local track ID.
    """
    sql = "SELECT id FROM Track WHERE spotify_track_id = %s"
    cursor.execute(sql, (spotify_track_id,))
    track = cursor.fetchone()
    
    if track:
        # Track is already in our DB
        return track['id']
    
    # Track not found, fetch from Spotify
    if not sp:
        raise Exception("Spotipy is not initialized.")
    
    try:
        sp_track_data = sp.track(spotify_track_id)
    except Exception as e:
        print(f"Error fetching from Spotify: {e}")
        return None

    # 1. Get/Create Artist
    # We'll use the primary artist for simplicity
    sp_artist_data = sp_track_data['artists'][0]
    local_artist_id = get_or_create_artist(cursor, sp_artist_data)
    
    # 2. Get/Create Album
    sp_album_data = sp_track_data['album']
    local_album_id = get_or_create_album(cursor, sp_album_data, local_artist_id)
    
    # 3. Create Track
    title = sp_track_data['name']
    sql = "INSERT INTO Track (title, artist_id, album_id, spotify_track_id) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (title, local_artist_id, local_album_id, spotify_track_id))
    return cursor.lastrowid

# ==========================================
# NEW SPOTIFY-POWERED API ENDPOINTS
# ==========================================

@app.route('/search', methods=['GET'])
def search_spotify():
    """
    A new endpoint to search Spotify.
    This lets the DJ find tracks to add.
    """
    query = request.args.get('q')
    search_type = request.args.get('type', 'track')
    limit = int(request.args.get('limit', 10))

    if not query:
        return bad_request("Missing 'q' query parameter.")
    if not sp:
        return jsonify({'error': 'Spotipy not configured on server'}), 500

    try:
        results = sp.search(q=query, type=search_type, limit=limit)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/playlists/<int:playlist_id>/tracks', methods=['POST'])
def add_track_to_playlist(playlist_id):
    """
    This is the new "smart" endpoint.
    It accepts a `spotify_track_id` and `track_order`.
    It then uses our helper functions to populate the DB.
    """
    data = request.get_json()
    if not data or 'spotify_track_id' not in data or 'track_order' not in data:
        return bad_request("Missing 'spotify_track_id' or 'track_order'.")

    conn, cursor = None, None
    try:
        conn, cursor = get_db_cursor()
        
        # This is the magic!
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
        if conn: 
            conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor: 
            cursor.close()
        if conn: 
            conn.close()

# ==========================================
# STANDARD CRUD ENDPOINTS
# ==========================================

@app.route('/playlists', methods=['POST'])
def create_playlist():
    """
    Creates a new *local* playlist.
    Does not touch Spotify.
    """
    data = request.get_json()
    if not data or 'name' not in data or 'posting_dj_id' not in data:
        return bad_request("Missing required fields")

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
        if conn:
            conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/playlists', methods=['GET'])
def get_all_playlists():
    conn, cursor = None, None
    try:
        conn, cursor = get_db_cursor()
        sql = """
        SELECT p.*, d.dj_name
        FROM Playlist p
        JOIN DJ d ON p.posting_dj_id = d.id
        ORDER BY p.date_created DESC
        """
        cursor.execute(sql)
        playlists = cursor.fetchall()
        return jsonify(playlists), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/playlists/<int:id>', methods=['GET'])
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
            return not_found(None)
            
        sql = """
        SELECT
            t.id AS track_id,
            t.title,
            t.spotify_track_id,
            a.name AS artist_name,
            a.spotify_artist_id,
            al.name AS album_name,
            al.spotify_album_id,
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
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/playlists/<int:playlist_id>/tracks/<int:playlist_track_id>', methods=['DELETE'])
def remove_track_from_playlist(playlist_id, playlist_track_id):
    conn, cursor = None, None
    try:
        conn, cursor = get_db_cursor()
        
        cursor.execute("SELECT * FROM Playlist_Track WHERE id = %s AND playlist_id = %s", (playlist_track_id, playlist_id))
        item = cursor.fetchone()
        if not item:
            return not_found(None)

        cursor.execute("DELETE FROM Playlist_Track WHERE id = %s", (playlist_track_id,))
        conn.commit()
        
        return jsonify({'message': 'Track removed from playlist'}), 200
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# ==========================================
# TESTING AND STATUS ENDPOINTS
# ==========================================

@app.route('/test/spotipy', methods=['GET'])
def test_spotipy():
    """Test endpoint to verify Spotify integration works"""
    if not sp:
        return jsonify({'error': 'Spotipy not configured'}), 500
    
    try:
        # Test with a simple search
        results = sp.search(q='test', type='track', limit=1)
        return jsonify({
            'status': 'Spotipy working!',
            'test_search_results_count': len(results['tracks']['items'])
        }), 200
    except Exception as e:
        return jsonify({'error': f'Spotipy error: {str(e)}'}), 500

@app.route('/status', methods=['GET'])
def status():
    """Health check endpoint"""
    conn, cursor = None, None
    try:
        conn, cursor = get_db_cursor()
        cursor.execute("SELECT COUNT(*) as playlist_count FROM Playlist")
        result = cursor.fetchone()
        
        return jsonify({
            'status': 'API is running',
            'database': 'connected',
            'spotipy': 'configured' if sp else 'not configured',
            'playlists_in_db': result['playlist_count'] if result else 0
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'API is running',
            'database': f'error: {str(e)}',
            'spotipy': 'configured' if sp else 'not configured'
        }), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)