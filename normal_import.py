#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import simplejson as json
import io
from datetime import datetime
from pprint import pprint
import os
import sys
import argparse
import getpass

from mysql_insert_queries import *


from helpers import UserManager, HashtagManager, UrlManager, MediaManager, convertRFC822ToDateTime, MySQLBatchInserter



class StatusUpdater(object):

	def __init__(self, update_time = 5, count = 0, current_val = 0, total_val = 0, total_added = 0):
		self.update_time = update_time
		self.last_display_time = datetime.now()
		self.count = count
		self.current_val = current_val
		self.total_val = total_val
		self.total_added = 0

	def update(self, force=False):
		# update progress display if necessary
		cur_time = datetime.now()
		time_since_last_update = cur_time - self.last_display_time
		if force or time_since_last_update.total_seconds() > self.update_time:
			self.last_display_time = cur_time
			progress = self.current_val * 100.0 / self.total_val
			print "parsed %d tweets (%2.2f%% finished). %d added."%(self.count, progress, self.total_added)





class MySQLInserter(object):
	"""

	"""

	def __init__(self, cursor):
		""" """
		self.user_mgr = UserManager(cursor)
		self.hashtag_mgr = HashtagManager(cursor)
		self.media_mgr = MediaManager(cursor)
		self.url_mgr = UrlManager(cursor)

		self.status_updater = StatusUpdater()

		self.cursor = cursor

		self.file = None
		self.filesize = 0

		self.processed_tweets = set()

		# batch updaters
		self.tweet_snapshot_batch_inserter = MySQLBatchInserter(self.cursor, INSERT_TWEET_SNAPSHOT_STMT)
		self.tweet_retweet_snapshot_batch_inserter = MySQLBatchInserter(self.cursor, INSERT_TWEET_SNAPSHOT_WITH_RETWEET_STMT)

		# entity batch inserters
		self.tweet_mention_batch_inserter = MySQLBatchInserter(self.cursor, INSERT_MENTION_STMT)
		self.tweet_hashtag_batch_inserter = MySQLBatchInserter(self.cursor, INSERT_TWEET_HAHSTAG_STMT)
		self.tweet_url_batch_inserter = MySQLBatchInserter(self.cursor, INSERT_TWEET_URL_STMT)
		self.tweet_media_batch_inserter = MySQLBatchInserter(self.cursor, INSERT_TWEET_MEDIA_STMT)



	def __del__(self):
		""" """
		self.close()

	def getFileSize(self):
		""" """
		self.file.seek(0, os.SEEK_END)
		self.filesize = self.file.tell()
		self.file.seek(0, os.SEEK_SET)

		return self.filesize

	def close(self):
		""" """
		if self.file is not None:
			self.file.close()

	def open(self, filename, **kwargs):
		""" """
		self.close()
		self.file = io.open(args.filename, **kwargs)

		# store file descriptor number for better, but less accurate tell function
		# io.tell on a text file is painfully slow when not in binary mode
		self.filedescr = self.file.fileno()

		self.status_updater.total_val = self.getFileSize()

	def readLine(self):
		# grab the line
		line = self.file.readline()

		# update the status
		#self.status_updater.current_val = self.file.tell()

		return line


	def processLine(self, line):
		# clean line
		l = line.strip()

		# should be no empty lines, but just in case!
		if not l:
			return None

		# make a tweet dictionary from json object
		tweet = json.loads(l)

		# gnip data has status messages
		if "info" in tweet:
			return None

		# process the tweets from it
		self.processTweetSnapshot(tweet)


		# update the status
		#self.status_updater.current_val = self.file.tell()  OMG so slow
		self.status_updater.current_val = os.lseek(self.file.fileno(), 0, os.SEEK_CUR)

		return line


	def processFile(self, filename, **kwargs):
		"""

		"""
		self.open(filename,**kwargs)

		for line in self.file:
			line = self.processLine(line)

			# skip bad lines
			if line is None:
				continue

			# update status updater
			self.status_updater.count += 1
			self.status_updater.update()

			# do we need to bail?
			if args.limit > 0 and self.status_updater.count > args.limit:
				break

		# flush the batches
		self.tweet_snapshot_batch_inserter.flush()
		self.tweet_retweet_snapshot_batch_inserter.flush()

		self.tweet_mention_batch_inserter.flush()
		self.tweet_hashtag_batch_inserter.flush()
		self.tweet_url_batch_inserter.flush()
		self.tweet_media_batch_inserter.flush()

		# update status for user
		self.status_updater.update(True)

		# populate tweets table
		print "\npopulating tweets table..."
		print "(No progress available. Could take minutes.)"
		self.insert_tweets_from_snapshots()

		print "\npopulating users table..."
		print "(No progress available. Could take minutes.)"
		self.insert_users_from_snapshots()


	def processTweetSnapshot(self, tweet, snapshot_id = None, snapshot_time = None):
		"""

		"""
		tweet_id = tweet["id"]

		# parse the datetimes
		created_ts = convertRFC822ToDateTime(tweet['created_at'])
		tweet['created_ts'] = created_ts
		tweet['user']['created_ts'] = convertRFC822ToDateTime(tweet['user']['created_at'])

		tweet['snapshot_tweet_id'] = snapshot_id if snapshot_id is not None else tweet_id
		tweet['snapshot_time'] = snapshot_time if snapshot_time is not None else created_ts

		# add user
		#self.user_mgr.add(tweet)

		# add retweet if one exists
		if 'retweeted_status' in tweet:
			retweet = tweet['retweeted_status']
			retweet['created_ts'] = convertRFC822ToDateTime(retweet['created_at'])
			retweet['user']['created_ts'] = convertRFC822ToDateTime(retweet['user']['created_at'])
			self.processTweetSnapshot(retweet, tweet_id, created_ts)


		# add tweet
		#cnt = 0
		cnt = self.insert_snapshot(tweet)


		if tweet_id  not in self.processed_tweets:
			self.processed_tweets.add(tweet_id)

			# add entities
			#cnt = 1 # temporary
			self.addEntities(tweet, tweet_id)

		# update total added 
		self.status_updater.total_added += cnt


	def processTweet(self, tweet):
		"""

		"""
		tweet_id = tweet["id"]

		# parse the datetimes
		tweet['created_ts'] = convertRFC822ToDateTime(tweet['created_at'])
		tweet['user']['created_ts'] = convertRFC822ToDateTime(tweet['user']['created_at'])


		# add user
		self.user_mgr.add(tweet)

		# add retweet if one exists
		if 'retweeted_status' in tweet:
			retweet = tweet['retweeted_status']
			retweet['created_ts'] = convertRFC822ToDateTime(retweet['created_at'])
			retweet['user']['created_ts'] = convertRFC822ToDateTime(retweet['user']['created_at'])
			self.processTweet(retweet)


		# add tweet
		self.insert_tweet(tweet)

		# add all the entity data
		self.addEntities(tweet, tweet_id)

		# update total added 
		self.status_updater.total_added += 1





	def addEntities(self, tweet, tweet_id):
		entities = tweet["entities"]

		# add mentions
		self.addMentions(tweet_id, entities)

		# add hashtags
		self.addHashtags(tweet_id, entities)

		# add media
		self.addMedia(tweet_id, entities)

		# urls
		self.addUrls(tweet_id, entities)


	def addMentions(self, tweet_id, entities):
		""" 
		"""
		mentions = entities["user_mentions"]
		for idx in range(len(mentions)):
			m = mentions[idx]


			screen_name = m["screen_name"]
			mention_user_id = m["id"]

			# this is an awkward edge case, where we have to add an empty user if there's a mention of him, 
			# but he doesn't have a entry yet
 			if self.user_mgr.has_id(mention_user_id) == False:
 				#print "adding empty user %s (%d)"%(screen_name, mention_user_id)
 				self.user_mgr.add_empty(mention_user_id, screen_name)

			m_obj = {
				"tweet_id": tweet_id,
				"user_id": mention_user_id,
				"tweet_index": idx
			}

			try:
				#self.cursor.execute(INSERT_MENTION_STMT, m_obj)
				self.tweet_mention_batch_inserter.insert(m_obj)
			except Exception, e:
				print "Exception: ", e
				print "SQL: ", INSERT_MENTION_STMT
				print "tweet_id: ", tweet_id
				print "obj: ", m_obj
				raise e


	def addHashtags(self, tweet_id, entities):
		"""
		"""
		hashtags = entities["hashtags"]
		for n in range(len(hashtags)):
			ht = hashtags[n]["text"].lower()

			# insert it
			ht_id = self.hashtag_mgr.add(ht, { u"text": ht })

			obj = { "tweet_id": tweet_id, "hashtag_id": ht_id }
			#self.cursor.execute(INSERT_TWEET_HAHSTAG_STMT, obj)
			self.tweet_hashtag_batch_inserter.insert(obj)



	def addMedia(self, tweet_id, entities):
		if "media" in entities:
			media = entities["media"]
			for n in range(len(media)):
				m = media[n]

				media_id = self.media_mgr.add(m["media_url"],m)


				# insert relation
				obj = { "tweet_id": tweet_id, "media_id": media_id }
				#self.cursor.execute(INSERT_TWEET_MEDIA_STMT, obj)
				self.tweet_media_batch_inserter.insert(obj)

		
	def addUrls(self, tweet_id, entities):
		if "urls" in entities:
			urls = entities["urls"]

			for n in range(len(urls)):
				u = urls[n]

				url_id = self.url_mgr.add(u["url"], u)

				# insert relation
				obj = { "tweet_id": tweet_id, "url_id": url_id }
				#self.cursor.execute(INSERT_TWEET_URL_STMT, obj)
				self.tweet_url_batch_inserter.insert(obj)



	def insert_tweet(self, tweet):
		""" 

		"""
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
			stmt = REPLACE_TWEET_WITH_RETWEET_STMT
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
			stmt = REPLACE_TWEET_STMT
			retweet = {
			}


		obj.update(geo)
		obj.update(retweet)

		#pprint(obj)

		try:
			self.cursor.execute(stmt, obj)
		except Exception, e:
			print "Exception: ", e
			print "SQL: ", stmt
			print "obj: ", repr(obj)
			raise e


	def insert_snapshot(self, tweet):
		""" 

		"""
		user = tweet["user"]

		obj = {
			"snapshot_tweet_id": tweet["snapshot_tweet_id"],
			"snapshot_time": tweet["snapshot_time"],
			"tweet_id": tweet["id"],
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
			"user_description": user["description"],
			"user_location": user["location"],
			"user_created_at": user["created_at"],
			"user_created_ts": user["created_ts"],
			"user_lang": user["lang"],
			"user_listed_count": user["listed_count"],
			"user_name": user["name"],
			"user_url": user["url"],
			"user_utc_offset": user["utc_offset"],
			"user_verified": user["verified"],
			"source": tweet["source"],
			"in_reply_to_screen_name": tweet["in_reply_to_screen_name"],
			"in_reply_to_status_id": tweet["in_reply_to_status_id"],
			"in_reply_to_user_id": tweet["in_reply_to_user_id"],
			"retweet_count": tweet["retweet_count"],
			"favorite_count": tweet["favorite_count"]
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
			batch = self.tweet_retweet_snapshot_batch_inserter
			#stmt = INSERT_TWEET_SNAPSHOT_WITH_RETWEET_STMT
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
			batch = self.tweet_snapshot_batch_inserter
			#stmt = INSERT_TWEET_SNAPSHOT_STMT
			retweet = {
			}


		obj.update(geo)
		obj.update(retweet)

		#pprint(obj)

		try:
			#print obj["user_created_ts"], obj["user_created_ts"].microsecond, obj["user_created_ts"].tzinfo
			#sys.stdout.flush()
			#self.cursor.execute(stmt, obj)
			#return 1
			return batch.insert(obj)
		except Exception, e:
			print "Exception: ", e
			#print "SQL: ", stmt
			print "obj: ", repr(obj)
			raise e


	def exec_statement(self, stmt):
		try:
			self.cursor.execute(stmt)
		except Exception, e:
			print "Exception: ", e
			#print "SQL: ", stmt
			#print "obj: ", repr(obj)
			raise e				


	def insert_tweets_from_snapshots(self):
		"""
		Runs a query after snapshots have been added to generate actual tweets table content using the
		most recent tweet as deteremined by the snapshot tweet_id. 

		Twitter claims that the ids are k-sorted and they would try to keep them roughly in order within a second,
		however that was in 2010 and in 2014 they retired their snowflake codebase on github, so it's unclear how it's
		working

		https://blog.twitter.com/2010/announcing-snowflake

		https://github.com/twitter/snowflake/blob/742afd7d02adcfdafa9fd6a2844de087891fe1a2/README.md
		"""
		self.exec_statement(INSERT_TWEETS_FROM_SNAPSHOTS_STMT)


	def insert_users_from_snapshots(self):
		"""
		runs a query after snapshots have been added to generate the user table content using the
		most recent tweet as determined by the snapshot tweet_id. See note in the insert_tweets_from_snapshots
		about this. 
		"""

		self.exec_statement(INSERT_USERS_FROM_SNAPSHOTS_STMT)





#
#
# program arguments
#
#
parser = argparse.ArgumentParser(description='whatevs')
parser.add_argument('host', help='host')
parser.add_argument('database', help='database name')
parser.add_argument('username', help="username")
parser.add_argument('-l', '--limit', help="limit", type=int, default=0)
#parser.add_argument('-o', '--output', help="outfile")
parser.add_argument('-f', '--filename', help="input file")
parser.add_argument('-e', '--encoding', default="utf-8", help="json file encoding (default is utf-8)")
parser.add_argument('--db-encoding', default="utf8mb4", help="database encoding")
#parser.add_argument('-b', '--batchsize', default=1000, type=int, help="batch insert size")
parser.add_argument('-c', '--check', dest="check", action="store_true", help="check if tweet exists before inserting")
parser.add_argument('-r', '--no_retweets', dest="no_retweets", action="store_true", help="do not add embedded retweets")
parser.add_argument('-p', '--password', help="password for database. if not specified, will prompt.")
args = parser.parse_args()


if args.password is None:
	password = getpass.getpass("Enter password for %s@%s (%s) : "%(args.username, args.host, args.database))
else:
	password = args.password



db=MySQLdb.connect(args.host, args.username, password, args.database, charset='utf8mb4', use_unicode=True)



c=db.cursor()



inserter = MySQLInserter(c)

inserter.processFile(args.filename, encoding=args.encoding)

print "Finished and committing..."

c.close()

db.commit()
db.close()

quit()


with io.open(args.filename, encoding='utf-8') as f:
	insert_cnt = 0

	user_mgr = UserManager(c)
	hashtag_mgr = HashtagManager(c)
	media_mgr = MediaManager(c)
	url_mgr = UrlManager(c)

	last_update = datetime.now()

	f.seek(0, os.SEEK_END)
	filesize = f.tell()
	f.seek(0, os.SEEK_SET)

	for line in f:
		l = line.strip()
		if not l:
			continue
		#print json.loads(l)
		tweet = json.loads(l)

		if "info" in tweet:
			continue

		tweet_id = tweet["id"]

		# parse the datetimes
		tweet['created_ts'] = convertRFC822ToDateTime(tweet['created_at'])
		tweet['user']['created_ts'] = convertRFC822ToDateTime(tweet['user']['created_at'])
		if 'retweeted_status' in tweet:
			tweet['retweeted_status']['created_ts'] = convertRFC822ToDateTime(tweet['retweeted_status']['created_at'])
			tweet['retweeted_status']['user']['created_ts'] = convertRFC822ToDateTime(tweet['retweeted_status']['user']['created_at'])



		insert_cnt += 1

		#c.execute(INSERT_STMT, tweet)

		# add user
		user_mgr.add(tweet)



		# add tweet
		insert_tweet(tweet, c)


		entities = tweet["entities"]

		# add mentions
		mentions = entities["user_mentions"]
		for idx in range(len(mentions)):
			m = mentions[idx]


			screen_name = m["screen_name"]
			mention_user_id = m["id"]
 			#if user_mgr.has_id(mention_user_id) == False:
 				#print "adding empty user %s (%d)"%(screen_name, mention_user_id)
 			#	user_mgr.add_empty(mention_user_id, screen_name)

			m_obj = {
				"tweet_id": tweet_id,
				"user_id": mention_user_id,
				"tweet_index": idx
			}

			c.execute(INSERT_MENTION_STMT, m_obj)

		# hashtags
		hashtags = entities["hashtags"]
		for n in range(len(hashtags)):
			ht = hashtags[n]["text"].lower()

			# insert it
			ht_id = hashtag_mgr.add(ht, { u"text": ht })

			c.execute(INSERT_TWEET_HAHSTAG_STMT, { "tweet_id": tweet_id, "hashtag_id": ht_id })


		# media
		if "media" in entities:
			media = entities["media"]
			for n in range(len(media)):
				m = media[n]

				media_id = media_mgr.add(m["media_url"],m)


				# insert relation
				c.execute(INSERT_TWEET_MEDIA_STMT, { "tweet_id": tweet_id, "media_id": media_id })

		# urls
		if "urls" in entities:
			urls = entities["urls"]

			for n in range(len(urls)):
				u = urls[n]

				url_id = url_mgr.add(u["url"], u)

				# insert relation
				try:
					c.execute(INSERT_TWEET_URL_STMT, { "tweet_id": tweet_id, "url_id": url_id })
				except Exception, e:
					print "Exception : ", e
					print "tweet_id: ", tweet_id
					print "url_id: ", url_id



		dt = datetime.now()
		diff = dt - last_update

		if diff.total_seconds() > 10:
			#done = (f.tell() *  100) / filesize
			print "%d tweets"%(insert_cnt)
			last_update = dt


		if args.limit > 0 and insert_cnt > args.limit:
			break

	c.close()

db.commit()
db.close()

