#!/usr/bin/env python3

import requests
import json
from database_helper import get_db_cursor

def validate_database_schema():
    """Validate the new normalized database schema"""
    print("🔍 Validating Database Schema...")
    
    try:
        conn, cursor = get_db_cursor()
        
        # Check all required tables exist
        expected_tables = ['DJ', 'Artist', 'Album', 'Track', 'Playlist', 'Playlist_Track']
        
        cursor.execute("SHOW TABLES")
        tables = [list(row.values())[0] for row in cursor.fetchall()]
        
        missing_tables = [table for table in expected_tables if table not in tables]
        if missing_tables:
            print(f"❌ Missing tables: {missing_tables}")
            return False
        else:
            print(f"✅ All required tables exist: {expected_tables}")
        
        # Check foreign key relationships
        print("\n🔗 Validating Foreign Key Relationships...")
        
        # Test Album -> Artist relationship
        cursor.execute("""
            SELECT a.name as album, ar.name as artist 
            FROM Album a 
            JOIN Artist ar ON a.artist_id = ar.id 
            LIMIT 3
        """)
        album_artists = cursor.fetchall()
        print(f"✅ Album-Artist relationships: {len(album_artists)} found")
        for row in album_artists:
            print(f"   - {row['album']} by {row['artist']}")
        
        # Test Track relationships
        cursor.execute("""
            SELECT t.title, ar.name as artist, al.name as album 
            FROM Track t 
            JOIN Artist ar ON t.artist_id = ar.id 
            LEFT JOIN Album al ON t.album_id = al.id 
            LIMIT 3
        """)
        tracks = cursor.fetchall()
        print(f"✅ Track relationships: {len(tracks)} found")
        for row in tracks:
            album = row['album'] if row['album'] else 'No Album'
            print(f"   - {row['title']} by {row['artist']} ({album})")
        
        # Test Playlist-Track relationships
        cursor.execute("""
            SELECT p.name as playlist, t.title as track, pt.track_order 
            FROM Playlist_Track pt
            JOIN Playlist p ON pt.playlist_id = p.id
            JOIN Track t ON pt.track_id = t.id
            ORDER BY p.id, pt.track_order
            LIMIT 5
        """)
        playlist_tracks = cursor.fetchall()
        print(f"✅ Playlist-Track relationships: {len(playlist_tracks)} found")
        for row in playlist_tracks:
            print(f"   - {row['playlist']}: #{row['track_order']} {row['track']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database validation failed: {e}")
        return False
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

def validate_api_endpoints():
    """Validate all API endpoints are working"""
    print("\n🌐 Validating API Endpoints...")
    
    BASE_URL = "http://localhost:5001"
    
    # Test basic connectivity
    try:
        response = requests.get(f"{BASE_URL}/test")
        if response.status_code != 200:
            print(f"❌ Basic connectivity failed: {response.status_code}")
            return False
        print("✅ Basic connectivity working")
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        return False
    
    # Test GET /playlists
    try:
        response = requests.get(f"{BASE_URL}/playlists")
        if response.status_code != 200:
            print(f"❌ GET /playlists failed: {response.status_code}")
            return False
        playlists = response.json()
        print(f"✅ GET /playlists: {len(playlists)} playlists found")
    except Exception as e:
        print(f"❌ GET /playlists error: {e}")
        return False
    
    # Test GET /playlists/{id}
    if playlists:
        playlist_id = playlists[0]['id']
        try:
            response = requests.get(f"{BASE_URL}/playlists/{playlist_id}")
            if response.status_code != 200:
                print(f"❌ GET /playlists/{playlist_id} failed: {response.status_code}")
                return False
            playlist = response.json()
            track_count = len(playlist.get('tracks', []))
            print(f"✅ GET /playlists/{playlist_id}: '{playlist['name']}' with {track_count} tracks")
        except Exception as e:
            print(f"❌ GET /playlists/{playlist_id} error: {e}")
            return False
    
    # Test GET /playlists/{id}/tracks
    if playlists:
        playlist_id = playlists[0]['id']
        try:
            response = requests.get(f"{BASE_URL}/playlists/{playlist_id}/tracks")
            if response.status_code != 200:
                print(f"❌ GET /playlists/{playlist_id}/tracks failed: {response.status_code}")
                return False
            tracks = response.json()
            print(f"✅ GET /playlists/{playlist_id}/tracks: {len(tracks)} tracks")
        except Exception as e:
            print(f"❌ GET /playlists/{playlist_id}/tracks error: {e}")
            return False
    
    # Test POST /playlists (create)
    try:
        test_playlist = {
            "name": "Validation Test Playlist",
            "description": "Testing playlist creation",
            "posting_dj_id": 1,
            "hidden": False
        }
        response = requests.post(f"{BASE_URL}/playlists", json=test_playlist)
        if response.status_code != 201:
            print(f"❌ POST /playlists failed: {response.status_code}")
            return False
        new_playlist = response.json()
        print(f"✅ POST /playlists: Created '{new_playlist['name']}'")
        
        # Clean up - delete the test playlist would go here if we had DELETE endpoint
        
    except Exception as e:
        print(f"❌ POST /playlists error: {e}")
        return False
    
    return True

