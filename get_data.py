import json
import urllib
import strict_rfc3339
import datetime
import calendar
import re
import cPickle as pickle
import math
import jordy
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer
from scipy.sparse import coo_matrix, hstack

video_ids=[] #,"SGmwsrjkjM8","GIt01DTdqpg"]
api_key="AIzaSyCE61_r8FRDi1PIg6kjeJEG11pziJ4uguw"


numerical_features = []
categorical_features = []

for video_id in video_ids :
   #print 'video_id : ', video_id
   url = "https://www.googleapis.com/youtube/v3/videos?id=" + video_id + "&key=" + api_key + "&part=status,statistics,contentDetails,snippet"
   response = urllib.urlopen(url).read()
   data = json.loads(response)
   all_data = data['items']
   #print all_data

   #Snippet
   channelId = all_data[0]['snippet']['channelId']
   channelTitle = all_data[0]['snippet']['channelTitle']
   title = all_data[0]['snippet']['title']
   description = all_data[0]['snippet']['description']
   category_id = all_data[0]['snippet']['categoryId']
   publishedAt = all_data[0]['snippet']['publishedAt'] 
   publishedAt	= int(strict_rfc3339.rfc3339_to_timestamp(publishedAt))
   currentTime	= datetime.datetime.utcnow() # current time as rtf3339
   currentTime	= datetime.datetime.timetuple(currentTime) # current time as timetuple
   currentTime	= calendar.timegm(currentTime) # current time as epoch timestamp
   life = currentTime - publishedAt

   #Content Details
   defintion = all_data[0]['contentDetails']['definition']
   caption = all_data[0]['contentDetails']['caption']
   licensedContent = all_data[0]['contentDetails']['licensedContent']
   dimension = all_data[0]['contentDetails']['dimension']

   duration = all_data[0]['contentDetails']['duration']
   duration_w = re.search(r"(\d+)w", duration, re.I)
   duration_w = int(duration_w.group(1)) if duration_w else 0
   duration_d = re.search(r"(\d+)d", duration, re.I)
   duration_d = int(duration_d.group(1)) if duration_d else 0
   duration_h = re.search(r"(\d+)h", duration, re.I)
   duration_h = int(duration_h.group(1)) if duration_h else 0
   duration_m = re.search(r"(\d+)m", duration, re.I)
   duration_m = int(duration_m.group(1)) if duration_m else 0
   duration_s = re.search(r"(\d+)s", duration, re.I)
   duration_s = int(duration_s.group(1)) if duration_s else 0
   duration = 0
   duration += duration_w * 7 * 24 * 60 * 60
   duration += duration_d * 24 * 60 * 60
   duration += duration_h * 60 * 60
   duration += duration_m * 60
   duration += duration_s * 1
   durationCategory	= "short"
   durationCategory	= "medium" if duration_m >= 4 else "short"
   durationCategory	= "long" if duration_m >= 20 else "medium"

   try:
	   allowed = ','.join(all_data[0]["contentDetails"]["regionRestriction"]["allowed"])
   except Exception:
	   allowed = None
   try:
	   allowedCount = len(all_data[0]["contentDetails"]["regionRestriction"]["allowed"])
   except Exception:
	   allowedCount = 0

   # recordingDetails
   try:
	   recordingDate = all_data[0]["recordingDetails"]["recordingDate"]
	   recordingDate = int(strict_rfc3339.rfc3339_to_timestamp(recordingDate))
   except Exception:
	   recordingDate = None
   try:
	   latitude = all_data[0]["recordingDetails"]["location"]["latitude"]
   except Exception:
	   latitude = None
   try:
	   longitude = all_data[0]["recordingDetails"]["location"]["longitude"]
   except Exception:
	   longitude = None

   # status
   publicStatsViewable	= int(all_data[0]['status']['publicStatsViewable'])
   privacyStatus = all_data[0]['status']['privacyStatus']
   license	= all_data[0]['status']['license']
   embeddable = int(all_data[0]['status']['embeddable'])

   #Statistics
   commentCount = int(all_data[0]['statistics']['commentCount'])
   viewCount = int(all_data[0]['statistics']['viewCount'])
   favoriteCount = int(all_data[0]['statistics']['favoriteCount'])
   likeCount = int(all_data[0]['statistics']['likeCount'])
   dislikeCount = int(all_data[0]['statistics']['dislikeCount'])



   numerical_features.append([
  	  viewCount,
   	  commentCount,
   	  favoriteCount,
      dislikeCount,
      duration,
      ]) 
        
   # categorical features
   #print 'description ', description
   description_containsWebsite = 0 #jordy.containsWebsite(description)
   description_containsSocialMedia = 1 #jordy.containsSocialMedia(description)
        
   categorical_features.append([
      description_containsWebsite,
      description_containsSocialMedia,
     ])

    

with open('my_numerical_encoder.pkl', 'rb') as fid:
    numencoder = pickle.load(fid)
with open('my_categorical_encoder.pkl', 'rb') as fid:
    catencoder = pickle.load(fid)
    
#scaler = StandardScaler()
numerical_features2 = numencoder.transform(numerical_features)
#onehot = OneHotEncoder()
categorical_features2 = catencoder.transform(categorical_features)

#print numerical_features2.shape, 'numerical_features2'
#print categorical_features2.shape, 'categorical_features2'
         

X = hstack([numerical_features2, categorical_features2])

#print X.shape

#print '\nnumerical before:\n'
#print numerical_features[0]
#print '\nnumerical after:\n'
#print numerical_features2[0]

#print '\ncategorical before:\n'
#print categorical_features[0]

#print '\ncategorical after:\n'
#print categorical_features2[0].toarray()

#print ''
#print 'final X:', X.getrow(0).todense()


with open('my_dumped_classifier.pkl', 'rb') as fid:
    model = pickle.load(fid)
    
y_pred = []
y_pred = model.predict(X)
print 'Predicted : ', y_pred
print 'Actual : ', likeCount

'''
https://www.googleapis.com/youtube/v3/videos?id=byNRLEkv0Fg&key=AIzaSyCE61_r8FRDi1PIg6kjeJEG11pziJ4uguw&part=status,snippet,contentDetails,statistics
video Id - done
Channel Id - done
Channel Title - done
Title - done 
Description - done
Category ID - done
publishedAt - done
currentTime - done
life - done
definition - done
caption - done 
duration - done
durationCategory - done
licensedContent - done
dimension - done
allowed - done
allowedCount - done
recordingDate - done
Latitude - done
Longitude - done
public stats Viewable - done
privacy status - done
license - done
embeddable - done
comment count - done
view count - done
favorite count - done
dislike count - done
like count - done
'''
