USE `kwip`;

INSERT INTO `semester` VALUES
    (1, 'Fall', 2023),
    (2, 'Spring', 2024);

INSERT INTO `user` VALUES
    -- All of these dummy accounts have the password: 'password'
    (1, 'Carson', 'carson@jones.com', UNHEX('25fcb872a83dfb97b0f487c9c9c5508398e4f9f921de9ac9d9b0d8ec7ca0db9c'), UNHEX('a3b32c3aff3bf0ea733c6e0ee10a12ff9b3cb12f0652c9d07f957ff0ec7ecd6d5ab60f3f179743027027136f6e88d965428c422d962729579603bafb50f5be84'), 'admin'),
    (2, 'Luna', 'im@dog.gov', UNHEX('3ca6818d0d5b4b97ac99cd0f5742fd054e32ec5db9890035ec82fccb0a9b7701'), UNHEX('355db24f35be0fd01c198f52cbf617f9cce2320aadc83d4493a485121cd814d56bd7683bdb88c7fdd59481bf54a84442439c9f1d718aa6f105e797b8d3780e9e'), 'dj'),
    (3, 'test', 'a@b.c', UNHEX('61bd392469af8bd703f10829c6807a9f5bfdc33007c8d22b4fa0d2f2af337761'), UNHEX('92604e44b94dd0ca20635b129dfdd2b7fc3d3ee26287d018f4b149c3e8c2e885f2e0a176f14e30b332bbf685e5bdbcb3dac91d5590d1c4a1342937d82450a2e5'), 'dj');

INSERT INTO `dj` (`id`, `dj_name`, `training_semester_id`)
    VALUES
        (1, 'DJCubed', 1),
        (2, 'MC Dogwater', 2);

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
    (4, '2023-10-22', NULL, NULL, 'automation show', NULL);

INSERT INTO `playlist_track` VALUES
    (1, 1, 'Barely Legal', 'The Strokes', 'Is This It?'),
    (1, 2, 'Roommates', 'Malcolm Todd', NULL),
    (2, 1, 'Raw Dog', 'The Las Vegas', NULL);

INSERT INTO `town_and_campus_news` VALUES
    (1, 'fake event', NULL, 'nothing is really happening', 'nowhere', NULL, 'Nobody AtHome', 'no@email.gone', 0, '2023-11-01 23:51:22', '2026-11-01'),
    (2, '2nd event', 'event holder corps.', 'this is the 2nd event', 'here', 'www.secondfake.org', 'Micheal Jackson', 'mj@dead.org', 1, '2023-10-30 05:04:03', '2023-11-01');