#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import simplejson as json
import io
import email.utils
from datetime import datetime
from pprint import pprint
import os
import argparse
import getpass

from mysql_insert_queries import *
from helpers import *



#
# convert an RFC822 date to a datetime
# borrowed and modified from: https://gist.github.com/robertklep/2928188
#
# original used fromtimestamp instead of utcfromtimestamp, which converts it to local time.
# currently, all of the tweets seem to just use utc, so we can ignore the timestamp (though
# it's unclear if mktime_tz actually utilizes the info or just ignores it. )
#
def convertRFC822ToDateTime(rfc822string):
	"""
		convert an RFC822 date to a datetime
	"""
	return datetime.utcfromtimestamp(email.utils.mktime_tz(email.utils.parsedate_tz(rfc822string)))


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
args = parser.parse_args()



password = getpass.getpass("Enter password for %s@%s (%s) : "%(args.username, args.host, args.database))



db=MySQLdb.connect(args.host, args.username, password, args.database, charset='utf8mb4', use_unicode=True)



c=db.cursor()

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


		# add tweet
		insert_tweet(tweet, c)


		# add user
		user_mgr.add(tweet)

		entities = tweet["entities"]

		# add mentions
		mentions = entities["user_mentions"]
		for idx in range(len(mentions)):
			m = mentions[idx]


			screen_name = m["screen_name"]
			mention_user_id = m["id"]
 			if user_mgr.has_id(mention_user_id) == False:
 				#print "adding empty user %s (%d)"%(screen_name, mention_user_id)
 				user_mgr.add_empty(mention_user_id, screen_name)

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
				c.execute(INSERT_TWEET_URL_STMT, { "tweet_id": tweet_id, "url_id": url_id })



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

