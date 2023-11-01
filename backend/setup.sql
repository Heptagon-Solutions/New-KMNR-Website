CREATE DATABASE IF NOT EXISTS kwip;
USE kwip;

DROP TABLE IF EXISTS playlist_track;
DROP TABLE IF EXISTS playlist;
DROP TABLE IF EXISTS rented_show;
DROP TABLE IF EXISTS show_host;
DROP TABLE IF EXISTS radio_show;
DROP TABLE IF EXISTS town_and_campus_news;
DROP TABLE IF EXISTS dj;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS semester;

CREATE TABLE
    semester (
        id INT AUTO_INCREMENT,
        semester ENUM('Spring','Summer','Fall') NOT NULL,
        year YEAR NOT NULL,
        PRIMARY KEY (id)
    );

CREATE TABLE
    user (
        id INT AUTO_INCREMENT,
        name VARCHAR(50) NOT NULL,
        email VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(50) NOT NULL,
        role VARCHAR(50),  -- IDK about this one; probably should be enum
        PRIMARY KEY (ID)
    );

CREATE TABLE
    dj (
        id INT AUTO_INCREMENT,
        dj_name VARCHAR(50) NOT NULL,
        training_semester_id INT NOT NULL,
        trainer_dj_id INT,  -- Can not make NOT NULL; how would we add the first DJ?
        graduating_semester_id INT,
        profile_desc TINYTEXT,  -- Longer?
        profile_img MEDIUMBLOB,  -- What's best Blob size?
        PRIMARY KEY (id),
        FOREIGN KEY (id) REFERENCES user(id),
        FOREIGN KEY (training_semester_id) REFERENCES semester(id),
        FOREIGN KEY (trainer_dj_id) REFERENCES dj(id),
        FOREIGN KEY (graduating_semester_id) REFERENCES semester(id)
    );

CREATE TABLE
    town_and_campus_news (
        id INT AUTO_INCREMENT,
        title VARCHAR(50) NOT NULL,
        organization VARCHAR(50),
        description TEXT NOT NULL,  -- TEXT can be sized for enforcing char-limit
        location VARCHAR(50) NOT NULL,
        website VARCHAR(50),  -- Lengthen for longer URLs?
        contact_name VARCHAR(50) NOT NULL,
        contact_email VARCHAR(50) NOT NULL,
        approved BOOLEAN NOT NULL DEFAULT 0,
        submit_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        expiration_date TIMESTAMP NOT NULL,
        PRIMARY KEY (id)
    );

CREATE TABLE
    radio_show (
        id INT AUTO_INCREMENT,
        name VARCHAR(50) NOT NULL,
        short_desc VARCHAR(50),  -- Shorter?
        long_desc TINYTEXT,  -- Longer?
        day ENUM('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday') NOT NULL,
        start_time TINYINT NOT NULL,  -- Only 24 values needed, maybe customize with BIT(size)?
        end_time TINYINT NOT NULL,  -- Only 24 values needed, maybe customize with BIT(size)?
        semester_id INT NOT NULL,
        show_image MEDIUMBLOB,  -- What's the best blob size?
        PRIMARY KEY (id),
        FOREIGN KEY (semester_id) REFERENCES semester(id)
    );

CREATE TABLE
    show_host (
        radio_show_id INT,
        dj_id INT,
        PRIMARY KEY (radio_show_id, dj_id),
        FOREIGN KEY (radio_show_id) REFERENCES radio_show (id),
        FOREIGN KEY (dj_id) REFERENCES dj(id)
    );

CREATE TABLE
    rented_show (
        id INT,  -- Remove surrogate; use composite show_id + rent_date key instead?
        radio_show_id INT NOT NULL,
        rent_date DATE NOT NULL,  -- Time can be found from joining with show or slot table
        claimer_dj_id INT,
        PRIMARY KEY (id),
        FOREIGN KEY (radio_show_id) REFERENCES radio_show (id),
        FOREIGN KEY (claimer_dj_id) REFERENCES dj(id)
    );

CREATE TABLE
    playlist (
        id INT,
        radio_show_id INT NOT NULL,
        name VARCHAR(50),  -- Null allowed for DJs who don't leave playlist names in KLAP
        description TINYTEXT,  -- Longer? Shorter?
        date_played DATE NOT NULL,  -- Default to current date?
        -- Listenership: Problem for another day
        -- Spotify_URL VARCHAR(50): Problem for another day
        hidden BOOLEAN NOT NULL DEFAULT 0,
        playlist_img MEDIUMBLOB,  -- What's the best blob size?
        PRIMARY KEY (ID),
        FOREIGN KEY (radio_show_id) REFERENCES radio_show(id)
    );

CREATE TABLE
    playlist_track (
        playlist_id INT,
        track TINYINT,  -- unsigned preferably
        song VARCHAR(100) NOT NULL,  -- what's the best size for this?
        artist VARCHAR(100) NOT NULL,  -- what's the best size for this?
        album VARCHAR(50),  -- what's the best size for this?
        -- Spotify_URL VARCHAR(50): Problem for another day
        PRIMARY KEY (playlist_id, track),
        FOREIGN KEY (playlist_id) REFERENCES playlist(id)
    );