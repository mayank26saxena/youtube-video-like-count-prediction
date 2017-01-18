import urllib, json
channel_id = 'UC3KQ5GWANYF8lChqjZpXsQw'
key = 'AIzaSyCE61_r8FRDi1PIg6kjeJEG11pziJ4uguw'
url = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + channel_id + "&key=" + key
response = urllib.urlopen(url)
data = json.loads(response.read())
#print data
all_data = data['items']
channel_commentCount = all_data[0]['statistics']['commentCount']
channel_viewCount = all_data[0]['statistics']['viewCount']
channel_videoCount = all_data[0]['statistics']['videoCount']
channel_subscriberCount = all_data[0]['statistics']['subscriberCount']

print 'comment count' , channel_commentCount
print 'view count' , channel_viewCount
print 'video count' , channel_videoCount
print 'subscriber count' , channel_subscriberCount
