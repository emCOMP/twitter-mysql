#!/usr/bin/env python
# -*- coding: utf-8 -*-

TWEET_BASE_STMT = """ INTO `tweets`
(`id`,
`created_at`,
`created_ts`,
`lang`,
`text`,
`geo_coordinates_0`,
`geo_coordinates_1`,
`user_id`,
`user_screen_name`,
`user_followers_count`,
`user_friends_count`,
`user_statuses_count`,
`user_favourites_count`,
`user_geo_enabled`,
`source`,
`in_reply_to_screen_name`,
`in_reply_to_status_id`,
`retweet_source_id`,
`in_reply_to_user_id`)
VALUES
(%(id)s,
%(created_at)s,
%(created_ts)s,
%(lang)s,
%(text)s,
%(geo_coordinates_0)s,
%(geo_coordinates_1)s,
%(user_id)s,
%(user_screen_name)s,
%(user_followers_count)s,
%(user_friends_count)s,
%(user_statuses_count)s,
%(user_favourites_count)s,
%(user_geo_enabled)s,
%(source)s,
%(in_reply_to_screen_name)s,
%(in_reply_to_status_id)s,
%(in_reply_to_user_id)s,
%(retweet_source_id)s)
"""

TWEET_WITH_RETWEET_BASE_STMT = """ INTO `tweets`
(`id`,
`created_at`,
`created_ts`,
`lang`,
`text`,
`geo_coordinates_0`,
`geo_coordinates_1`,
`user_id`,
`user_screen_name`,
`user_followers_count`,
`user_friends_count`,
`user_statuses_count`,
`user_favourites_count`,
`user_geo_enabled`,
`user_time_zone`,
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
`retweet_source_id`)
VALUES
(%(id)s,
%(created_at)s,
%(created_ts)s,
%(lang)s,
%(text)s,
%(geo_coordinates_0)s,
%(geo_coordinates_1)s,
%(user_id)s,
%(user_screen_name)s,
%(user_followers_count)s,
%(user_friends_count)s,
%(user_statuses_count)s,
%(user_favourites_count)s,
%(user_geo_enabled)s,
%(user_time_zone)s,
%(retweeted_status_id)s,
%(retweeted_status_user_screen_name)s,
%(retweeted_status_retweet_count)s,
%(retweeted_status_user_id)s,
%(retweeted_status_user_time_zone)s,
%(retweeted_status_user_friends_count)s,
%(retweeted_status_user_statuses_count)s,
%(retweeted_status_user_followers_count)s,
%(source)s,
%(in_reply_to_screen_name)s,
%(in_reply_to_status_id)s,
%(in_reply_to_user_id)s,
%(retweet_source_id)s
)"""


INSERT_TWEET_STMT = "INSERT" + TWEET_BASE_STMT
INSERT_TWEET_WITH_RETWEET_STMT = "INSERT" + TWEET_WITH_RETWEET_BASE_STMT
REPLACE_TWEET_STMT = "REPLACE" + TWEET_BASE_STMT
REPLACE_TWEET_WITH_RETWEET_STMT = "REPLACE" + TWEET_WITH_RETWEET_BASE_STMT

TWEET_SNAPSHOT_BASE_STMT = """ INTO `tweet_snapshots`
(
`snapshot_tweet_id`,
`snapshot_time`,
`tweet_id`,
`created_at`,
`created_ts`,
`lang`,
`text`,
`geo_coordinates_0`,
`geo_coordinates_1`,
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
`retweet_count`,
`favorite_count`,
`source`,
`in_reply_to_screen_name`,
`in_reply_to_status_id`,
`in_reply_to_user_id`,
`retweet_source_id`)
VALUES
(
%(snapshot_tweet_id)s,
%(snapshot_time)s,
%(tweet_id)s,
%(created_at)s,
%(created_ts)s,
%(lang)s,
%(text)s,
%(geo_coordinates_0)s,
%(geo_coordinates_1)s,
%(user_id)s,
%(user_screen_name)s,
%(user_followers_count)s,
%(user_friends_count)s,
%(user_statuses_count)s,
%(user_favourites_count)s,
%(user_geo_enabled)s,
%(user_time_zone)s,
%(user_description)s,
%(user_location)s,
%(user_created_at)s,
%(user_created_ts)s,
%(user_lang)s,
%(user_listed_count)s,
%(user_name)s,
%(user_url)s,
%(user_utc_offset)s,
%(user_verified)s,
%(retweet_count)s,
%(favorite_count)s,
%(source)s,
%(in_reply_to_screen_name)s,
%(in_reply_to_status_id)s,
%(in_reply_to_user_id)s,
%(retweet_source_id)s
)"""


