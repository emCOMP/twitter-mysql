#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
from mysql_insert_queries import *
from pprint import pprint

#
#
#
#

def insert_tweet(tweet, cursor):
	
	user = tweet["user"]

	obj = {
		"id": tweet["id"],
		"created_at": tweet["created_at"],
		"created_ts": tweet["created_ts"],
		"lang": tweet["lang"],
		"text": tweet["text"],
		"user_id": user["id"],
		"user_screen_name": user["screen_name"],
		"user_followers_count": user["followers_count"],
		"user_friends_count": user["friends_count"],
		"user_statuses_count": user["statuses_count"],
		"user_favourites_count": user["favourites_count"],
		"user_geo_enabled": user["geo_enabled"],
		"user_time_zone": user["time_zone"],
		"source": tweet["source"],
		"in_reply_to_screen_name": tweet["in_reply_to_screen_name"],
		"in_reply_to_status_id": tweet["in_reply_to_status_id"],
		"in_reply_to_user_id": tweet["in_reply_to_user_id"]		
	}


	if "geo" in obj and "coordinates" in obj["geo"] and len(obj["geo"]["coordinates"]) > 1:
		geo = {
			"geo_coordinates_0": tweet["geo"]["coordinates"][0],
			"geo_coordinates_1": tweet["geo"]["coordinates"][1],		
		}
	else:
		geo = {
			"geo_coordinates_0": None,
			"geo_coordinates_1": None
		}


	if "retweeted_status" in tweet:
		stmt = INSERT_TWEET_WITH_RETWEET_STMT
		#stmt = INSERT_TWEET_STMT
		retweet = {
			"retweeted_status_id": tweet["retweeted_status"]["id"],
			"retweeted_status_retweet_count": tweet["retweeted_status"]["retweet_count"],
			"retweeted_status_user_screen_name": tweet["retweeted_status"]["user"]["screen_name"],			
			"retweeted_status_user_id": tweet["retweeted_status"]["user"]["id"],
			"retweeted_status_user_time_zone": tweet["retweeted_status"]["user"]["time_zone"],
			"retweeted_status_user_friends_count": tweet["retweeted_status"]["user"]["friends_count"],
			"retweeted_status_user_statuses_count": tweet["retweeted_status"]["user"]["statuses_count"],
			"retweeted_status_user_followers_count": tweet["retweeted_status"]["user"]["followers_count"],
		}
	else:
		stmt = INSERT_TWEET_STMT
		retweet = {
		}


	obj.update(geo)
	obj.update(retweet)

	#pprint(obj)

	cursor.execute(stmt, obj)



#
#
#
#
#
class UserManager(object):
	"""

	"""

	def __init__(self, cursor):
		"""

		"""

		self.inserted_ids = set()
		self.cursor = cursor


	def add(self, tweet):
		"""

		"""


		user = tweet['user']
		id = user['id']

		# skip if already in the data
		#if id in self.inserted_ids
		#	return

		obj = self.build_obj(user)



	def do_insert(self, cursor, obj):
		self.cursor.execute(REPLACE_USER_STMT, obj)
		self.inserted_ids.add(obj["id"])


	def add_empty(self, user_id, user_screen_name):
		"""

		"""
		obj = {
		"id": user_id, 
		"screen_name": user_screen_name,
		"description": None,
		"followers_count": None,
		"friends_count": None,
		"statuses_count": None,
		"favourites_count": None,
		"location": None,
		"created_at": None,
		"created_ts": None,
		"geo_enabled": None,
		"lang": None,
		"listed_count": None,
		"name": None,
		"time_zone": None,
		"url": None,
		"utc_offset": None,
		"verified": None
		}

		self.do_insert(self.cursor, obj)





	def build_obj(self,user):
		"""

		"""


		obj = {		
		"id": user["id"], 
		"screen_name": user["screen_name"],
		"description": user["description"],
		"followers_count": user["followers_count"],
		"friends_count": user["friends_count"],
		"statuses_count": user["statuses_count"],
		"favourites_count": user["favourites_count"],
		"location": user["location"],
		"created_at": user["created_at"],
		"created_ts": user["created_ts"],
		"geo_enabled": user["geo_enabled"],
		"lang": user["lang"],
		"listed_count": user["listed_count"],
		"name": user["name"],
		"time_zone": user["time_zone"],
		"url": user["url"],
		"utc_offset": user["utc_offset"],
		"verified": user["verified"]
		}

		return obj


	def has_id(self, id):
		"""

		"""
		return (id in self.inserted_ids)

#
#
#
#
#
class TextRegistryManager(object):
	"""

	"""

	def __init__(self, cursor):
		"""

		"""
		self.cursor = cursor
		self.registry = {}


	def add(self, key, obj):
		"""

		"""
		if not key:
			print "attempt to add"
			return

		real_key = key.lower()

		if real_key in self.registry:
			return self.registry[real_key]['id']
		else:
			id = self.do_insert(obj)
			obj['id'] = id

			self.registry[real_key] = obj
			return id


	def do_insert(self, obj):
		"""
		"""
		raise Exception("Unimplemented do_insert command")


	def get_id(self, key):
		key = key.lower()
		if key in self.registry:
			return self.registry[key]

		return None


#
#
#
#
#
class HashtagManager(TextRegistryManager):
	"""

	"""

	def __init__(self, cursor):
		super(HashtagManager, self).__init__(cursor)

	def do_insert(self, obj):
		#print "%s - %s"%(INSERT_HASHTAG_STMT, obj)
		self.cursor.execute(INSERT_HASHTAG_STMT, obj)
		return self.cursor.lastrowid



#
#
#
#
#
class UrlManager(TextRegistryManager):
	"""

	"""

	def __init__(self, cursor):
		super(UrlManager, self).__init__(cursor)


	def build_obj(self, obj):
		ret = {
			"url": obj["url"],
			"expanded_url": obj["expanded_url"],
			"display_url": obj["display_url"]
		}

	def do_insert(self, obj):
		self.cursor.execute(INSERT_URL_STMT, obj)
		return self.cursor.lastrowid



#
#
#
#
#
class MediaManager(TextRegistryManager):
	"""
	"""

	def __init__(self, cursor):
		super(MediaManager, self).__init__(cursor)


	def build_obj(self, obj):
		ret = {
			"type": obj["type"],
			"media_id": obj["id"],
			"source_status_id": obj["source_status_id"] if "source_status_id" in obj else None,
			"expanded_url": obj["expanded_url"],
			"display_url": obj["display_url"],
			"media_url": obj["media_url"]
		}

		return ret

	def do_insert(self, obj):
		media_obj = self.build_obj(obj)
		self.cursor.execute(INSERT_MEDIA_STMT, media_obj)
		return self.cursor.lastrowid		

