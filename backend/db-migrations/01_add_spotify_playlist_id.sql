USE `kwip`;

-- Add Spotify playlist ID column to playlist table
ALTER TABLE `playlist` 
ADD COLUMN `spotify_playlist_id` VARCHAR(50) NULL COMMENT 'Spotify playlist ID when published to Spotify';

-- Add index for better query performance
CREATE INDEX `idx_spotify_playlist_id` ON `playlist` (`spotify_playlist_id`);