TWEET_SNAPSHOT_WITH_RETWEET_BASE_STMT = """ INTO `tweet_snapshots`
(
`snapshot_tweet_id`,
`snapshot_time`,
`tweet_id`,
`created_at`,
`created_ts`,
`lang`,
`text`,
`geo_coordinates_0`,
`geo_coordinates_1`,
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
`retweet_count`,
`favorite_count`,
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
`retweet_source_id`)
VALUES
(
%(snapshot_tweet_id)s,
%(snapshot_time)s,
%(tweet_id)s,
%(created_at)s,
%(created_ts)s,
%(lang)s,
%(text)s,
%(geo_coordinates_0)s,
%(geo_coordinates_1)s,
%(user_id)s,
%(user_screen_name)s,
%(user_followers_count)s,
%(user_friends_count)s,
%(user_statuses_count)s,
%(user_favourites_count)s,
%(user_geo_enabled)s,
%(user_time_zone)s,
%(user_description)s,
%(user_location)s,
%(user_created_at)s,
%(user_created_ts)s,
%(user_lang)s,
%(user_listed_count)s,
%(user_name)s,
%(user_url)s,
%(user_utc_offset)s,
%(user_verified)s,
%(retweet_count)s,
%(favorite_count)s,
%(retweeted_status_id)s,
%(retweeted_status_user_screen_name)s,
%(retweeted_status_retweet_count)s,
%(retweeted_status_user_id)s,
%(retweeted_status_user_time_zone)s,
%(retweeted_status_user_friends_count)s,
%(retweeted_status_user_statuses_count)s,
%(retweeted_status_user_followers_count)s,
%(source)s,
%(in_reply_to_screen_name)s,
%(in_reply_to_status_id)s,
%(in_reply_to_user_id)s,
%(retweet_source_id)s
)"""

INSERT_TWEET_SNAPSHOT_STMT = "INSERT" + TWEET_SNAPSHOT_BASE_STMT
INSERT_TWEET_SNAPSHOT_WITH_RETWEET_STMT = "INSERT" + TWEET_SNAPSHOT_WITH_RETWEET_BASE_STMT
REPLACE_TWEET_SNAPSHOT_STMT = "REPLACE" + TWEET_SNAPSHOT_BASE_STMT
REPLACE_TWEET_SNAPSHOT_WITH_RETWEET_STMT = "REPLACE" + TWEET_SNAPSHOT_WITH_RETWEET_BASE_STMT


USER_BASE_STMT = """ INTO `users` (
`id`, 
`screen_name`,
`description`,
`followers_count`,
`friends_count`,
`statuses_count`,
`favourites_count`,
`location`,
`created_at`,
`created_ts`,
`geo_enabled`,
`lang`,
`listed_count`,
`name`,
`time_zone`,
`url`,
`utc_offset`,
`verified`)
VALUES (
%(id)s, 
%(screen_name)s,
%(description)s,
%(followers_count)s,
%(friends_count)s,
%(statuses_count)s,
%(favourites_count)s,
%(location)s,
%(created_at)s,
%(created_ts)s,
%(geo_enabled)s,
%(lang)s,
%(listed_count)s,
%(name)s,
%(time_zone)s,
%(url)s,
%(utc_offset)s,
%(verified)s
)"""

INSERT_USER_STMT = "INSERT " + USER_BASE_STMT
REPLACE_USER_STMT = "REPLACE " + USER_BASE_STMT


REPLACE_USER_STMT = """REPLACE INTO `users` (
`id`, 
`screen_name`,
`description`,
`followers_count`,
`friends_count`,
`statuses_count`,
`favourites_count`,
`location`,
`created_at`,
`created_ts`,
`geo_enabled`,
`lang`,
`listed_count`,
`name`,
`time_zone`,
`url`,
`utc_offset`,
`verified`)
VALUES (
%(id)s, 
%(screen_name)s,
%(description)s,
%(followers_count)s,
%(friends_count)s,
%(statuses_count)s,
%(favourites_count)s,
%(location)s,
%(created_at)s,
%(created_ts)s,
%(geo_enabled)s,
%(lang)s,
%(listed_count)s,
%(name)s,
%(time_zone)s,
%(url)s,
%(utc_offset)s,
%(verified)s
)"""



INSERT_HASHTAG_STMT = """INSERT INTO `hashtags` (`text`) VALUES (%(text)s)"""



INSERT_MENTION_STMT = """INSERT INTO `tweet_mention` (
`tweet_id`,
`user_id`, 
`tweet_index`
) VALUES (
%(tweet_id)s,
%(user_id)s,
%(tweet_index)s
)
"""



