
# DROP TABLES

songplay_table_drop = "drop table if exists songplays"
user_table_drop = "drop table if exists users"
song_table_drop = "drop table if exists songs"
artist_table_drop = "drop table if exists artists"
time_table_drop = "drop table if exists time"

# CREATE TABLES



user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users 
    (
        user_id integer PRIMARY KEY,
        first_name varchar(250) NOT NULL, 
        last_name varchar(250) NOT NULL, 
        gender varchar, 
        level varchar(250)
    )
""")


song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs 
    (
        song_id varchar(250) PRIMARY KEY,
        title varchar(250) NOT NULL, 
        artist_id varchar(250) NOT NULL, 
        year integer, 
        duration float NOT NULL
    )
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists 
    (
        artist_id varchar(250) PRIMARY KEY,
        name varchar(250) NOT NULL, 
        location varchar(250), 
        latitude float,
        longitude float
    )
""")


time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time 
    (
    start_time varchar PRIMARY KEY,
    hour integer, 
    day integer, 
    week integer,
    month integer, 
    year integer,
    weekday integer
    )
""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays
    (
        songplay_id SERIAL PRIMARY KEY, 
        start_time varchar, 
        user_id integer NOT NULL REFERENCES users(user_id), 
        level varchar(250),
        song_id varchar(250) REFERENCES songs(song_id), 
        artist_id varchar(250) REFERENCES artists(artist_id),
        session_id integer,
        location varchar(250), 
        user_agent varchar(250)
    )
""")

# INSERT RECORDS

songplay_table_insert = ("""
    INSERT INTO songplays
    (start_time,user_id,level,song_id,artist_id,session_id,location,user_agent) 
    VALUES (%s, %s, %s, %s,%s, %s, %s, %s) 
""")

user_table_insert = ("""
    INSERT INTO users (user_id,first_name,last_name,gender,level) 
    VALUES (%s, %s, %s, %s, %s) 
    ON CONFLICT (user_id) DO UPDATE SET level = excluded.level 
""")

song_table_insert = ("""
    INSERT INTO songs (song_id, title, artist_id, year, duration) 
    VALUES (%s, %s, %s, %s, %s) 
    ON CONFLICT (song_id) DO NOTHING 
""")

artist_table_insert = ("""
    INSERT INTO artists (artist_id, name, location, latitude, longitude) 
    VALUES (%s, %s, %s, %s, %s)  
    ON CONFLICT (artist_id) DO NOTHING
""")


time_table_insert = ("""
    INSERT INTO time (start_time,hour,day,week,month,year,weekday) 
    values (%s, %s, %s, %s, %s, %s, %s)  
    ON CONFLICT (start_time) DO NOTHING
""")

# FIND SONGS

song_select = ("""
    SELECT S.song_id,A.artist_id from 
    songs S 
    INNER JOIN 
    artists A 
    ON S.artist_id = A.artist_id 
    WHERE S.title = %s 
    AND 
    A.name = %s 
    AND 
    S.duration = %s
""")


# QUERY LISTS

create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create,songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]