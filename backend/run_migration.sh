#!/bin/bash

# Database Migration Script for Spotify-Powered Playlists
echo "🎵 Starting database migration to Spotify-powered playlists..."

# Check if MySQL is running
if ! mysql --version > /dev/null 2>&1; then
    echo "❌ MySQL not found. Please install MySQL and try again."
    exit 1
fi

# Set up environment variables if not already set
if [ -z "$SPOTIPY_CLIENT_ID" ] || [ -z "$SPOTIPY_CLIENT_SECRET" ]; then
    echo "⚠️  Warning: SPOTIPY_CLIENT_ID and/or SPOTIPY_CLIENT_SECRET not set"
    echo "   Set these environment variables for full Spotify functionality"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "❌ requirements.txt not found"
    exit 1
fi

# Database connection parameters
DB_USER=${DB_USER:-kwip}
DB_PASS=${DB_PASS:-kwip-password}
DB_HOST=${DB_HOST:-localhost}
DB_NAME=${DB_NAME:-kwip}

echo "🔄 Running database migrations..."

# Step 1: Create normalized schema and backup old tables
echo "Step 1: Creating new normalized schema..."
mysql -u"$DB_USER" -p"$DB_PASS" -h"$DB_HOST" < db-migrations/02_normalized_schema.sql

if [ $? -eq 0 ]; then
    echo "✅ New schema created successfully"
else
    echo "❌ Failed to create new schema"
    exit 1
fi

# Step 2: Migrate data
echo "Step 2: Migrating existing data..."
mysql -u"$DB_USER" -p"$DB_PASS" -h"$DB_HOST" < db-migrations/03_data_migration.sql

if [ $? -eq 0 ]; then
    echo "✅ Data migration completed successfully"
else
    echo "❌ Failed to migrate data"
    exit 1
fi

echo "🎉 Database migration completed!"
echo ""
echo "Summary:"
echo "- ✅ Old tables backed up as Playlist_Old, Playlist_Track_Old, DJ_Old"
echo "- ✅ New normalized schema created with Spotify integration"
echo "- ✅ Existing data migrated to new structure"
echo ""
echo "Next steps:"
echo "1. Set SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET environment variables"
echo "2. Run the new API: python spotify_playlist_api.py"
echo "3. Test with: curl http://localhost:5001/status"

echo ""
echo "🔍 Running verification query..."
mysql -u"$DB_USER" -p"$DB_PASS" -h"$DB_HOST" -D"$DB_NAME" -e "
SELECT 'Verification Results' as info;
SELECT 'DJs' as table_name, COUNT(*) as count FROM DJ
UNION ALL
SELECT 'Artists', COUNT(*) FROM Artist  
UNION ALL
SELECT 'Albums', COUNT(*) FROM Album
UNION ALL
SELECT 'Tracks', COUNT(*) FROM Track
UNION ALL
SELECT 'Playlists', COUNT(*) FROM Playlist
UNION ALL
SELECT 'Playlist_Tracks', COUNT(*) FROM Playlist_Track;
"