INSERT_TWEET_HAHSTAG_STMT = """INSERT INTO `tweet_hashtag` (
`tweet_id`,
`hashtag_id`
) VALUES (
%(tweet_id)s,
%(hashtag_id)s
)
"""


INSERT_MEDIA_STMT = """INSERT INTO `media` (
`type`,
`media_id`,
`source_status_id`,
`expanded_url`,
`display_url`,
`media_url`
) VALUES (
%(type)s,
%(media_id)s,
%(source_status_id)s,
%(expanded_url)s,
%(display_url)s,
%(media_url)s
)
"""

INSERT_TWEET_MEDIA_STMT = """INSERT INTO `tweet_media` (
`tweet_id`,
`media_id`
) VALUES (
%(tweet_id)s,
%(media_id)s
)
"""



INSERT_URL_STMT = """INSERT INTO `urls` (`url`, `expanded_url`, `display_url`) VALUES (%(url)s, %(expanded_url)s, %(display_url)s ) """

INSERT_TWEET_URL_STMT = """INSERT INTO `tweet_url` (`tweet_id`, `url_id`) VALUES (%(tweet_id)s, %(url_id)s ) """



INSERT_TWEETS_FROM_SNAPSHOTS_STMT = """
INSERT INTO tweets (
`id`,
`created_at`,
`created_ts`,
`lang`,
`text`,
`geo_coordinates_0`,
`geo_coordinates_1`,
`user_id`,
`user_screen_name`,
`user_followers_count`,
`user_friends_count`,
`user_statuses_count`,
`user_favourites_count`,
`user_geo_enabled`,
`user_time_zone`,
`retweet_count`,
`favorite_count`,
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
`in_reply_to_user_id`)
select 
ts.tweet_id as id, 
ts.`created_at`,
ts.`created_ts`,
ts.`lang`,
ts.`text`,
ts.`geo_coordinates_0`,
ts.`geo_coordinates_1`,
ts.`user_id`,
ts.`user_screen_name`,
ts.`user_followers_count`,
ts.`user_friends_count`,
ts.`user_statuses_count`,
ts.`user_favourites_count`,
ts.`user_geo_enabled`,
ts.`user_time_zone`,
ts.`retweet_count`,
ts.`favorite_count`,
ts.`retweeted_status_id`,
ts.`retweeted_status_user_screen_name`,
ts.`retweeted_status_retweet_count`,
ts.`retweeted_status_user_id`,
ts.`retweeted_status_user_time_zone`,
ts.`retweeted_status_user_friends_count`,
ts.`retweeted_status_user_statuses_count`,
ts.`retweeted_status_user_followers_count`,
ts.`source`,
ts.`in_reply_to_screen_name`,
ts.`in_reply_to_status_id`,
ts.`in_reply_to_user_id`

from oso3.tweet_snapshots ts
inner join (select ts1.tweet_id, max(ts1.snapshot_tweet_id) as max_snapshot_tweet_id
	from oso3.tweet_snapshots ts1
	group by ts1.tweet_id) gts 
on gts.tweet_id = ts.tweet_id and gts.max_snapshot_tweet_id = ts.snapshot_tweet_id;
"""


INSERT_USERS_FROM_SNAPSHOTS_STMT = """
INSERT INTO users (
`id`, 
`screen_name`,
`description`,
`followers_count`,
`friends_count`,
`statuses_count`,
`favourites_count`,
`location`,
`created_at`,
`created_ts`,
`geo_enabled`,
`lang`,
`listed_count`,
`name`,
`time_zone`,
`url`,
`utc_offset`,
`verified`)
select 
ts.`user_id` as id, 
ts.`user_screen_name` as screen_name,
ts.`user_description` as description,
ts.`user_followers_count` as followers_count,
ts.`user_friends_count` as friends_count,
ts.`user_statuses_count` as statuses_count,
ts.`user_favourites_count` as favourites_count,
ts.`user_location` as location,
ts.`user_created_at` as created_at,
ts.`user_created_ts` as created_ts,
ts.`user_geo_enabled` as geo_enabled,
ts.`user_lang` as lang,
ts.`user_listed_count` as listed_count,
ts.`user_name` as name,
ts.`user_time_zone` as time_zone,
ts.`user_url` as url,
ts.`user_utc_offset` as utc_offset,
ts.`user_verified` as verified

from oso3.tweet_snapshots ts
inner join (select ts1.user_id, max(ts1.snapshot_tweet_id) as max_snapshot_tweet_id
	from oso3.tweet_snapshots ts1
	group by ts1.user_id) gts 
on gts.user_id = ts.user_id and gts.max_snapshot_tweet_id = ts.snapshot_tweet_id;
"""

