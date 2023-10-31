CREATE DATABASE IF NOT EXISTS kwip;
USE kwip;

DROP TABLE IF EXISTS user;
CREATE TABLE
    user (
        id INT AUTO_INCREMENT,
        name VARCHAR(50) NOT NULL,
        email VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(50) NOT NULL,
        role VARCHAR(50),  -- IDK about this one; probably should be enum
        PRIMARY KEY (ID)
    );

DROP TABLE IF EXISTS dj;
CREATE TABLE
    dj (
        id INT AUTO_INCREMENT,
        dj_name VARCHAR(50) NOT NULL,
        sem_trained ENUM('Spring', 'Summer', 'Fall') NOT NULL,
        year_trained YEAR NOT NULL,
        trainer_dj_id INT,  -- Can not make NOT NULL; how would we add the first DJ?
        sem_grad ENUM('Spring', 'Summer', 'Fall'),
        year_grad YEAR,
        profile_desc TINYTEXT,  -- Longer?
        profile_img MEDIUMBLOB,  -- What's best Blob size?
        PRIMARY KEY (id),
        FOREIGN KEY (id) REFERENCES user(id),
        FOREIGN KEY (trainer_dj_id) REFERENCES dj(id)
    );

DROP TABLE IF EXISTS town_and_campus_news;
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

-- Idek if we'll use this one
-- CREATE TABLE Show_Slot{
--    ID int,
--    Day VARCHAR(10),
--    Start_Time tinyint, //DATETIME unneccessary
--    End_Time tinyint,
--    Sem_Year VARCHAR(20),
-- }

DROP TABLE IF EXISTS radio_show;
CREATE TABLE
    radio_show (
        id INT AUTO_INCREMENT,
        name VARCHAR(50) NOT NULL,
        long_desc TINYTEXT,  -- Longer?
        short_desc VARCHAR(50),  -- Shorter?
        -- Associated_Slot from showslot table
        -- Fuck, idk if we need those slots or not man
        show_image MEDIUMBLOB,  -- What's the best blob size?
        PRIMARY KEY (id)
    );

DROP TABLE IF EXISTS show_host;
CREATE TABLE
    show_host (
        radio_show_id INT,
        dj_id INT,
        PRIMARY KEY (radio_show_id, dj_id),
        FOREIGN KEY (radio_show_id) REFERENCES radio_show (id),
        FOREIGN KEY (dj_id) REFERENCES dj(id)
    );

DROP TABLE IF EXISTS rented_show;
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

DROP TABLE IF EXISTS playlist;
CREATE TABLE
    playlist (
        id INT,
        radio_show_id INT NOT NULL,
        name VARCHAR(50),  -- Null allowed for DJs who don't leave playlist names in KLAP
        desc TINYTEXT,  -- Longer? Shorter?
        date_played DATE NOT NULL,  -- Default to current date?
        -- Listenership: Problem for another day
        -- Spotify_URL VARCHAR(50): Problem for another day
        hidden BOOLEAN NOT NULL DEFAULT 0,
        playlist_img MEDIUMBLOB,  -- What's the best blob size?
        PRIMARY KEY (ID),
        FOREIGN KEY (radio_show_id) REFERENCES radio_show(id)
    );

DROP TABLE IF EXISTS playlist_track;
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