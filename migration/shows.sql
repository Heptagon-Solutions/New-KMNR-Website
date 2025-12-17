/*
Query to get all shows for a specific semester (from `kmnrorg_django`), and reformat them into KWIP's schema
*/

INSERT INTO
    `kwip_migration_temp`.`radio_show`
SELECT
    `show`.`id` AS `id`,
    `show`.`title` AS `name`,
    LEFT(`show`.`detail`, 50) AS `short_desc`,
    NULL AS `long_desc`,
    `slot`.`day` AS `day`,
    HOUR(`slot`.`start_time`) AS `start_time`,
    HOUR(`slot`.`end_time`) AS `end_time`,
    `slot`.`semester_id` AS `semester_id`,
    NULL AS `show_image`
FROM `kmnrorg_django`.`shows_show` `show`
    JOIN `kmnrorg_django`.`shows_slot` `slot` ON `show`.`time_slot_id` = `slot`.`id`
WHERE
    `slot`.`semester_id` = 63