def validate_data_integrity():
    """Validate data integrity and consistency"""
    print("\n📊 Validating Data Integrity...")
    
    try:
        conn, cursor = get_db_cursor()
        
        # Check for orphaned records
        cursor.execute("""
            SELECT COUNT(*) as count FROM Album a
            LEFT JOIN Artist ar ON a.artist_id = ar.id
            WHERE ar.id IS NULL
        """)
        orphaned_albums = cursor.fetchone()['count']
        
        cursor.execute("""
            SELECT COUNT(*) as count FROM Track t
            LEFT JOIN Artist ar ON t.artist_id = ar.id
            WHERE ar.id IS NULL
        """)
        orphaned_tracks = cursor.fetchone()['count']
        
        cursor.execute("""
            SELECT COUNT(*) as count FROM Playlist_Track pt
            LEFT JOIN Playlist p ON pt.playlist_id = p.id
            LEFT JOIN Track t ON pt.track_id = t.id
            WHERE p.id IS NULL OR t.id IS NULL
        """)
        orphaned_playlist_tracks = cursor.fetchone()['count']
        
        if orphaned_albums > 0:
            print(f"❌ Found {orphaned_albums} orphaned albums")
            return False
        if orphaned_tracks > 0:
            print(f"❌ Found {orphaned_tracks} orphaned tracks")
            return False
        if orphaned_playlist_tracks > 0:
            print(f"❌ Found {orphaned_playlist_tracks} orphaned playlist tracks")
            return False
        
        print("✅ No orphaned records found")
        
        # Check for duplicate spotify_track_ids
        cursor.execute("""
            SELECT spotify_track_id, COUNT(*) as count 
            FROM Track 
            GROUP BY spotify_track_id 
            HAVING COUNT(*) > 1
        """)
        duplicates = cursor.fetchall()
        if duplicates:
            print(f"❌ Found {len(duplicates)} duplicate Spotify track IDs")
            return False
        print("✅ No duplicate Spotify track IDs found")
        
        return True
        
    except Exception as e:
        print(f"❌ Data integrity validation failed: {e}")
        return False
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

def main():
    """Run all validation tests"""
    print("🧪 COMPREHENSIVE MIGRATION VALIDATION")
    print("=" * 50)
    
    tests = [
        ("Database Schema", validate_database_schema),
        ("API Endpoints", validate_api_endpoints),
        ("Data Integrity", validate_data_integrity)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("VALIDATION SUMMARY:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Migration is successful!")
        print("🚀 The new normalized database with Spotify integration is ready!")
    else:
        print("❌ SOME TESTS FAILED! Please check the errors above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)