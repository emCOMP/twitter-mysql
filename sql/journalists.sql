drop database if exists `journalists`;
create database `journalists` DEFAULT CHARACTER SET=utf8mb4 DEFAULT COLLATE=utf8mb4_unicode_ci;
USE `journalists`;

SET SQL_MODE='ALLOW_INVALID_DATES';

#=====================================
# drop instance tables
#=====================================

DROP TABLE IF EXISTS `tweets`;


CREATE TABLE `tweets` (
  `id` bigint NOT NULL,

  `created_at` varchar(64) DEFAULT NULL,
  `created_ts` DATETIME NULL DEFAULT NULL,
  `lang` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `text` varchar(500) CHARACTER SET utf8mb4 DEFAULT NULL,
  `geo_coordinates_0` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `geo_coordinates_1` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL,

  `contributors` JSON DEFAULT NULL,
  `counts` JSON DEFAULT NULL,
  `entities` JSON DEFAULT NULL,
  `filter_level` VARCHAR(80) DEFAULT NULL,
  `coordinates` JSON DEFAULT NULL,
  `place` JSON DEFAULT NULL,
  `possibly_sensitive` INT(1) DEFAULT NULL,


  `user` JSON DEFAULT NULL,
  `user_id` bigint DEFAULT NULL,
  `user_screen_name` varchar(140) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_followers_count` int DEFAULT NULL,
  `user_friends_count` int DEFAULT NULL,
  `user_statuses_count` int DEFAULT NULL,
  `user_favourites_count` int DEFAULT NULL,
  `user_geo_enabled` int(1) default NULL,
  `user_time_zone` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_description` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_location` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_created_at` varchar(64) DEFAULT NULL,
  `user_created_ts` DATETIME NULL DEFAULT NULL,
  `user_lang` varchar(8) default NULL,
  `user_listed_count` int DEFAULT NULL,
  `user_name` varchar(140) DEFAULT NULL,
  `user_url` varchar(512) DEFAULT NULL,
  `user_utc_offset` int DEFAULT NULL,
  `user_verified` int(1) DEFAULT NULL,

  `user_profile_use_background_image` int(1) DEFAULT NULL,
  `user_default_profile_image` int(1) DEFAULT NULL,
  `user_profile_sidebar_fill_color` varchar(16) DEFAULT NULL,
  `user_profile_text_color` varchar(16) DEFAULT NULL,
  `user_profile_sidebar_border_color` varchar(16) DEFAULT NULL,
  `user_profile_background_color` varchar(16) DEFAULT NULL,
  `user_profile_link_color` varchar(16) DEFAULT NULL,
  `user_profile_image_url` varchar(256) DEFAULT NULL,
  `user_profile_banner_url` varchar(256) DEFAULT NULL,
  `user_profile_background_image_url` varchar(256) DEFAULT NULL,
  `user_profile_background_tile` int(1) DEFAULT NULL,
  `user_contributors_enabled` int(1) DEFAULT NULL,
  `user_default_profile` int(1) DEFAULT NULL,
  `user_is_translator` int(1) DEFAULT NULL,

  `retweet_count` int DEFAULT NULL,
  `favorite_count` int DEFAULT NULL,
  `retweeted_status` JSON DEFAULT NULL,
  `retweeted_status_id` bigint DEFAULT NULL,
  `retweeted_status_user_screen_name` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `retweeted_status_retweet_count` int DEFAULT NULL,
  `retweeted_status_user_id` bigint DEFAULT NULL,
  `retweeted_status_user_time_zone` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `retweeted_status_user_friends_count` int DEFAULT NULL,
  `retweeted_status_user_statuses_count` int DEFAULT NULL,
  `retweeted_status_user_followers_count` int DEFAULT NULL,
  `source` varchar(500) DEFAULT NULL,
  `in_reply_to_screen_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `in_reply_to_status_id` bigint DEFAULT NULL,
  `in_reply_to_user_id` bigint DEFAULT NULL,

  `quoted_status_id` bigint DEFAULT NULL,
  `quoted_status_id_str` VARCHAR(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `quoted_status` JSON DEFAULT NULL,

  `truncated` int(1) DEFAULT NULL,



  `local_time` DATETIME NULL DEFAULT NULL,

  `rumor` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `codes_first` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `codes_uncertainty` int(1) default 0,
  `codes_implicit` int(1) default 0,
  `codes_ambiguity` int(1) default 0,



  PRIMARY KEY (`id`),
  INDEX `idx_tweets_user_screen_name` (`user_screen_name`),
  INDEX `idx_tweets_user_id` (`user_id`),
  FULLTEXT KEY `idx_tweets_oso_text` (`text`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


