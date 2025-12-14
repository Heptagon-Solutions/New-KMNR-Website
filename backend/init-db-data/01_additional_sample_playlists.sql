-- Additional sample playlists and tracks for development
-- Run after 00_sample_data.sql

USE `kwip`;

-- Add more recent playlists with current dates (let database auto-generate IDs)
INSERT INTO `playlist`
    (`date_played`, `posting_dj_id`, `radio_show_id`, `name`, `description`)
    VALUES
    ('2024-12-13 14:00:00', 1, 1, 'Friday Indie Mix', 'Indie rock and alternative tracks for your Friday afternoon'),
    ('2024-12-13 16:00:00', 2, 3, 'Electronic Vibes', 'Electronic and synth-pop journey'),
    ('2024-12-12 20:00:00', 1, 1, 'Classic Rock Hour', 'Greatest hits from the 70s and 80s'),
    ('2024-12-12 18:00:00', 2, NULL, 'Jazz & Blues Evening', 'Smooth jazz and blues for a relaxing evening'),
    ('2024-12-11 12:00:00', 1, 3, 'Metal Mayhem', 'Heavy metal and rock anthems'),
    ('2024-12-11 10:00:00', NULL, NULL, 'Morning Pop Mix', 'Upbeat pop songs to start your day');

-- Add tracks for Friday Indie Mix (playlist 5)
INSERT INTO `playlist_track` VALUES
    (5, 1, 'Last Nite', 'The Strokes', 'Is This It'),
    (5, 2, 'Creep', 'Radiohead', 'Pablo Honey'),
    (5, 3, 'Mr. Brightside', 'The Killers', 'Hot Fuss'),
    (5, 4, 'Take Me Out', 'Franz Ferdinand', 'Franz Ferdinand'),
    (5, 5, 'Somebody Told Me', 'The Killers', 'Hot Fuss'),
    (5, 6, 'Float On', 'Modest Mouse', 'Good News for People Who Love Bad News');

-- Add tracks for Electronic Vibes (playlist 6)
INSERT INTO `playlist_track` VALUES
    (6, 1, 'One More Time', 'Daft Punk', 'Discovery'),
    (6, 2, 'Blue Monday', 'New Order', 'Power, Corruption & Lies'),
    (6, 3, 'Around the World', 'Daft Punk', 'Homework'),
    (6, 4, 'Breathe Me', 'Sia', '1000 Forms of Fear'),
    (6, 5, 'Midnight City', 'M83', 'Hurry Up, We''re Dreaming'),
    (6, 6, 'Crystallised', 'The xx', 'xx');

-- Add tracks for Classic Rock Hour (playlist 7)
INSERT INTO `playlist_track` VALUES
    (7, 1, 'Stairway to Heaven', 'Led Zeppelin', 'Led Zeppelin IV'),
    (7, 2, 'Bohemian Rhapsody', 'Queen', 'A Night at the Opera'),
    (7, 3, 'Hotel California', 'Eagles', 'Hotel California'),
    (7, 4, 'Sweet Child O'' Mine', 'Guns N'' Roses', 'Appetite for Destruction'),
    (7, 5, 'Free Bird', 'Lynyrd Skynyrd', 'pronounced ''leh-''nérd ''skin-''nérd'),
    (7, 6, 'Dream On', 'Aerosmith', 'Aerosmith');

-- Add tracks for Jazz & Blues Evening (playlist 8)
INSERT INTO `playlist_track` VALUES
    (8, 1, 'Kind of Blue', 'Miles Davis', 'Kind of Blue'),
    (8, 2, 'Take Five', 'Dave Brubeck', 'Time Out'),
    (8, 3, 'The Thrill Is Gone', 'B.B. King', 'Completely Well'),
    (8, 4, 'Summertime', 'Ella Fitzgerald', 'Porgy and Bess'),
    (8, 5, 'Mack the Knife', 'Louis Armstrong', 'Satch Plays Fats'),
    (8, 6, 'Blue Train', 'John Coltrane', 'Blue Train');

-- Add tracks for Metal Mayhem (playlist 9)
INSERT INTO `playlist_track` VALUES
    (9, 1, 'Enter Sandman', 'Metallica', 'Metallica'),
    (9, 2, 'Master of Puppets', 'Metallica', 'Master of Puppets'),
    (9, 3, 'Paranoid', 'Black Sabbath', 'Paranoid'),
    (9, 4, 'Ace of Spades', 'Motörhead', 'Ace of Spades'),
    (9, 5, 'Breaking the Law', 'Judas Priest', 'British Steel'),
    (9, 6, 'Run to the Hills', 'Iron Maiden', 'The Number of the Beast');

-- Add tracks for Morning Pop Mix (playlist 10)
INSERT INTO `playlist_track` VALUES
    (10, 1, 'Shake It Off', 'Taylor Swift', '1989'),
    (10, 2, 'Uptown Funk', 'Mark Ronson ft. Bruno Mars', 'Uptown Special'),
    (10, 3, 'Can''t Stop the Feeling!', 'Justin Timberlake', 'Trolls Soundtrack'),
    (10, 4, 'Happy', 'Pharrell Williams', 'Girl'),
    (10, 5, 'Good as Hell', 'Lizzo', 'Cuz I Love You'),
    (10, 6, 'Sunflower', 'Post Malone & Swae Lee', 'Spider-Man: Into the Spider-Verse Soundtrack');

-- Add a few more tracks to existing playlists to make them more substantial
INSERT INTO `playlist_track` VALUES
    (1, 3, 'Under Control', 'The Strokes', 'Room on Fire'),
    (1, 4, 'Reptilia', 'The Strokes', 'Room on Fire'),
    (2, 2, 'Monster', 'Kanye West ft. Jay-Z', 'My Beautiful Dark Twisted Fantasy'),
    (2, 3, 'Thriller', 'Michael Jackson', 'Thriller'),
    (3, 1, 'Somebody That I Used to Know', 'Gotye', 'Making Mirrors'),
    (3, 2, 'Pumped Up Kicks', 'Foster the People', 'Torches'),
    (4, 1, 'Automatic', 'Mildlife', 'Automatic'),
    (4, 2, 'Robots', 'Dan Deacon', 'Bromst');