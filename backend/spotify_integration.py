"""Spotify integration using spotipy with the new normalized database schema."""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from database_helper import get_db_cursor

# Spotipy Setup - Uses Client Credentials flow (server-to-server)
try:
    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)
    if not os.environ.get("SPOTIPY_CLIENT_ID") or not os.environ.get("SPOTIPY_CLIENT_SECRET"):
        print("Warning: SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET env vars not set. API calls may fail.")
except Exception as e:
    print(f"Error initializing Spotipy: {e}")
    sp = None

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

def search_spotify(query, search_type='track', limit=10):
    """Search Spotify and return results."""
    if not sp:
        raise Exception("Spotipy is not initialized.")
    
    try:
        results = sp.search(q=query, type=search_type, limit=limit)
        return results
    except Exception as e:
        raise Exception(f"Spotify search failed: {str(e)}")