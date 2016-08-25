import MySQLdb
import json
import codecs
import pprint
from datetime import datetime
from decimal import *



INSERT_STMT="""INSERT INTO `tweets`
(
  `id`,

  `created_at`,
  `created_ts`,
  `lang`,
  `text`,
  `geo_coordinates_0`,
  `geo_coordinates_1`,

  `contributors`,
  `counts`,
  `entities`,
  `filter_level`,
  `coordinates`,
  `place`,
  `possibly_sensitive`,


  `user`,
  `user_id`,
  `user_screen_name`,
  `user_followers_count`,
  `user_friends_count`,
  `user_statuses_count`,
  `user_favourites_count`,
  `user_geo_enabled`,
  `user_time_zone`,
  `user_description`,
  `user_location`,
  `user_created_at`,
  `user_created_ts`,
  `user_lang`,
  `user_listed_count`,
  `user_name`,
  `user_url`,
  `user_utc_offset`,
  `user_verified`,

  `user_profile_use_background_image`,
  `user_default_profile_image`,
  `user_profile_sidebar_fill_color`,
  `user_profile_text_color`,
  `user_profile_sidebar_border_color`,
  `user_profile_background_color`,
  `user_profile_link_color`,
  `user_profile_image_url`,
  `user_profile_banner_url`,
  `user_profile_background_image_url`,
  `user_profile_background_tile`,
  `user_contributors_enabled`,
  `user_default_profile`,
  `user_is_translator`,

  `retweet_count`,
  `favorite_count`,
  `retweeted_status`,
  `retweeted_status_id`,
  `retweeted_status_user_screen_name`,
  `retweeted_status_retweet_count`,
  `retweeted_status_user_id`,
  `retweeted_status_user_time_zone`,
  `retweeted_status_user_friends_count`,
  `retweeted_status_user_statuses_count`,
  `retweeted_status_user_followers_count`,
  `source`,
  `in_reply_to_screen_name`,
  `in_reply_to_status_id`,
  `in_reply_to_user_id`,

  `quoted_status_id`,
  `quoted_status`,

  `truncated`,

  `local_time`,

  `rumor`,
  `codes_first`,
  `codes_uncertainty`,
  `codes_implicit`,
  `codes_ambiguity`)
VALUES
( %s,
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
  %s,
  %s,
  %s,
  %s,
  %s,
  %s,
  %s,
  %s)
"""


def get_nested_value(_dict, path, default=None):
    """ gets value from a nested value """
    # step through each path and try to process it
    parts = path.split(".")
    num_parts = len(parts)
    cur_dict = _dict

    # step through each part of the path
    try:
        for i in range(0, num_parts - 1):
            part = parts[i]
            if part[0] >= ord('0') and part[0] <= ord('9'):
                try:
                    part = int(part)
                except ValueError:
                    pass
            cur_dict = cur_dict[part]

        return cur_dict[parts[num_parts - 1]]
    except KeyError:
        pass

    return default


def get_nested_value_json(_dict, path, default=None):
    value = get_nested_value(_dict, path, default)
    if value is not None:
        return json.dumps(value)
    return value


parser = argparse.ArgumentParser(description='journalist sql importer')
parser.add_argument('host', help='host')
parser.add_argument('database', help='database name')
parser.add_argument('username', help="username")
parser.add_argument('rumor', help="rumor")
parser.add_argument('-l', '--limit', help="limit", type=int, default=0)
parser.add_argument('-f', '--filename', help="input file")
parser.add_argument(
    '-e',
    '--encoding',
    default="utf-8", help="json file encoding (default is utf-8)")
parser.add_argument(
    '--db_encoding',
    default="utf8mb4", help="database encoding")
#parser.add_argument('-b', '--batchsize', default=1000, type=int, help="batch insert size")
parser.add_argument(
    '-c',
    '--check',
    dest="check",
    action="store_true",
    help="check if tweet exists before inserting")
parser.add_argument(
    '-r',
    '--no_retweets',
    dest="no_retweets",
    action="store_true",
    help="do not add embedded retweets")
args = parser.parse_args()


# ask for password
password = getpass.getpass(
    "Enter password for %s@%s (%s) : " % (
        args.username,
        args.host,
        args.database))

# connect to db
db = MySQLdb.connect(
    args.host, args.username, password,
    args.database, charset=args.db_encoding, use_unicode=True)


