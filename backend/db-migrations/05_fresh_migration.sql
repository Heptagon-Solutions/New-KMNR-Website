USE `kwip`;

-- ==========================================
-- FRESH MIGRATION: Create new normalized schema
-- ==========================================

-- First, let's check what tables exist
SHOW TABLES;

-- Create normalized schema from scratch

-- DJ table
CREATE TABLE IF NOT EXISTS `DJ` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `dj_name` VARCHAR(255) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Artists table - stores each artist ONCE
CREATE TABLE IF NOT EXISTS `Artist` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `spotify_artist_id` VARCHAR(255) UNIQUE,
    UNIQUE(`name`),
    INDEX `idx_name` (`name`),
    INDEX `idx_spotify_artist_id` (`spotify_artist_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Albums table - stores each album ONCE
CREATE TABLE IF NOT EXISTS `Album` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `artist_id` INT NOT NULL,
    `spotify_album_id` VARCHAR(255) UNIQUE,
    FOREIGN KEY (`artist_id`) REFERENCES `Artist`(`id`) ON DELETE CASCADE,
    INDEX `idx_artist_id` (`artist_id`),
    INDEX `idx_spotify_album_id` (`spotify_album_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tracks table - stores each track ONCE
CREATE TABLE IF NOT EXISTS `Track` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(255) NOT NULL,
    `artist_id` INT NOT NULL,
    `album_id` INT,
    `spotify_track_id` VARCHAR(255) UNIQUE NOT NULL,
    FOREIGN KEY (`artist_id`) REFERENCES `Artist`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`album_id`) REFERENCES `Album`(`id`) ON DELETE SET NULL,
    INDEX `idx_artist_id` (`artist_id`),
    INDEX `idx_album_id` (`album_id`),
    INDEX `idx_spotify_track_id` (`spotify_track_id`),
    INDEX `idx_title` (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Playlist table (header information)
CREATE TABLE IF NOT EXISTS `Playlist` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `date_created` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `date_updated` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `spotify_playlist_id` VARCHAR(255),
    `posting_dj_id` INT NOT NULL,
    `hidden` BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (`posting_dj_id`) REFERENCES `DJ`(`id`) ON DELETE CASCADE,
    INDEX `idx_posting_dj_id` (`posting_dj_id`),
    INDEX `idx_spotify_playlist_id` (`spotify_playlist_id`),
    INDEX `idx_date_created` (`date_created`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- The magic join table - links playlists to tracks
CREATE TABLE IF NOT EXISTS `Playlist_Track` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `playlist_id` INT NOT NULL,
    `track_id` INT NOT NULL,
    `track_order` INT NOT NULL,
    `date_added` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`playlist_id`) REFERENCES `Playlist`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`track_id`) REFERENCES `Track`(`id`) ON DELETE CASCADE,
    UNIQUE(`playlist_id`, `track_order`),
    INDEX `idx_playlist_id` (`playlist_id`),
    INDEX `idx_track_id` (`track_id`),
    INDEX `idx_track_order` (`track_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert sample data for testing

-- Sample DJ
INSERT IGNORE INTO `DJ` (`id`, `dj_name`) VALUES (1, 'Test DJ');

-- Sample data migration if old tables exist
INSERT IGNORE INTO `DJ` (`dj_name`)
SELECT DISTINCT COALESCE(`dj_name`, CONCAT('DJ_', `id`)) 
FROM `dj` 
WHERE EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'kwip' AND table_name = 'dj')
AND `dj_name` IS NOT NULL 
AND `dj_name` != '';

INSERT IGNORE INTO `Artist` (`name`)
SELECT DISTINCT `artist` 
FROM `playlist_track` 
WHERE EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'kwip' AND table_name = 'playlist_track')
AND `artist` IS NOT NULL 
AND `artist` != '';

INSERT IGNORE INTO `Album` (`name`, `artist_id`)
SELECT DISTINCT 
    pt.`album`, 
    a.`id` 
FROM `playlist_track` pt
JOIN `Artist` a ON pt.`artist` = a.`name`
WHERE EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'kwip' AND table_name = 'playlist_track')
AND pt.`album` IS NOT NULL 
AND pt.`album` != '';

INSERT IGNORE INTO `Track` (`title`, `artist_id`, `album_id`, `spotify_track_id`)
SELECT DISTINCT 
    pt.`song`,
    a.`id` as `artist_id`,
    al.`id` as `album_id`,
    CONCAT('legacy_', pt.`playlist_id`, '_', pt.`track`, '_', UNIX_TIMESTAMP(), '_', a.`id`) as `spotify_track_id`
FROM `playlist_track` pt
JOIN `Artist` a ON pt.`artist` = a.`name`
LEFT JOIN `Album` al ON pt.`album` = al.`name` AND al.`artist_id` = a.`id`
WHERE EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'kwip' AND table_name = 'playlist_track')
AND pt.`song` IS NOT NULL 
AND pt.`song` != '';

INSERT IGNORE INTO `Playlist` (`name`, `description`, `date_created`, `posting_dj_id`, `hidden`)
SELECT 
    COALESCE(p.`name`, CONCAT('Playlist ', p.`id`)) as `name`,
    p.`description`,
    COALESCE(p.`date_played`, NOW()) as `date_created`,
    COALESCE(p.`posting_dj_id`, 1) as `posting_dj_id`,
    COALESCE(p.`hidden`, 0) as `hidden`
FROM `playlist` p
WHERE EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'kwip' AND table_name = 'playlist');

INSERT IGNORE INTO `Playlist_Track` (`playlist_id`, `track_id`, `track_order`)
SELECT
    pt.`playlist_id`,
    t.`id` as `track_id`,
    pt.`track` as `track_order`
FROM `playlist_track` pt
JOIN `Track` t ON pt.`song` = t.`title`
JOIN `Artist` a ON pt.`artist` = a.`name` AND t.`artist_id` = a.`id`
WHERE EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'kwip' AND table_name = 'playlist_track')
AND EXISTS (SELECT 1 FROM `Playlist` p WHERE p.id = pt.playlist_id);

-- Show final counts
SELECT 'New Schema Summary' as info;
SELECT 'DJs' as table_name, COUNT(*) as count FROM `DJ`
UNION ALL
SELECT 'Artists', COUNT(*) FROM `Artist`
UNION ALL
SELECT 'Albums', COUNT(*) FROM `Album`
UNION ALL
SELECT 'Tracks', COUNT(*) FROM `Track`
UNION ALL
SELECT 'Playlists', COUNT(*) FROM `Playlist`
UNION ALL
SELECT 'Playlist_Tracks', COUNT(*) FROM `Playlist_Track`;

SELECT 'Fresh migration completed successfully!' as status;