use `oso3`;

CREATE TABLE `users_current` (
  `id` bigint NOT NULL, 
  `screen_name` varchar(140) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `followers_count` int DEFAULT NULL,
  `friends_count` int DEFAULT NULL,
  `statuses_count` int DEFAULT NULL,
  `favourites_count` int DEFAULT NULL,
  `location` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` varchar(64) DEFAULT NULL,
  `created_ts` DATETIME NULL DEFAULT NULL,
  `geo_enabled` int(1) default NULL,
  `lang` varchar(8) default NULL,
  `listed_count` int DEFAULT NULL,
  `name` varchar(140) DEFAULT NULL,
  `time_zone` varchar(64) DEFAULT NULL,
  `url` varchar(512) DEFAULT NULL,
  `utc_offset` int DEFAULT NULL,
  `verified` int(1) DEFAULT NULL,

  `profile_use_background_image` int(1) DEFAULT NULL,
  `default_profile_image` int(1) DEFAULT NULL,
  `profile_sidebar_fill_color` varchar(16) DEFAULT NULL,
  `profile_text_color` varchar(16) DEFAULT NULL,
  `profile_sidebar_border_color` varchar(16) DEFAULT NULL,
  `profile_background_color` varchar(16) DEFAULT NULL,
  `profile_background_image_url_https` varchar(16) DEFAULT NULL,
  `profile_link_color` varchar(16) DEFAULT NULL,
  `profile_image_url` varchar(256) DEFAULT NULL,
  `profile_banner_url` varchar(256) DEFAULT NULL,
  `profile_background_image_url` varchar(256) DEFAULT NULL,
  `profile_background_tile` int(1) DEFAULT NULL,
  `contributors_enabled` int(1) DEFAULT NULL,
  `default_profile` int(1) DEFAULT NULL,
  `is_translator` int(1) DEFAULT NULL,

  `request_date` datetime NULL DEFAULT NULL,
  `deletion_noticed_date` datetime NULL DEFAULT NULL,

  PRIMARY KEY (`id`),
  FOREIGN KEY (`id`) REFERENCES users(`id`),
  KEY `idx_user_screen_name` (`screen_name`),
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `user_stats` (
  `id` bigint NOT NULL,

  `statuses_count_in_set` int DEFAULT NULL, 

  `followers_count_min` int DEFAULT NULL,
  `followers_count_max` int DEFAULT NULL,
  `followers_count_delta` int DEFAULT NULL,
  `friends_count_min` int DEFAULT NULL,
  `friends_count_max` int DEFAULT NULL,
  `friends_count_delta` int DEFAULT NULL,
  `statuses_count_min` int DEFAULT NULL,
  `statuses_count_max` int DEFAULT NULL,
  `statuses_count_delta` int DEFAULT NULL,
  `favourites_count_min` int DEFAULT NULL,
  `favourites_count_max` int DEFAULT NULL,
  `favourites_count_delta` int DEFAULT NULL,
  `listed_count_min` int DEFAULT NULL,
  `listed_count_max` int DEFAULT NULL,
  `listed_count_delta` int DEFAULT NULL,

  `screen_name_change_count` int DEFAULT NULL,
  `name_change_count` int DEFAULT NULL,
  `location_change_count` int DEFAULT NULL,
  `geo_enabled_change_count` int DEFAULT NULL,
  `description_change_count` int DEFAULT NULL,
  `profile_change_count` int DEFAULT NULL,
  `url_change_count` int DEFAULT NULL,

  /* in set values */
  `timeline_total_retweets` int DEFAULT NULL, /* number of user's tweets in set that have been retweeted */
  `timeline_total_replied` int DEFAULT NULL, /* number of tweets that have replies from other people */
  `timeline_total_favorited` int DEFAULT NULL, /* number of tweets that have been favorited */

  `users_retweet_count` int DEFAULT NULL, /* number of users tweets in collection that are retweets */
  `users_replies_count` int DEFAULT NULL, /* number of uers tweets in collection that are replies */

  `percent_tweets_retweets` int DEFAULT NULL, /* % of users's tweets that are retweets */
  `percent_tweets_replies` int DEFAULT NULL, /* % of user's tweets that are replies */
  `percent_tweets_originals` int DEFAULT NULL, /* number of tweets that are deemed to be original */



  PRIMARY KEY (`id`),
  FOREIGN KEY (`id`) REFERENCES users(`id`),

)


CREATE TABLE `tweet_stats` (
  `id` bigint NOT NULL,

  `replies_count` int DEFAULT NULL,
  `replies_in_set` int DEFAULT NULL

  PRIMARY KEY (`id`),
  FOREIGN KEY (`id`) REFERENCES tweets(`id`),

)