c = db.cursor()
with open(args.filename, 'r') as infile:
    queue = []
    total = 0
    try:
        last_item = {}

        for line in infile:
            if not line or len(line) < 1:
                continue
            tweet = json.loads(line)


            last_item = tweet

            created_ts = datetime.strptime(
                tweet["created_ts"], "%Y-%m-%dT%H:%M:%SZ")
            user_created_ts = datetime.strptime(
                get_nested_value(tweet, "user.created_ts"))
            rsct = get_nested_value(tweet, "retweeted_status.created_ts")
            retweet_created = datetime.strptime(
                rsct, "%Y-%m-%dT%H:%M:%SZ") if rsct else None


            geo_0 = Decimal(get_nested_value(tweet, "coordinates.0"))
            geo_1 = Decimal(get_nested_value(tweet, "coordinates.1"))

            second_codes = set(get_nested_value(tweet, "codes.0.second_code"))

            #if geo_0 is not None:
            #   print geo_0, geo_1

            item = (
                tweet["id"],
                tweet["created_at"],
                created_ts,
                get_nested_value(tweet, "lang"),
                get_nested_value(tweet, "text"),
                geo_0,
                geo_1,
                get_nested_value_json(tweet, "contributors"),
                get_nested_value_json(tweet, "counts"),
                get_nested_value_json(tweet, "entities"),
                get_nested_value(tweet, "filter_level"),
                get_nested_value_json(tweet, "coordinates"),
                get_nested_value_json(tweet, "place"),
                get_nested_value(tweet, "possibly_sensitive"),
                get_nested_value_json(tweet, "user"),
                get_nested_value(tweet, "user.id"),
                get_nested_value(tweet, "user.screen_name"),
                get_nested_value(tweet, "user.followers_count"),
                get_nested_value(tweet, "user.friends_count"),
                get_nested_value(tweet, "user.statuses_count"),
                get_nested_value(tweet, "user.favourites_count"),
                get_nested_value(tweet, "user.geo_enabled"),
                get_nested_value(tweet, "user.time_zone"),
                get_nested_value(tweet, "user.description"),
                get_nested_value(tweet, "user.location"),
                get_nested_value(tweet, "user.created_at"),
                user_created_ts,
                get_nested_value(tweet, "user.lang"),
                get_nested_value(tweet, "user.listed_count"),
                get_nested_value(tweet, "user.name"),
                get_nested_value(tweet, "user.url"),
                get_nested_value(tweet, "user.utc_offset"),
                get_nested_value(tweet, "user.verified"),
                get_nested_value(tweet, "user.profile_use_background_image"),
                get_nested_value(tweet, "user.default_profile_image"),
                get_nested_value(tweet, "user.profile_sidebar_fill_color"),
                get_nested_value(tweet, "user.profile_text_color"),
                get_nested_value(tweet, "user.profile_sidebar_border_color"),
                get_nested_value(tweet, "user.profile_background_color"),
                get_nested_value(tweet, "user.profile_link_color"),
                get_nested_value(tweet, "user.profile_image_url"),
                get_nested_value(tweet, "user.profile_banner_url"),
                get_nested_value(tweet, "user.profile_background_image_url"),
                get_nested_value(tweet, "user.profile_background_tile"),
                get_nested_value(tweet, "user.contributors_enabled"),
                get_nested_value(tweet, "user.default_profile"),
                get_nested_value(tweet, "user.is_translator"),
                get_nested_value(tweet, "retweet_count"),
                get_nested_value(tweet, "favorite_count"),
                get_nested_value_json(tweet, "retweeted_status"),
                get_nested_value(tweet, "retweeted_status.id"),
                get_nested_value(tweet, "retweeted_status.user.screen_name"),
                get_nested_value(tweet, "retweeted_status.retweet_count"),
                get_nested_value(tweet, "retweeted_status.user.id"),
                get_nested_value(tweet, "retweeted_status.user.time_zone"),
                get_nested_value(tweet, "retweeted_status.user.friends_count"),
                get_nested_value(tweet, "retweeted_status.user.statuses_count"),
                get_nested_value(tweet, "retweeted_status.user.followers_count"),
                get_nested_value(tweet, "source"),
                get_nested_value(tweet, "in_reply_to_screen_name"),
                get_nested_value(tweet, "in_reply_to_status_id"),
                get_nested_value(tweet, "in_reply_to_user_id"),
                get_nested_value(tweet, "quoted_status_id"),
                get_nested_value_json(tweet, "quoted_status"),
                get_nested_value(tweet, "truncated"),
                None,
                args.rumor,
                get_nested_value(tweet, "codes.0.first_code"),
                "Uncertainty" in second_codes,
                "Implicit" in second_codes,
                "Ambiguity" in second_codes
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
