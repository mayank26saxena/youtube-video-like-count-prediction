#!/usr/bin/python

import json
import re
from time import sleep
import datetime
import calendar
import sqlite3

import strict_rfc3339

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

DEVELOPER_KEY = "AIzaSyCE61_r8FRDi1PIg6kjeJEG11pziJ4uguw"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


t1 = datetime.datetime(2016, 7, 1, 0, 0, 0) # from July 1, 2016
t1 = calendar.timegm(t1.timetuple())
t2 = datetime.datetime(2016, 12, 31, 0, 0, 0) # to December 1, 2016
t2 = calendar.timegm(t2.timetuple())
t = t1

while True:
	try:
		db_connection = sqlite3.connect('/home/mayank/Desktop/precog/youtube/create-database/youtube.db')
		print "Opened database successfully"
		db = db_connection.cursor()

		youtube = build(
			YOUTUBE_API_SERVICE_NAME,
			YOUTUBE_API_VERSION,
			developerKey=DEVELOPER_KEY
		)

		while True:
			idx = 1
			pageToken = ""
			videoIds = []

			publishedAfter = strict_rfc3339.timestamp_to_rfc3339_utcoffset(t)
			publishedBefore = strict_rfc3339.timestamp_to_rfc3339_utcoffset(t + (60*60))
			print("> %s - %s" % (publishedAfter, publishedBefore))

			while True:
				search = youtube.search().list(
					part="snippet",
					type="video",
					order="viewCount",
					publishedAfter=publishedAfter,
					publishedBefore=publishedBefore,
					maxResults=50,
					pageToken=pageToken,
					safeSearch="none",
				).execute()

				for r in search.get("items", []):
				
					#print r
					
					videoId 	= r["id"]["videoId"]
					channelId	= r["snippet"]["channelId"]

					# don't process videos found in earlier batches
					if videoId in videoIds:
						continue
					videoIds.append(videoId)

					videos = youtube.videos().list(
						id=videoId,
						part="snippet, contentDetails, recordingDetails, statistics, status", #id, snippet, contentDetails, localizations, player, statistics, status
					).execute()

					for r in videos.get("items", []):
						# skip live broadcasts
						try:
							liveBroadcastContent = r["snippet"]["liveBroadcastContent"]
							if liveBroadcastContent != "none":
								continue
						except KeyError:
							continue

						# basics
						videoId 		= videoId
						channelId 		= channelId
						channelTitle	= r["snippet"]["channelTitle"]

						# snippet
						title 		= r["snippet"]["title"]
						description = r["snippet"]["description"]
						categoryId	= int(r["snippet"]["categoryId"])
						publishedAt	= r["snippet"]["publishedAt"]
						publishedAt	= int(strict_rfc3339.rfc3339_to_timestamp(publishedAt))
						currentTime	= datetime.datetime.utcnow() # current time as rtf3339
						currentTime	= datetime.datetime.timetuple(currentTime) # current time as timetuple
						currentTime	= calendar.timegm(currentTime) # current time as epoch timestamp
						life = currentTime - publishedAt

						# contentDetails
						definition 			= r["contentDetails"]["definition"]
						caption 			= 0 if r["contentDetails"]["caption"].lower() == 'false' else 1
						duration 			= r["contentDetails"]["duration"]
						duration_w 			= re.search(r"(\d+)w", duration, re.I)
						duration_w 			= int(duration_w.group(1)) if duration_w else 0
						duration_d 			= re.search(r"(\d+)d", duration, re.I)
						duration_d 			= int(duration_d.group(1)) if duration_d else 0
						duration_h 			= re.search(r"(\d+)h", duration, re.I)
						duration_h 			= int(duration_h.group(1)) if duration_h else 0
						duration_m 			= re.search(r"(\d+)m", duration, re.I)
						duration_m 			= int(duration_m.group(1)) if duration_m else 0
						duration_s 			= re.search(r"(\d+)s", duration, re.I)
						duration_s 			= int(duration_s.group(1)) if duration_s else 0
						duration 			= 0
						duration 			+= duration_w * 7 * 24 * 60 * 60
						duration 			+= duration_d * 24 * 60 * 60
						duration 			+= duration_h * 60 * 60
						duration 			+= duration_m * 60
						duration 			+= duration_s * 1
						durationCategory	= "short"
						durationCategory	= "medium" if duration_m >= 4 else "short"
						durationCategory	= "long" if duration_m >= 20 else "medium"
						licensedContent 	= 0 if r["contentDetails"]["licensedContent"] == False else 1
						dimension 			= r["contentDetails"]["dimension"]
						try:
							allowed = ','.join(r["contentDetails"]["regionRestriction"]["allowed"])
						except Exception:
							allowed = None
						try:
							allowedCount = len(r["contentDetails"]["regionRestriction"]["allowed"])
						except Exception:
							allowedCount = 0
						
						# recordingDetails
						try:
							recordingDate	= r["recordingDetails"]["recordingDate"]
							recordingDate 	= int(strict_rfc3339.rfc3339_to_timestamp(recordingDate))
						except Exception:
							recordingDate	= None
						try:
							latitude		= r["recordingDetails"]["location"]["latitude"]
						except Exception:
							latitude		= None
						try:
							longitude		= r["recordingDetails"]["location"]["longitude"]
						except Exception:
							longitude		= None
						

						# status
						publicStatsViewable	= int(r["status"]["publicStatsViewable"])
						privacyStatus 		= r["status"]["privacyStatus"]
						license 			= r["status"]["license"]
						embeddable 			= int(r["status"]["embeddable"])

						# statistics
						try:
							commentCount	= int(r["statistics"]["commentCount"])
						except Exception:
							commentCount	= None
						try:
							viewCount 		= int(r["statistics"]["viewCount"])
						except Exception:
							viewCount	= None						
						try:
							favoriteCount 	= int(r["statistics"]["favoriteCount"])
						except Exception:
							favoriteCount	= None
						try:
							dislikeCount 	= int(r["statistics"]["dislikeCount"])
						except Exception:
							dislikeCount	= None
						try:
							likeCount 		= int(r["statistics"]["likeCount"])
						except Exception:
							likeCount	= None
							
						sql_insert_vars = (videoId,
							channelId,
							channelTitle,
							title,
							description,
							categoryId,
							publishedAt,
							currentTime,
							life,
							definition,
							caption,
							duration,
							durationCategory,
							licensedContent,
							dimension,
							allowed,
							allowedCount,
							recordingDate,
							latitude,
							longitude,
							publicStatsViewable,
							privacyStatus,
							license,
							embeddable,
							commentCount,
							viewCount,
							favoriteCount,
							dislikeCount,
							likeCount,
						)

						try:
							db.execute("INSERT INTO VIDEOS VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (sql_insert_vars))
							#print "Record inserted successfully";
						except sqlite3.IntegrityError:
							print('sqlite3.IntegrityError: videoId=%s' % videoId)

						print("%s - %s --- #%d --- %s" % (publishedAfter, publishedBefore, idx, videoId.encode('utf-8'))) #  --- %s              , title.encode('utf-8')
						idx += 1

				db_connection.commit()
				#print "Records committed successfully"

				try:
					pageToken = search["nextPageToken"]
				except KeyError:
					pageToken = None
					break
			
			t += (60*60)
			if t >= t2:
				break

		db_connection.close()
		break

	except HttpError, e:
		print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
		db_connection.close()

		#print("Waiting for 60 seconds...")
		sleep(60)

		pass
