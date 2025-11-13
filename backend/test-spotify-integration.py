#!/usr/bin/env python3

import os
import requests
import json
from database_helper import get_db_cursor

def test_spotify_integration():
    """Test the complete Spotify integration workflow"""
    print("🧪 Testing Complete Spotify Integration")
    print("Setting up mock Spotify environment...")
    
    # Set mock Spotify credentials for testing
    os.environ["SPOTIPY_CLIENT_ID"] = "mock_client_id"
    os.environ["SPOTIPY_CLIENT_SECRET"] = "mock_client_secret"
    
    BASE_URL = "http://localhost:5001"
    
    # Test 1: Create a playlist
    print("\n1. Testing playlist creation...")
    playlist_data = {
        "name": "Integration Test Playlist",
        "description": "Testing normalized database with Spotify integration",
        "posting_dj_id": 1,
        "hidden": False
    }
    
    response = requests.post(f"{BASE_URL}/playlists", json=playlist_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        playlist = response.json()
        playlist_id = playlist['id']
        print(f"✅ Created playlist: {playlist['name']} (ID: {playlist_id})")
    else:
        print(f"❌ Failed to create playlist: {response.text}")
        return False
    
    # Test 2: Test track addition (without real Spotify API)
    print("\n2. Testing direct database track addition...")
    try:
        conn, cursor = get_db_cursor()
        
        # Get existing artist and album IDs
        cursor.execute("SELECT id FROM Artist LIMIT 1")
        artist_result = cursor.fetchone()
        artist_id = artist_result['id'] if artist_result else None
        
        cursor.execute("SELECT id FROM Album LIMIT 1")
        album_result = cursor.fetchone()
        album_id = album_result['id'] if album_result else None
        
        if not artist_id:
            # Create test artist if none exists
            cursor.execute("INSERT INTO Artist (name, spotify_artist_id) VALUES ('Test Artist', 'test_artist_123')")
            artist_id = cursor.lastrowid
            print(f"Created test artist (ID: {artist_id})")
        
        # Add a test track directly to database
        cursor.execute("""INSERT INTO Track (title, artist_id, album_id, spotify_track_id)
            VALUES ('Test Song', %s, %s, 'test_spotify_id_12345')""", (artist_id, album_id))
        track_id = cursor.lastrowid
        
        # Add track to playlist
        cursor.execute("""INSERT INTO Playlist_Track (playlist_id, track_id, track_order)
            VALUES (%s, %s, 1)""", (playlist_id, track_id))
        
        conn.commit()
        print(f"✅ Added test track to playlist (Track ID: {track_id})")
        
    except Exception as e:
        print(f"❌ Failed to add track: {e}")
        return False
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()
    
    # Test 3: Verify playlist with tracks
    print("\n3. Testing playlist retrieval with tracks...")
    response = requests.get(f"{BASE_URL}/playlists/{playlist_id}")
    if response.status_code == 200:
        playlist = response.json()
        print(f"✅ Retrieved playlist: {playlist['name']}")
        print(f"   Tracks: {len(playlist['tracks'])}")
        for track in playlist['tracks']:
            print(f"     - {track['title']} by {track['artist_name']}")
    else:
        print(f"❌ Failed to retrieve playlist: {response.text}")
        return False
    
    # Test 4: Test all playlists endpoint
    print("\n4. Testing all playlists endpoint...")
    response = requests.get(f"{BASE_URL}/playlists")
    if response.status_code == 200:
        playlists = response.json()
        print(f"✅ Retrieved {len(playlists)} playlists")
        for playlist in playlists[-2:]:  # Show last 2 playlists
            print(f"   - {playlist['name']} by {playlist['dj_name']}")
    else:
        print(f"❌ Failed to retrieve playlists: {response.text}")
        return False
    
    print("\n✅ All integration tests passed!")
    return True

if __name__ == "__main__":
    success = test_spotify_integration()
    print(f"\nFinal result: {'✅ SUCCESS' if success else '❌ FAILURE'}")
    exit(0 if success else 1)