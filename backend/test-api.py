#!/usr/bin/env python3

import requests
import json
import os

# Base URL for the API
BASE_URL = "http://localhost:5001"

def test_endpoint(method, endpoint, data=None, params=None):
    """Test an API endpoint and return the response."""
    url = f"{BASE_URL}{endpoint}"
    
    print(f"\n{'='*50}")
    print(f"{method} {url}")
    if params:
        print(f"Params: {params}")
    if data:
        print(f"Data: {json.dumps(data, indent=2)}")
    print(f"{'='*50}")
    
    try:
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, json=data, params=params)
        elif method == "DELETE":
            response = requests.delete(url)
        else:
            print(f"Unsupported method: {method}")
            return None
        
        print(f"Status Code: {response.status_code}")
        
        try:
            response_data = response.json()
            print(f"Response: {json.dumps(response_data, indent=2)}")
        except:
            print(f"Response Text: {response.text}")
        
        return response
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Is the Flask server running on port 5000?")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("🧪 Testing New Normalized Playlist API")
    print("Make sure Flask server is running on localhost:5000")
    
    # Test basic connectivity
    print("\n🔍 Testing basic connectivity...")
    test_endpoint("GET", "/test")
    
    # Test getting all playlists
    print("\n🎵 Testing GET /playlists...")
    test_endpoint("GET", "/playlists")
    
    # Test Spotify search (requires SPOTIPY environment variables)
    print("\n🔍 Testing Spotify search...")
    test_endpoint("GET", "/search", params={"q": "Bohemian Rhapsody", "type": "track", "limit": 3})
    
    # Test creating a new playlist
    print("\n✨ Testing POST /playlists (create playlist)...")
    new_playlist_data = {
        "name": "Test Playlist - API Migration",
        "description": "Testing the new normalized API",
        "posting_dj_id": 1,
        "hidden": False
    }
    response = test_endpoint("POST", "/playlists", data=new_playlist_data)
    
    if response and response.status_code == 201:
        playlist_id = response.json().get('id')
        print(f"✅ Created playlist with ID: {playlist_id}")
        
        # Test getting specific playlist
        print(f"\n🎵 Testing GET /playlists/{playlist_id}...")
        test_endpoint("GET", f"/playlists/{playlist_id}")
        
        # Test adding a track to playlist (requires a valid Spotify track ID)
        print(f"\n🎵 Testing POST /playlists/{playlist_id}/tracks (add track)...")
        track_data = {
            "spotify_track_id": "0JTNUQOww8LhZvSnP47Ny",  # A valid Spotify track ID
            "track_order": 1
        }
        test_endpoint("POST", f"/playlists/{playlist_id}/tracks", data=track_data)
        
        # Test getting playlist with tracks
        print(f"\n🎵 Testing GET /playlists/{playlist_id} (with tracks)...")
        test_endpoint("GET", f"/playlists/{playlist_id}")
        
        # Test getting tracks for playlist
        print(f"\n🎵 Testing GET /playlists/{playlist_id}/tracks...")
        test_endpoint("GET", f"/playlists/{playlist_id}/tracks")
        
    else:
        print("❌ Failed to create test playlist")

if __name__ == "__main__":
    main()