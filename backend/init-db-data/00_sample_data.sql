-- THIS DATA IS MEANT FOR DEVELOPMENT ONLY - DO NOT RUN ON PRODUCTION

USE `kwip`;

INSERT INTO `semester` VALUES
    (1, 'Fall', 2023),
    (2, 'Spring', 2024);

INSERT INTO `user` VALUES
    (1, 'Carson', 'carson@jones.com', 'sfgebyrs4346dA', NULL),
    (2, 'Luna', 'im@dog.gov', 'fd73Jsd8SH', NULL);

INSERT INTO `dj` (`id`, `dj_name`, `training_semester_id`)
    VALUES
        (1, 'DJCubed', 1),
        (2, 'MC Dogwater', 2),
        (3, 'Vinyl Viper', 1),
        (4, 'Bass Bandit', 2),
        (5, 'Echo Elite', 1),
        (6, 'Mix Master Maya', 2),
        (7, 'Sound Sage', 1),
        (8, 'Beat Builder', 2),
        (9, 'Rhythm Renegade', 1),
        (10, 'Frequency Phoenix', 2);

INSERT INTO `radio_show`
    (`id`, `name`, `day`, `start_time`, `end_time`, `semester_id`)
    VALUES
        (1, 'Music Appreciation 201', 'Monday', 18, 20, 1),
        (2, 'Music Appreciation 202', 'Monday', 18, 20, 2),
        (3, 'Walking the dog', 'Friday', 8, 17, 1),
        (4, 'Beggin for scraps', 'Saturday', 14, 15, 1);

INSERT INTO `show_host` VALUES
    (1, 1),
    (2, 1),
    (3, 1),
    (3, 2),
    (4, 2);

INSERT INTO `rented_show`
    (`radio_show_id`, `rent_date`, `claimer_dj_id`)
    VALUES
        (1, '2023-11-06', NULL),
        (4, '2023-11-04', 1);

INSERT INTO `playlist`
    (`id`, `date_played`, `posting_dj_id`, `radio_show_id`, `name`, `description`)
    VALUES
    (1, '2023-10-30', 1, 1, NULL, NULL),
    (2, '2023-10-13', 1, 3, 'Spooky walk', 'walking on friday 13th'),
    (3, '2023-10-20', 2, NULL, 'impromptu show', NULL),
    (4, '2023-10-22', NULL, NULL, 'automation show', NULL),
    (5, '2023-11-01', 3, NULL, 'Vinyl Vibes', 'Classic rock and vintage hits'),
    (6, '2023-11-02', 4, NULL, 'Bass Drop Zone', 'Heavy electronic beats'),
    (7, '2023-11-03', 5, NULL, 'Echo Chamber', 'Ambient and atmospheric'),
    (8, '2023-11-04', 6, NULL, 'Maya Mix', 'Hip-hop and R&B fusion'),
    (9, '2023-11-05', 7, NULL, 'Wisdom Sessions', 'Jazz and blues classics'),
    (10, '2023-11-06', 8, NULL, 'Beat Laboratory', 'Experimental electronic'),
    (11, '2023-11-07', 9, NULL, 'Rebel Radio', 'Punk and alternative rock'),
    (12, '2023-11-08', 10, NULL, 'Phoenix Rising', 'Indie and emerging artists');

INSERT INTO `playlist_track` VALUES
    (1, 1, 'Barely Legal', 'The Strokes', 'Is This It?'),
    (1, 2, 'Roommates', 'Malcolm Todd', NULL),
    (2, 1, 'Raw Dog', 'The Las Vegas', NULL);

INSERT INTO `town_and_campus_news` VALUES
    (1, 'fake event', NULL, 'nothing is really happening', 'nowhere', NULL, 'Nobody AtHome', 'no@email.gone', 0, '2023-11-01 23:51:22', '2026-11-01'),
    (2, '2nd event', 'event holder corps.', 'this is the 2nd event', 'here', 'www.secondfake.org', 'Micheal Jackson', 'mj@dead.org', 1, '2023-10-30 05:04:03', '2023-11-01');