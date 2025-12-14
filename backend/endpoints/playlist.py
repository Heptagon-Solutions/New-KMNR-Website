from flask import Blueprint, jsonify, request
from database import db, DatabaseError
import json

playlist_bp = Blueprint('playlist', __name__)

# Sample playlist data for development
SAMPLE_PLAYLIST_DATA = [
    {
        "id": 1,
        "artist": "The Strokes",
        "title": "Last Nite",
        "album": "Is This It",
        "genre": "Indie Rock",
        "played_at": "2024-12-14T10:30:00Z",
        "dj_name": "Indie Isaac"
    },
    {
        "id": 2,
        "artist": "Led Zeppelin",
        "title": "Stairway to Heaven",
        "album": "Led Zeppelin IV",
        "genre": "Classic Rock",
        "played_at": "2024-12-14T10:15:00Z",
        "dj_name": "Mining Mike"
    },
    {
        "id": 3,
        "artist": "Daft Punk",
        "title": "One More Time",
        "album": "Discovery",
        "genre": "Electronic",
        "played_at": "2024-12-14T10:00:00Z",
        "dj_name": "Techno Tyler"
    },
    {
        "id": 4,
        "artist": "Miles Davis",
        "title": "Kind of Blue",
        "album": "Kind of Blue",
        "genre": "Jazz",
        "played_at": "2024-12-14T09:45:00Z",
        "dj_name": "Jazz Jessica"
    },
    {
        "id": 5,
        "artist": "Metallica",
        "title": "Enter Sandman",
        "album": "Metallica",
        "genre": "Heavy Metal",
        "played_at": "2024-12-14T09:30:00Z",
        "dj_name": "Metal Miner"
    },
    {
        "id": 6,
        "artist": "Taylor Swift",
        "title": "Anti-Hero",
        "album": "Midnights",
        "genre": "Pop",
        "played_at": "2024-12-14T09:15:00Z",
        "dj_name": "Pop Princess"
    },
    {
        "id": 7,
        "artist": "Johnny Cash",
        "title": "Ring of Fire",
        "album": "Ring of Fire: The Best of Johnny Cash",
        "genre": "Country",
        "played_at": "2024-12-14T09:00:00Z",
        "dj_name": "Country Chris"
    },
    {
        "id": 8,
        "artist": "Radiohead",
        "title": "Creep",
        "album": "Pablo Honey",
        "genre": "Alternative",
        "played_at": "2024-12-14T08:45:00Z",
        "dj_name": "Indie Isaac"
    },
    {
        "id": 9,
        "artist": "Bon Iver",
        "title": "Holocene",
        "album": "Bon Iver, Bon Iver",
        "genre": "Indie Folk",
        "played_at": "2024-12-14T08:30:00Z",
        "dj_name": "Ambient Adam"
    },
    {
        "id": 10,
        "artist": "The Ramones",
        "title": "Blitzkrieg Bop",
        "album": "Ramones",
        "genre": "Punk",
        "played_at": "2024-12-14T08:15:00Z",
        "dj_name": "Punk Pete"
    }
]

@playlist_bp.route('/recent', methods=['GET'])
def get_recent_tracks():
    limit = request.args.get('limit', 50, type=int)
    
    try:
        cursor = db.connection.cursor()
        
        # Query the existing database structure
        cursor.execute("""
            SELECT 
                p.id, 
                pt.artist, 
                pt.song as title, 
                pt.album, 
                'Unknown' as genre,
                p.date_played as played_at, 
                COALESCE(d.dj_name, 'Unknown DJ') as dj_name
            FROM playlist p
            LEFT JOIN playlist_track pt ON p.id = pt.playlist_id
            LEFT JOIN dj d ON p.posting_dj_id = d.id
            WHERE p.hidden = 0 AND pt.song IS NOT NULL
            ORDER BY p.date_played DESC, pt.track ASC
            LIMIT %s
        """, (limit,))
        
        tracks = cursor.fetchall()
        
        if tracks:
            # Convert to list of dictionaries (track is already a dict due to DictCursor)
            result = []
            for track in tracks:
                result.append({
                    'id': track['id'],
                    'artist': track['artist'],
                    'title': track['title'],
                    'album': track['album'] if track['album'] else 'Unknown Album',
                    'genre': track['genre'],
                    'played_at': track['played_at'].isoformat() + 'Z' if track['played_at'] else None,
                    'dj_name': track['dj_name']
                })
            
            cursor.close()
            return jsonify(result)
        else:
            # If no data in database, return sample data
            cursor.close()
            return jsonify(SAMPLE_PLAYLIST_DATA[:limit])
            
    except DatabaseError as e:
        print(f"Database error: {e}")
        # Fallback to sample data if database fails
        return jsonify(SAMPLE_PLAYLIST_DATA[:limit])
    except Exception as e:
        print(f"Error fetching recent tracks: {e}")
        return jsonify(SAMPLE_PLAYLIST_DATA[:limit])

