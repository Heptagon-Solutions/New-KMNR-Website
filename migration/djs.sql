/*
This gets DJs from `kmnrorg_django` and puts them in a format that can be directly exported into the JSON models that KWIP's frontend should expect
*/

SELECT
    `dj`.`id`,
    `dj`.`name` AS `djName`,
    'John Doe' AS `userName`,
    NULL AS `profileImg`,
    `dj`.`profile` AS `profileDesc`
FROM `kmnrorg_django`.`discjockeys_discjockey` `dj`;