import urllib
import json
import sqlite3
from nltk.sentiment import SentimentIntensityAnalyzer

db_connection = sqlite3.connect(
    './youtube.db')
db = db_connection.cursor()

all_video_ids = []
all_video_titles = []
all_video_descriptions = []

# db_connection.close()
#db.execute("CREATE TABLE SENTIMENT(videoId NOT NULL, title_sentiment INT, description_sentiment INT)")

try:
    for i, row in enumerate(db.execute("SELECT videoId, title, description FROM VIDEOS").fetchall()):
        all_video_ids.append(row[0])
        all_video_titles.append(row[1])
        all_video_descriptions.append(row[2])
except sqlite3.OperationalError, e:
    print 'sqlite3.OperationalError:', e

# print all_video_ids[:10]
# print all_video_titles[:10]
# print all_video_descriptions[:10]


def find_sentiment(videoId, title, description, sid):
    try:
        ss = sid.polarity_scores(title)
        ss2 = sid.polarity_scores(description)

        title_sentiment = ss['compound']
        description_sentiment = ss2['compound']

        vars_to_insert = (videoId, title_sentiment, description_sentiment)
        db.execute("INSERT INTO SENTIMENT VALUES (?,?,?)",
                           (vars_to_insert))
        db_connection.commit()

    except Exception as e:
        print e.message
        pass


sid = SentimentIntensityAnalyzer()
for i in range(0, len(all_video_ids)):
    find_sentiment(all_video_ids[i], all_video_titles[i], all_video_descriptions[i], sid)

#ss = sid.polarity_scores(all_video_titles[0])
#print ss['compound']
# db_connection.close()