@playlist_bp.route('/dj/<int:dj_id>', methods=['GET'])
def get_tracks_by_dj(dj_id):
    try:
        cursor = db.connection.cursor()
        
        cursor.execute("""
            SELECT 
                p.id, 
                pt.artist, 
                pt.song as title, 
                pt.album, 
                'Unknown' as genre,
                p.date_played as played_at, 
                d.dj_name
            FROM playlist p
            LEFT JOIN playlist_track pt ON p.id = pt.playlist_id
            LEFT JOIN dj d ON p.posting_dj_id = d.id
            WHERE p.posting_dj_id = %s AND p.hidden = 0 AND pt.song IS NOT NULL
            ORDER BY p.date_played DESC, pt.track ASC
        """, (dj_id,))
        
        tracks = cursor.fetchall()
        
        if tracks:
            result = []
            for track in tracks:
                result.append({
                    'id': track['id'],
                    'artist': track['artist'],
                    'title': track['title'],
                    'album': track['album'] if track['album'] else 'Unknown Album',
                    'genre': track['genre'],
                    'played_at': track['played_at'].isoformat() + 'Z' if track['played_at'] else None,
                    'dj_name': track['dj_name']
                })
            
            cursor.close()
            return jsonify(result)
        else:
            cursor.close()
            # Filter sample data by DJ name containing the ID (fallback)
            filtered_data = [track for track in SAMPLE_PLAYLIST_DATA 
                           if str(dj_id) in track['dj_name'].lower()]
            return jsonify(filtered_data)
            
    except DatabaseError as e:
        print(f"Database error: {e}")
        filtered_data = [track for track in SAMPLE_PLAYLIST_DATA 
                       if str(dj_id) in track['dj_name'].lower()]
        return jsonify(filtered_data)
    except Exception as e:
        print(f"Error fetching tracks by DJ: {e}")
        return jsonify([])

@playlist_bp.route('/by-dj/<int:dj_id>', methods=['GET'])
def get_playlists_by_dj(dj_id):
    try:
        cursor = db.connection.cursor()
        
        cursor.execute("""
            SELECT 
                p.id,
                p.name,
                p.description,
                p.date_played,
                p.posting_dj_id as dj_id,
                d.dj_name,
                COUNT(pt.playlist_id) as track_count
            FROM playlist p
            LEFT JOIN dj d ON p.posting_dj_id = d.id
            LEFT JOIN playlist_track pt ON p.id = pt.playlist_id
            WHERE p.posting_dj_id = %s AND p.hidden = 0
            GROUP BY p.id, p.name, p.description, p.date_played, p.posting_dj_id, d.dj_name
            ORDER BY p.date_played DESC
        """, (dj_id,))
        
        playlists = cursor.fetchall()
        
        result = []
        for playlist in playlists:
            result.append({
                'id': playlist['id'],
                'name': playlist['name'] or f'Untitled Playlist {playlist["id"]}',
                'description': playlist['description'],
                'date_played': playlist['date_played'].isoformat() + 'Z' if playlist['date_played'] else None,
                'dj_id': playlist['dj_id'],
                'dj_name': playlist['dj_name'],
                'track_count': playlist['track_count']
            })
        
        cursor.close()
        return jsonify(result)
        
    except DatabaseError as e:
        print(f"Database error: {e}")
        return jsonify([])
    except Exception as e:
        print(f"Error fetching playlists by DJ: {e}")
        return jsonify([])

