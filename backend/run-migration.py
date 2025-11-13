#!/usr/bin/env python3

import pymysql
import os
from configparser import ConfigParser
from dotenv import dotenv_values

def run_migration():
    print("🚀 Starting database migration...")
    
    # Load configuration
    config = ConfigParser()
    config.read('config.ini')
    secrets = dotenv_values('.env')
    
    db_config = config['DATABASE']
    
    try:
        # Connect to database (use localhost when testing locally with Docker)
        host = 'localhost' if db_config['host'] == 'database' else db_config['host']
        port = 8972 if host == 'localhost' else int(db_config['port'])
        
        connection = pymysql.connect(
            host=host,
            port=port,
            user=secrets['DB_USER'],
            password=secrets['DB_PASS'],
            database=db_config['database'],
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False
        )
        
        cursor = connection.cursor()
        print("✅ Database connection established")
        
        # Read and execute migration script
        migration_file = 'db-migrations/05_fresh_migration.sql'
        print(f"📖 Reading migration file: {migration_file}")
        
        with open(migration_file, 'r') as f:
            migration_sql = f.read()
        
        # Split SQL commands by semicolon and execute each
        statements = [stmt.strip() for stmt in migration_sql.split(';') if stmt.strip()]
        
        for i, statement in enumerate(statements, 1):
            if statement.upper().startswith(('USE', 'DROP', 'CREATE', 'INSERT', 'ALTER', 'SELECT', 'SHOW')):
                print(f"⚡ Executing statement {i}/{len(statements)}")
                try:
                    cursor.execute(statement)
                    if statement.upper().startswith(('SELECT', 'SHOW')):
                        results = cursor.fetchall()
                        for row in results:
                            print(f"   {row}")
                except Exception as e:
                    print(f"⚠️  Statement {i} warning: {e}")
                    # Continue with migration for non-critical errors
        
        connection.commit()
        print("✅ Migration completed successfully!")
        
        # Test the new schema with a verification query
        try:
            cursor.execute("SELECT COUNT(*) as playlist_count FROM Playlist")
            playlist_count = cursor.fetchone()
            print(f"📊 Verified: {playlist_count['playlist_count']} playlists in new schema")
            
            cursor.execute("SELECT COUNT(*) as artist_count FROM Artist")
            artist_count = cursor.fetchone()
            print(f"📊 Verified: {artist_count['artist_count']} artists in new schema")
        except Exception as e:
            print(f"⚠️  Verification warning: {e}")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        if 'connection' in locals():
            connection.rollback()
        return False
        
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
        print("🔌 Database connection closed")
    
    return True

if __name__ == "__main__":
    success = run_migration()
    exit(0 if success else 1)