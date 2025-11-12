USE `kwip`;

-- ==========================================
-- STEP 3: Data Migration from Old to New Schema
-- ==========================================

-- Migrate DJ data (simplified mapping from old DJ table)
INSERT INTO `DJ` (`id`, `dj_name`)
SELECT `id`, `dj_name` 
FROM `DJ_Old`
WHERE `dj_name` IS NOT NULL AND `dj_name` != '';

-- Migrate Playlists (map old structure to new)
INSERT INTO `Playlist` (`id`, `name`, `description`, `date_created`, `spotify_playlist_id`, `posting_dj_id`, `hidden`)
SELECT 
    `id`, 
    COALESCE(`name`, CONCAT('Playlist ', `id`)) as `name`,
    `description`,
    `date_played` as `date_created`,
    `spotify_playlist_id`,
    COALESCE(`posting_dj_id`, 1) as `posting_dj_id`,  -- Default to DJ 1 if NULL
    `hidden`
FROM `Playlist_Old`;

-- Populate Artists (get unique artists from old playlist_track data)
INSERT INTO `Artist` (`name`)
SELECT DISTINCT `artist` 
FROM `Playlist_Track_Old`
WHERE `artist` IS NOT NULL 
AND `artist` != '' 
AND `artist` NOT IN (SELECT `name` FROM `Artist`);

-- Populate Albums (link to artists)
INSERT INTO `Album` (`name`, `artist_id`)
SELECT DISTINCT 
    pto.`album`, 
    a.`id` 
FROM `Playlist_Track_Old` pto
JOIN `Artist` a ON pto.`artist` = a.`name`
WHERE pto.`album` IS NOT NULL 
AND pto.`album` != ''
AND NOT EXISTS (
    SELECT 1 FROM `Album` al 
    WHERE al.`name` = pto.`album` AND al.`artist_id` = a.`id`
);

-- Populate Tracks (create legacy spotify_track_id for migration)
INSERT INTO `Track` (`title`, `artist_id`, `album_id`, `spotify_track_id`)
SELECT DISTINCT 
    pto.`song`,
    a.`id` as `artist_id`,
    al.`id` as `album_id`,
    CONCAT('legacy_', pto.`playlist_id`, '_', pto.`track`, '_', UNIX_TIMESTAMP()) as `spotify_track_id`
FROM `Playlist_Track_Old` pto
JOIN `Artist` a ON pto.`artist` = a.`name`
LEFT JOIN `Album` al ON pto.`album` = al.`name` AND al.`artist_id` = a.`id`
WHERE pto.`song` IS NOT NULL 
AND pto.`song` != ''
AND NOT EXISTS (
    SELECT 1 FROM `Track` t 
    WHERE t.`title` = pto.`song` 
    AND t.`artist_id` = a.`id` 
    AND (t.`album_id` = al.`id` OR (t.`album_id` IS NULL AND al.`id` IS NULL))
);

-- Populate the new Playlist_Track join table
INSERT INTO `Playlist_Track` (`playlist_id`, `track_id`, `track_order`)
SELECT
    pto.`playlist_id`,
    t.`id` as `track_id`,
    pto.`track` as `track_order`
FROM `Playlist_Track_Old` pto
JOIN `Track` t ON pto.`song` = t.`title`
JOIN `Artist` a ON pto.`artist` = a.`name` AND t.`artist_id` = a.`id`
LEFT JOIN `Album` al ON pto.`album` = al.`name` AND t.`album_id` = al.`id`
WHERE NOT EXISTS (
    SELECT 1 FROM `Playlist_Track` pt 
    WHERE pt.`playlist_id` = pto.`playlist_id` 
    AND pt.`track_order` = pto.`track`
);

-- Verification queries - show counts for comparison
SELECT 'Migration Summary' as info;
SELECT 'DJs' as table_name, COUNT(*) as old_count FROM `DJ_Old`
UNION ALL
SELECT 'DJs_New', COUNT(*) FROM `DJ`
UNION ALL
SELECT 'Playlists' as table_name, COUNT(*) FROM `Playlist_Old`
UNION ALL
SELECT 'Playlists_New', COUNT(*) FROM `Playlist`
UNION ALL
SELECT 'Playlist_Tracks', COUNT(*) FROM `Playlist_Track_Old`
UNION ALL
SELECT 'Playlist_Tracks_New', COUNT(*) FROM `Playlist_Track`
UNION ALL
SELECT 'Artists_New', COUNT(*) FROM `Artist`
UNION ALL
SELECT 'Albums_New', COUNT(*) FROM `Album`
UNION ALL
SELECT 'Tracks_New', COUNT(*) FROM `Track`;

SELECT 'Migration completed successfully!' as status;