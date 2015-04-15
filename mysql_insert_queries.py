#!/usr/bin/env python
# -*- coding: utf-8 -*-

INSERT_TWEET_STMT = """INSERT INTO `tweets`
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
%(in_reply_to_user_id)s)
"""


INSERT_TWEET_WITH_RETWEET_STMT = """INSERT INTO `tweets`
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
%(in_reply_to_user_id)s
)"""




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



INSERT_HASHTAG_STMT = """REPLACE INTO `hashtags` (`text`) VALUES (%(text)s)"""



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

