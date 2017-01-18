#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('youtube.db')
print "Opened database successfully";

conn.execute('''CREATE TABLE VIDEOS
       (videoId INT PRIMARY KEY     NOT NULL,
		channelId	INT,
		channelTitle	TEXT,
		title	TEXT,
		description	TEXT,
		categoryId INT,
        publishedAt INT,
        currentTime INT,
        life INT,
        definition TEXT,
        caption INT,
        duration INT,
        durationCategory TEXT,
        licensedContent TEXT,
        dimension INT,
        allowed TEXT,
        allowedCount INT,
        recordingDate INT,
        latitude INT,
        longitude INT,
        publicStatsViewable INT,
        privacyStatus INT,
        license TEXT,
        embeddable INT,
        commentCount INT,
        viewCount INT,
        favoriteCount INT,
        dislikeCount INT,
        likeCount INT);''')
        
print "Table created successfully";

conn.commit()
conn.close()
