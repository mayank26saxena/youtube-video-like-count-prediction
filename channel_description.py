import urllib
import json
import sqlite3

db_connection = sqlite3.connect(
    './youtube.db')
db = db_connection.cursor()
all_channel_ids = []

#db_connection.close()
#db.execute("CREATE TABLE CHANNEL(channelId NOT NULL, channel_commentCount INT, channel_viewCount INT, channel_videoCount INT, channel_subscriberCount INT)")

try:
    for i, row in enumerate(db.execute("SELECT channelId FROM VIDEOS").fetchall()):
        all_channel_ids.append(row[0])
except sqlite3.OperationalError, e:
    print 'sqlite3.OperationalError:', e


def get_channel_info(channelId):
    try :
        #channel_id = 'UC3KQ5GWANYF8lChqjZpXsQw'
        key = 'AIzaSyCE61_r8FRDi1PIg6kjeJEG11pziJ4uguw'
        url = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + channelId + "&key=" + key
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        #print data
        all_data = data['items']
        channel_commentCount = all_data[0]['statistics']['commentCount']
        channel_viewCount = all_data[0]['statistics']['viewCount']
        channel_videoCount = all_data[0]['statistics']['videoCount']
        channel_subscriberCount = all_data[0]['statistics']['subscriberCount']


        vars_to_insert = (channelId, channel_commentCount, channel_viewCount, channel_videoCount,
                                  channel_subscriberCount)
        db.execute("INSERT INTO CHANNEL VALUES (?,?,?,?,?)",
                           (vars_to_insert))
        db_connection.commit()

        #print 'comment count' , channel_commentCount
        #print 'view count' , channel_viewCount
        #print 'video count' , channel_videoCount
        #print 'subscriber count' , channel_subscriberCount

    except Exception as e:
        print e.message
        pass


for _id in all_channel_ids:
    get_channel_info(_id)

db_connection.close()
