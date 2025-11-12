USE `kwip`;

-- ==========================================
-- CORRECTED MIGRATION: Handle existing lowercase table names
-- ==========================================

-- Step 1: Create backup tables with different names to avoid conflicts
CREATE TABLE `playlist_backup` LIKE `playlist`;
INSERT INTO `playlist_backup` SELECT * FROM `playlist`;

CREATE TABLE `playlist_track_backup` LIKE `playlist_track`;
INSERT INTO `playlist_track_backup` SELECT * FROM `playlist_track`;

CREATE TABLE `dj_backup` LIKE `dj`;
INSERT INTO `dj_backup` SELECT * FROM `dj`;

-- Step 2: Drop original tables to make room for new normalized schema
DROP TABLE IF EXISTS `playlist_track`;
DROP TABLE IF EXISTS `playlist`;

-- Step 3: Create new normalized schema (capitalized table names)
-- DJ table (simplified from existing dj structure)
CREATE TABLE `DJ` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `dj_name` VARCHAR(255) NOT NULL UNIQUE
);

-- Artists table - stores each artist ONCE
CREATE TABLE `Artist` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `spotify_artist_id` VARCHAR(255) UNIQUE,
    UNIQUE(`name`)
);

-- Albums table - stores each album ONCE
CREATE TABLE `Album` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `artist_id` INT NOT NULL,
    `spotify_album_id` VARCHAR(255) UNIQUE,
    FOREIGN KEY (`artist_id`) REFERENCES `Artist`(`id`),
    INDEX `idx_artist_id` (`artist_id`),
    INDEX `idx_spotify_album_id` (`spotify_album_id`)
);

-- Tracks table - stores each track ONCE
CREATE TABLE `Track` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(255) NOT NULL,
    `artist_id` INT NOT NULL,
    `album_id` INT,
    `spotify_track_id` VARCHAR(255) UNIQUE NOT NULL,
    FOREIGN KEY (`artist_id`) REFERENCES `Artist`(`id`),
    FOREIGN KEY (`album_id`) REFERENCES `Album`(`id`),
    INDEX `idx_artist_id` (`artist_id`),
    INDEX `idx_album_id` (`album_id`),
    INDEX `idx_spotify_track_id` (`spotify_track_id`)
);

-- Playlist table (header information)
CREATE TABLE `Playlist` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `date_created` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `date_updated` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `spotify_playlist_id` VARCHAR(255),
    `posting_dj_id` INT NOT NULL,
    `hidden` BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (`posting_dj_id`) REFERENCES `DJ`(`id`),
    INDEX `idx_posting_dj_id` (`posting_dj_id`),
    INDEX `idx_spotify_playlist_id` (`spotify_playlist_id`),
    INDEX `idx_date_created` (`date_created`)
);

-- The magic join table - links playlists to tracks
CREATE TABLE `Playlist_Track` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `playlist_id` INT NOT NULL,
    `track_id` INT NOT NULL,
    `track_order` INT NOT NULL,
    `date_added` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`playlist_id`) REFERENCES `Playlist`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`track_id`) REFERENCES `Track`(`id`),
    UNIQUE(`playlist_id`, `track_order`),
    INDEX `idx_playlist_id` (`playlist_id`),
    INDEX `idx_track_id` (`track_id`),
    INDEX `idx_track_order` (`track_order`)
);

-- Step 4: Migrate DJ data
INSERT INTO `DJ` (`id`, `dj_name`)
SELECT `id`, `dj_name` 
FROM `dj_backup`
WHERE `dj_name` IS NOT NULL AND `dj_name` != '';

-- Step 5: Migrate Playlists
INSERT INTO `Playlist` (`id`, `name`, `description`, `date_created`, `spotify_playlist_id`, `posting_dj_id`, `hidden`)
SELECT 
    `id`, 
    COALESCE(`name`, CONCAT('Playlist ', `id`)) as `name`,
    `description`,
    `date_played` as `date_created`,
    NULL as `spotify_playlist_id`,  -- spotify_playlist_id doesn't exist in old schema
    COALESCE(`posting_dj_id`, 1) as `posting_dj_id`,
    `hidden`
FROM `playlist_backup`;

-- Step 6: Populate Artists
INSERT INTO `Artist` (`name`)
SELECT DISTINCT `artist` 
FROM `playlist_track_backup`
WHERE `artist` IS NOT NULL 
AND `artist` != '';

-- Step 7: Populate Albums
INSERT INTO `Album` (`name`, `artist_id`)
SELECT DISTINCT 
    ptb.`album`, 
    a.`id` 
FROM `playlist_track_backup` ptb
JOIN `Artist` a ON ptb.`artist` = a.`name`
WHERE ptb.`album` IS NOT NULL 
AND ptb.`album` != '';

-- Step 8: Populate Tracks
INSERT INTO `Track` (`title`, `artist_id`, `album_id`, `spotify_track_id`)
SELECT DISTINCT 
    ptb.`song`,
    a.`id` as `artist_id`,
    al.`id` as `album_id`,
    CONCAT('legacy_', ptb.`playlist_id`, '_', ptb.`track`, '_', UNIX_TIMESTAMP(), '_', a.`id`) as `spotify_track_id`
FROM `playlist_track_backup` ptb
JOIN `Artist` a ON ptb.`artist` = a.`name`
LEFT JOIN `Album` al ON ptb.`album` = al.`name` AND al.`artist_id` = a.`id`
WHERE ptb.`song` IS NOT NULL 
AND ptb.`song` != '';

-- Step 9: Populate the new Playlist_Track join table
INSERT INTO `Playlist_Track` (`playlist_id`, `track_id`, `track_order`)
SELECT
    ptb.`playlist_id`,
    t.`id` as `track_id`,
    ptb.`track` as `track_order`
FROM `playlist_track_backup` ptb
JOIN `Track` t ON ptb.`song` = t.`title`
JOIN `Artist` a ON ptb.`artist` = a.`name` AND t.`artist_id` = a.`id`
LEFT JOIN `Album` al ON ptb.`album` = al.`name` AND t.`album_id` = al.`id`;

-- Verification query
SELECT 'Migration Summary' as info;
SELECT 'Original DJs' as table_name, COUNT(*) as count FROM `dj_backup`
UNION ALL
SELECT 'Migrated DJs', COUNT(*) FROM `DJ`
UNION ALL
SELECT 'Original Playlists', COUNT(*) FROM `playlist_backup`
UNION ALL
SELECT 'Migrated Playlists', COUNT(*) FROM `Playlist`
UNION ALL
SELECT 'Original Tracks', COUNT(*) FROM `playlist_track_backup`
UNION ALL
SELECT 'Migrated Playlist_Tracks', COUNT(*) FROM `Playlist_Track`
UNION ALL
SELECT 'New Artists', COUNT(*) FROM `Artist`
UNION ALL
SELECT 'New Albums', COUNT(*) FROM `Album`
UNION ALL
SELECT 'New Tracks', COUNT(*) FROM `Track`;

SELECT 'Migration completed successfully!' as status;