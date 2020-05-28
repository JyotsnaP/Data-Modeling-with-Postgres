


# Sparkify Data Modelling and Postgres ETL

## Context of this startup:

Our startup is called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

Our role is to create a database schema and ETL pipeline for this analysis. 


### Data

- **Song datasets**: There are multiple json files in subdirectories under */data/song_data*. A sample of this file is as follows:

```
{
	"num_songs": 1, 
	"artist_id": "ARJIE2Y1187B994AB7", 
	"artist_latitude": null, 
	"artist_longitude": null, 
	"artist_location": "", 
	"artist_name": "Line Renaud", 
	"song_id": "SOUPIRU12A6D4FA1E1", 
	"title": "Der Kleine Dompfaff", 
	"duration": 152.92036, 
	"year": 0
}
```

- **Log datasets**: There are multiple json files in subdirectories under */data/log_data*. A sample of a single row of this files is as follows:

```
{
	"artist":"Survivor",
	"auth":"Logged In",
	"firstName":"Jayden",
	"gender":"M",
	"itemInSession":0,
	"lastName":"Fox",
	"length":245.36771,
	"level":"free",
	"location":"New Orleans-Metairie, LA",
	"method":"PUT",
	"page":"NextSong",
	"registration":1541033612796.0,
	"sessionId":100,
	"song":"Eye Of The Tiger",
	"status":200,
	"ts":1541110994796,
	"userAgent":"\"Mozilla\/5.0 (Windows NT 6.3; WOW64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"",
	"userId":"101"
}
```

## Database Schema

The schema used for Sparkify is the Star Schema. 
We have one fact table (songplays) containing facts associated to an event. 
There is one main fact table containing all the measures associated to each event. 
There are 4 dimensional tables (users, songs, artists, and time) in which each of the respective primary keys is referenced from the fact table.

[UML NOTATION](UML notation.jpeg)

### Database schema design:

- The size of the data is not large enough to use a distributed database.
```
song_files = get_files("/home/workspace/data/song_data/")
log_files = get_files("/home/workspace/data/log_data/")

for index in range (0,len(log_files)):
    filepath=log_files[index]
    df = pd.read_json(filepath, lines=True)

print(len(song_files))
93

print(len(df))
327
```

- The data is structured ( as mentioned in the above Data section)- 
	- The data we need to analyze data is of type JSON
	- It is easy to infer where, which and how to extract and transform the required fields
- The analysis that needs to be done can be done using simple SQL queries.
- One of the solutions requires us to do a JOIN & SQL is more efficient for it. 




#### Fact Table
**songplays** - Records from the log data associated with song plays - records that contains page as 'Next Song'

- **songplay_id** (SERIAL) **PRIMARY KEY** : Serial id for each song play
- **start_time** (VARCHAR) : Timestamp of the beginning of the song
- **user_id** (INTEGER) NOT NULL : An integer that uniquely identifies the user
- **level** (VARCHAR) : User level - Valid values : {free | paid}
- **song_id** (VARCHAR) : An ID that uniquely identifies a song
- **artist_id** (VARCHAR) : An ID that uniquely identifies an artist
- **session_id** (INTEGER) : An ID that represents the session
- **location** (VARCHAR) : User's Location
- **user_agent** (VARCHAR) : The agent used by the user to use the Sparkify app. 

#### Dimension Tables

**Users** - Users using the Sparkify app
- **user_id** (INTEGER) **PRIMARY KEY**
- **first_name** (VARCHAR) NOT NULL
- **last_name** (VARCHAR) NOT NULL
- **gender** (VARCHAR)
- **level** (VARCHAR)

**Songs** - Songs in the database
- **song_id** (VARCHAR) **PRIMARY KEY**
- **title** (VARCHAR) NOT NULL
- **artist_id** (VARCHAR) NOT NULL
- **year** (INTEGER)
- **duration** (FLOAT) NOT NULL

**Artists** - Artists in the database

- **artist_id** (VARCHAR) **PRIMARY KEY**
- **name** (VARCHAR) NOT NULL
- **location** (VARCHAR)
- **latitude** (FLOAT)
- **longitude** (FLOAT)

**Time** - Timestamps of records from songplays which has been broken down into units of hour/day/week/month/year/weekday
- **start_time** (VARCHAR) **PRIMARY KEY**
- **hour** (INTEGER)
- **day** (INTEGER)
- **week** (INTEGER)
- **month** (INTEGER)
- **year** (INTEGER)
- **weekday** (INTEGER)


## Project structure
```
+-- data 
|   +-- log_data - Contains log files
|   +-- song_data - Contains song files
+-- sql_queries.py - Contains all the sql queries required 
+-- test.ipynb - A jupiter notebook used for testing connections with the databases and testing 
+-- etl.ipynb - A jupiter notebook used for testing and working through the logic for the ETL 
+-- etl.py - Reads data from /data and process them and load into the tables
+-- README.md - Contains the design and decisions of Sparkify
```

## Steps to complete/run this app: 
 - Complete the sql_queries.py with the required DROP, CREATE queries.
 - To run the above queries run the following file: 
	```
	python create_tables.py
	```
 - To check if the tables were created, check using the file test.ipynb
 - Complete the steps mentioned in etl.ipynb and verify using test.ipynb to check if the records were inserted in respective tables
 - On completion of etl.ipynb, complete etl.py accordingly. 
 - Run the create_tables.py to reset and run the etl.py :
	 ```
	 python create_tables.py
	 python etl.py
	 ```
 - To verify, use test.ipynb

## ETL Pipeline 

- We start with performing an ETL on a single song file and load a single record into each table to start.
	```
	song_files = get_files("/home/workspace/data/song_data/")
	df = pd.read_json(song_files[0], lines=True)
	song_data = list(df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0])
	```
	- Insert the above song_data into the songs table
- We then extract data into the Artists table
	```
	artist_data = list(df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0])
	```
	- Insert the above artist_data into the artists table
- We then process the log data:
	```
	log_files = get_files("/home/workspace/data/log_data/")
	df = df[df['page'] == 'NextSong']
	t = pd.to_datetime(df['ts'], unit='ms')
	time_data = ([data,data.hour,data.day,data.weekofyear,data.month,data.year,data.weekday()] for data in t)
	time_df = pd.DataFrame(time_data, columns=column_labels)
	```
	- Iterate over time_data and insert that into the time table
	```
	log_files = get_files("/home/workspace/data/log_data/")
	filepath=log_files[0]
	df = pd.read_json(filepath, lines=True)
	user_df = df[['userId','firstName','lastName','gender','level']]
	user_df = user_df.drop_duplicates().replace('', numpy.NaN).drop_duplicates().dropna()
	user_df
	```
	-  Iterate over user_df and insert that into the users table
```
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

for index, row in df.iterrows():
    
    # get songid and artistid from song and artist tables
    cur.execute(song_select, (row.song, row.artist, row.length))
    results = cur.fetchone()
    if results:
       songid, artistid = results
    else:
       songid, artistid = None, None

    print(songid,artistid)
    
    #insert songplay record
    songplay_data = ()
    cur.execute(songplay_table_insert, songplay_data)
    conn.commit()
```

### Results of song_plays where the artist_id and song_id is not null:

[SONG_PLAYS_RESULT](song_plays.jpeg)



