USE `kwip`;

-- ==========================================
-- STEP 1: Backup and rename existing tables
-- ==========================================
-- Drop any existing backup tables first
DROP TABLE IF EXISTS `Playlist_Old`;
DROP TABLE IF EXISTS `Playlist_Track_Old`;
DROP TABLE IF EXISTS `DJ_Old`;

-- Rename existing tables to _Old for backup
ALTER TABLE `playlist` RENAME TO `Playlist_Old`;
ALTER TABLE `playlist_track` RENAME TO `Playlist_Track_Old`;
ALTER TABLE `dj` RENAME TO `DJ_Old`;

-- ==========================================
-- STEP 2: Create new normalized schema
-- ==========================================

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

-- Add some useful indexes for performance
CREATE INDEX `idx_artist_name` ON `Artist`(`name`);
CREATE INDEX `idx_album_name` ON `Album`(`name`);
CREATE INDEX `idx_track_title` ON `Track`(`title`);