@playlist_bp.route('/all', methods=['GET'])
def get_all_playlists():
    try:
        cursor = db.connection.cursor()
        
        cursor.execute("""
            SELECT 
                p.id,
                p.name,
                p.description,
                p.date_played,
                p.posting_dj_id as dj_id,
                d.dj_name,
                COUNT(pt.playlist_id) as track_count
            FROM playlist p
            LEFT JOIN dj d ON p.posting_dj_id = d.id
            LEFT JOIN playlist_track pt ON p.id = pt.playlist_id
            WHERE p.hidden = 0
            GROUP BY p.id, p.name, p.description, p.date_played, p.posting_dj_id, d.dj_name
            ORDER BY p.date_played DESC
        """, ())
        
        playlists = cursor.fetchall()
        
        result = []
        for playlist in playlists:
            result.append({
                'id': playlist['id'],
                'name': playlist['name'] or f'Untitled Playlist {playlist["id"]}',
                'description': playlist['description'],
                'date_played': playlist['date_played'].isoformat() + 'Z' if playlist['date_played'] else None,
                'dj_id': playlist['dj_id'],
                'dj_name': playlist['dj_name'],
                'track_count': playlist['track_count']
            })
        
        cursor.close()
        return jsonify(result)
        
    except DatabaseError as e:
        print(f"Database error: {e}")
        return jsonify([])
    except Exception as e:
        print(f"Error fetching all playlists: {e}")
        return jsonify([])

@playlist_bp.route('/<int:playlist_id>', methods=['GET'])
def get_playlist_details(playlist_id):
    try:
        cursor = db.connection.cursor()
        
        # Get playlist info
        cursor.execute("""
            SELECT 
                p.id,
                p.name,
                p.description,
                p.date_played,
                p.posting_dj_id as dj_id,
                d.dj_name
            FROM playlist p
            LEFT JOIN dj d ON p.posting_dj_id = d.id
            WHERE p.id = %s AND p.hidden = 0
        """, (playlist_id,))
        
        playlist = cursor.fetchone()
        
        if not playlist:
            cursor.close()
            return jsonify({'error': 'Playlist not found'}), 404
        
        # Get tracks for this playlist
        cursor.execute("""
            SELECT 
                pt.track as track_number,
                pt.song as title,
                pt.artist,
                pt.album
            FROM playlist_track pt
            WHERE pt.playlist_id = %s
            ORDER BY pt.track ASC
        """, (playlist_id,))
        
        tracks = cursor.fetchall()
        
        result = {
            'id': playlist['id'],
            'name': playlist['name'] or f'Untitled Playlist {playlist["id"]}',
            'description': playlist['description'],
            'date_played': playlist['date_played'].isoformat() + 'Z' if playlist['date_played'] else None,
            'dj_id': playlist['dj_id'],
            'dj_name': playlist['dj_name'],
            'tracks': []
        }
        
        for track in tracks:
            result['tracks'].append({
                'track_number': track['track_number'],
                'title': track['title'],
                'artist': track['artist'],
                'album': track['album']
            })
        
        cursor.close()
        return jsonify(result)
        
    except DatabaseError as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error'}), 500
    except Exception as e:
        print(f"Error fetching playlist details: {e}")
        return jsonify({'error': 'Internal error'}), 500

@playlist_bp.route('/add', methods=['POST'])
def add_track():
    try:
        data = request.get_json()
        
        cursor = db.connection.cursor()
        
        cursor.execute("""
            INSERT INTO playlist_entries (artist, title, album, genre, played_at, dj_name, dj_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data['artist'],
            data['title'], 
            data['album'],
            data['genre'],
            data['played_at'],
            data['dj_name'],
            data.get('dj_id')
        ))
        
        db.connection.commit()
        cursor.close()
        
        return jsonify({'success': True, 'message': 'Track added successfully'})
        
    except DatabaseError as e:
        print(f"Database error: {e}")
        return jsonify({'success': False, 'error': 'Database error'}), 500
    except Exception as e:
        print(f"Error adding track: {e}")
        return jsonify({'success': False, 'error': 'Failed to add track'}), 500