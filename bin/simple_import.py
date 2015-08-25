import MySQLdb
import csv
import cStringIO
import codecs
import pprint
from datetime import datetime
from decimal import *


class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")



class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self






INSERT_STMT="""INSERT INTO `tweets_Oso`
(`created_at`,
`lang`,
`text`,
`uuid`,
`user_id`,
`geo_coordinates_0`,
`geo_coordinates_1`,
`user_screen_name`,
`user_description`,
`user_followers_count`,
`user_friends_count`,
`user_location`,
`entities_urls_0_expanded_url`,
`entities_urls_1_expanded_url`,
`entities_urls_2_expanded_url`,
`user_statuses_count`,
`entities_urls_0_display_url`,
`entities_urls_1_display_url`,
`entities_urls_2_display_url`,
`retweeted_status_id`,
`retweeted_status_user_screen_name`,
`retweeted_status_retweet_count`,
`retweeted_status_created_at`,
`retweeted_status_text`,
`retweeted_status_favorite_count`,
`retweeted_status_user_id`,
`retweeted_status_user_time_zone`,
`retweeted_status_user_friends_count`,
`retweeted_status_user_statuses_count`,
`retweeted_status_user_followers_count`,
`in_reply_to_screen_name`,
`in_reply_to_status_id`,
`in_reply_to_user_id`)
VALUES
(%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s)
"""


parser = argparse.ArgumentParser(description='whatevs')
parser.add_argument('host', help='host')
parser.add_argument('database', help='database name')
parser.add_argument('username', help="username")
parser.add_argument('-l', '--limit', help="limit", type=int, default=0)
#parser.add_argument('-o', '--output', help="outfile")
parser.add_argument('-f', '--filename', help="input file")
parser.add_argument('-e', '--encoding', default="utf-8", help="json file encoding (default is utf-8)")
parser.add_argument('--db_encoding', default="utf8mb4", help="database encoding")
#parser.add_argument('-b', '--batchsize', default=1000, type=int, help="batch insert size")
parser.add_argument('-c', '--check', dest="check", action="store_true", help="check if tweet exists before inserting")
parser.add_argument('-r', '--no_retweets', dest="no_retweets", action="store_true", help="do not add embedded retweets")
args = parser.parse_args()


# ask for password
password = getpass.getpass("Enter password for %s@%s (%s) : "%(args.username, args.host, args.database))

# connect to db
db=MySQLdb.connect(args.host, args.username, password, args.database, charset=args.db_encoding, use_unicode=True)



c=db.cursor()
with open(args.filename, 'r') as infile:
	coder = codecs.iterencode(codecs.iterdecode(infile, "utf-8"), "utf-8")
	csvreader = csv.DictReader(coder, delimiter=',', quotechar='"')

	queue = []
	total = 0
	try:

		last_item = {}

		for row in csvreader:
			
			#print "%d - %s,%s,%s,%s"%(total, row["created_ts"], row["text"], row["retweeted_status.created_ts"], row["retweeted_status.text"])
			last_item = row

			created_ts = datetime.strptime( row["created_ts"], "%Y-%m-%dT%H:%M:%SZ" )
			retweet_created = datetime.strptime( row["retweeted_status.created_ts"], "%Y-%m-%dT%H:%M:%SZ" ) if row["retweeted_status.created_ts"] else None

			geo_0 = Decimal(row["geo.coordinates.0"] if len(row["geo.coordinates.0"]) < 16 else row["geo.coordinates.0"][:16]) if row["geo.coordinates.0"] else None
			geo_1 = Decimal(Decimal(row["geo.coordinates.1"] if len(row["geo.coordinates.1"]) < 16 else row["geo.coordinates.1"][:16])) if row["geo.coordinates.1"] else None

			#if geo_0 is not None:
			#	print geo_0, geo_1

			item = (
				created_ts,
				row["lang"],
				row["text"],
				int(row["id"]),
				int(row["user.id"]),
				geo_0,
				geo_1,
				row["user.screen_name"],
				row["user.description"],
				int(row["user.followers_count"]),
				int(row["user.friends_count"]),
				row["user.location"],
				row["entities.urls.0.expanded_url"],
				row["entities.urls.1.expanded_url"],
				row["entities.urls.2.expanded_url"],
				int(row["user.statuses_count"]),
				row["entities.urls.0.display_url"],
				row["entities.urls.1.display_url"],
				row["entities.urls.2.display_url"],
				int(row["retweeted_status.id"]) if row["retweeted_status.id"] else None,
				row["retweeted_status.user.screen_name"] if row["retweeted_status.user.screen_name"] else None,
				int(row["retweeted_status.retweet_count"]) if row["retweeted_status.retweet_count"] else None,
				retweet_created,
				row["retweeted_status.text"] if row["retweeted_status.text"] else None,
				int(row["retweeted_status.favorite_count"]) if row["retweeted_status.favorite_count"] else None,
				int(row["retweeted_status.user.id"]) if row["retweeted_status.user.id"] else None,
				row["retweeted_status.user.time_zone"] if row["retweeted_status.user.time_zone"] else None,
				int(row["retweeted_status.user.friends_count"]) if row["retweeted_status.user.friends_count"] else None,
				int(row["retweeted_status.user.statuses_count"]) if row["retweeted_status.user.statuses_count"] else None,
				int(row["retweeted_status.user.followers_count"]) if row["retweeted_status.user.followers_count"] else None,
				row["in_reply_to_screen_name"] if row["in_reply_to_screen_name"] else None,
				int(row["in_reply_to_status_id"]) if row["in_reply_to_status_id"] else None,
				int(row["in_reply_to_user_id"]) if row["in_reply_to_user_id"] else None
				)
			queue.append(item)
			total += 1
			if len(queue) >= MAX_NUM:
				#print
				#print "---------------------"
				#print 
				c.executemany(INSERT_STMT, queue)
				queue = []
				print total
				#print "---------------------"
				#print

		# insert the last few
		c.executemany(INSERT_STMT, queue)
		print "%d total inserted"%(total)

		c.close()

	except Exception, e:
		print "error ", e
		print "last item: "
		pprint.pprint(last_item)
		c.close()
		db.close()
		raise e

	finally:
		c.close()

db.commit()
db.close()
