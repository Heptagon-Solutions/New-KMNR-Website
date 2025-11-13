#!/usr/bin/env python3

from database_helper import get_db_cursor

def migrate_data():
    """Migrate data from old tables to new normalized schema"""
    try:
        conn, cursor = get_db_cursor()
        print('🚀 Migrating data from old tables...')
        
        # Migrate DJs
        print('Migrating DJs...')
        cursor.execute("""INSERT IGNORE INTO DJ (dj_name)
            SELECT DISTINCT COALESCE(dj_name, CONCAT('DJ_', id)) 
            FROM dj_old 
            WHERE dj_name IS NOT NULL AND dj_name != ''""")
        print(f'  - Inserted {cursor.rowcount} DJs')
        
        # Add default DJ if none exist
        cursor.execute("INSERT IGNORE INTO DJ (id, dj_name) VALUES (1, 'Test DJ')")
        
        # Migrate Artists
        print('Migrating Artists...')
        cursor.execute("""INSERT IGNORE INTO Artist (name)
            SELECT DISTINCT artist 
            FROM playlist_track_old
            WHERE artist IS NOT NULL AND artist != ''""")
        print(f'  - Inserted {cursor.rowcount} Artists')
        
        # Migrate Albums
        print('Migrating Albums...')
        cursor.execute("""INSERT IGNORE INTO Album (name, artist_id)
            SELECT DISTINCT pt.album, a.id 
            FROM playlist_track_old pt
            JOIN Artist a ON pt.artist = a.name
            WHERE pt.album IS NOT NULL AND pt.album != ''""")
        print(f'  - Inserted {cursor.rowcount} Albums')
        
        # Migrate Tracks
        print('Migrating Tracks...')
        cursor.execute("""INSERT IGNORE INTO Track (title, artist_id, album_id, spotify_track_id)
            SELECT DISTINCT 
                pt.song,
                a.id as artist_id,
                al.id as album_id,
                CONCAT('legacy_', pt.playlist_id, '_', pt.track, '_', UNIX_TIMESTAMP(), '_', a.id) as spotify_track_id
            FROM playlist_track_old pt
            JOIN Artist a ON pt.artist = a.name
            LEFT JOIN Album al ON pt.album = al.name AND al.artist_id = a.id
            WHERE pt.song IS NOT NULL AND pt.song != ''""")
        print(f'  - Inserted {cursor.rowcount} Tracks')
        
        # Migrate Playlists
        print('Migrating Playlists...')
        cursor.execute("""INSERT IGNORE INTO Playlist (name, description, date_created, posting_dj_id, hidden)
            SELECT 
                COALESCE(p.name, CONCAT('Playlist ', p.id)) as name,
                p.description,
                COALESCE(p.date_played, NOW()) as date_created,
                COALESCE(p.posting_dj_id, 1) as posting_dj_id,
                COALESCE(p.hidden, 0) as hidden
            FROM playlist_old p""")
        print(f'  - Inserted {cursor.rowcount} Playlists')
        
        # Migrate Playlist Tracks
        print('Migrating Playlist Tracks...')
        cursor.execute("""INSERT IGNORE INTO Playlist_Track (playlist_id, track_id, track_order)
            SELECT DISTINCT
                pt.playlist_id,
                t.id as track_id,
                pt.track as track_order
            FROM playlist_track_old pt
            JOIN Track t ON pt.song = t.title
            JOIN Artist a ON pt.artist = a.name AND t.artist_id = a.id
            WHERE EXISTS (SELECT 1 FROM Playlist p WHERE p.id = pt.playlist_id)""")
        print(f'  - Inserted {cursor.rowcount} Playlist Tracks')
        
        conn.commit()
        print('✅ Data migration completed')
        
        # Show counts
        print('\n📊 Final counts:')
        for table in ['DJ', 'Artist', 'Album', 'Track', 'Playlist', 'Playlist_Track']:
            cursor.execute(f'SELECT COUNT(*) as count FROM {table}')
            count = cursor.fetchone()['count']
            print(f'  - {table}: {count}')
        
        return True
        
    except Exception as e:
        print(f'❌ Migration failed: {e}')
        if conn: conn.rollback()
        return False
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    success = migrate_data()
    exit(0 if success else 1)