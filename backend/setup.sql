CREATE DATABASE IF NOT EXISTS kwip;

USE kwip;

DROP TABLE IF EXISTS show_slot;

CREATE TABLE
    show_slot (
        id INT AUTO_INCREMENT,
        day ENUM(
            'Sunday',
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday'
        ) NOT NULL,
        start_time TINYINT NOT NULL,
        end_time TINYINT NOT NULL,
        PRIMARY KEY (id)
    );

INSERT INTO
    show_slot (day, start_time, end_time)
VALUES ('Sunday', 1, 2);