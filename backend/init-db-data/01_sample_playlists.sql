USE `kwip`;

-- Insert sample data for testing playlist functionality

-- Sample DJ data
INSERT INTO `semester` (`semester`, `year`) VALUES 
('Fall', 2024),
('Spring', 2025);

INSERT INTO `user` (`name`, `email`, `password`, `role`) VALUES 
('DJ Test', 'dj.test@kmnr.org', 'password123', 'dj'),
('DJ Admin', 'dj.admin@kmnr.org', 'password123', 'admin');

INSERT INTO `dj` (`id`, `dj_name`, `training_semester_id`, `trainer_dj_id`, `graduating_semester_id`, `profile_desc`) VALUES 
(1, 'DJ Test', 1, NULL, NULL, 'Test DJ for playlist functionality'),
(2, 'DJ Admin', 1, NULL, NULL, 'Admin DJ for testing');

-- Sample playlists
INSERT INTO `playlist` (`name`, `description`, `posting_dj_id`, `date_played`, `hidden`) VALUES 
('Rock Hits Collection', 'A collection of classic rock hits from the 70s and 80s', 1, '2024-10-01 14:00:00', 0),
('Indie Discoveries', 'New indie tracks worth discovering', 1, '2024-10-08 16:00:00', 0),
('Electronic Vibes', 'Electronic music for late night sessions', 2, '2024-10-10 22:00:00', 0),
('Jazz Standards', 'Classic jazz standards and modern interpretations', 2, '2024-10-12 19:00:00', 0);

-- Sample tracks for playlists
INSERT INTO `playlist_track` (`playlist_id`, `track`, `song`, `artist`, `album`) VALUES 
-- Rock Hits Collection
(1, 1, 'Bohemian Rhapsody', 'Queen', 'A Night at the Opera'),
(1, 2, 'Stairway to Heaven', 'Led Zeppelin', 'Led Zeppelin IV'),
(1, 3, 'Hotel California', 'Eagles', 'Hotel California'),
(1, 4, 'Sweet Child O Mine', 'Guns N Roses', 'Appetite for Destruction'),

-- Indie Discoveries
(2, 1, 'Time to Dance', 'The Sounds', 'Living in America'),
(2, 2, 'Electric Feel', 'MGMT', 'Oracular Spectacular'),
(2, 3, 'Pumped Up Kicks', 'Foster the People', 'Torches'),
(2, 4, 'Midnight City', 'M83', 'Hurry Up, Were Dreaming'),

-- Electronic Vibes
(3, 1, 'Strobe', 'Deadmau5', 'For Lack of a Better Name'),
(3, 2, 'Language', 'Porter Robinson', 'Worlds'),
(3, 3, 'Clarity', 'Zedd', 'Clarity'),
(3, 4, 'Animals', 'Martin Garrix', 'Animals'),

-- Jazz Standards
(4, 1, 'Take Five', 'Dave Brubeck', 'Time Out'),
(4, 2, 'So What', 'Miles Davis', 'Kind of Blue'),
(4, 3, 'Blue Moon', 'Billie Holiday', 'Lady in Satin'),
(4, 4, 'Autumn Leaves', 'Bill Evans Trio', 'Portrait in Jazz');