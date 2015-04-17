
create database `oso3` DEFAULT CHARACTER SET=utf8mb4 DEFAULT COLLATE=utf8mb4_unicode_ci;
USE `oso3`;

SET SQL_MODE='ALLOW_INVALID_DATES';

#=====================================
# drop instance tables
#=====================================
DROP TABLE IF EXISTS `tweet_url`;
DROP TABLE IF EXISTS `tweet_mention`;
DROP TABLE IF EXISTS `tweet_media`;
DROP TABLE IF EXISTS `tweet_hashtag`;
DROP TABLE IF EXISTS `tweet_webpage`;

DROP TABLE IF EXISTS `media`;
DROP TABLE IF EXISTS `tweets`;
DROP TABLE IF EXISTS `hashtags`;
DROP TABLE IF EXISTS `webpages`;
DROP TABLE IF EXISTS `urls`;
DROP TABLE IF EXISTS `users`;

#=====================================
# create tables
#=====================================

CREATE TABLE `urls` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `url` varchar(1000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `expanded_url` varchar(2000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `display_url` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `webpages` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `url` varchar(1000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,    
    `title` varchar(1000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `users` (
  `id` bigint(20) NOT NULL, 
  `screen_name` varchar(140) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `followers_count` int(11) DEFAULT NULL,
  `friends_count` int(11) DEFAULT NULL,
  `statuses_count` int(11) DEFAULT NULL,
  `favourites_count` int(11) DEFAULT NULL,
  `location` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` varchar(64) DEFAULT NULL,
  `created_ts` timestamp NULL DEFAULT NULL,
  `geo_enabled` int(1) default NULL,
  `lang` varchar(8) default NULL,
  `listed_count` int(11) DEFAULT NULL,
  `name` varchar(140) DEFAULT NULL,
  `time_zone` varchar(64) DEFAULT NULL,
  `url` varchar(512) DEFAULT NULL,
  `utc_offset` int(11) DEFAULT NULL,
  `verified` int(1) DEFAULT NULL,

  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `hashtags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `media` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
    `type` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `media_id` bigint(20) DEFAULT NULL,
    `source_status_id` bigint(20) DEFAULT NULL,
  `expanded_url` varchar(1000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `display_url` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `media_url` varchar(1000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `idx_media_media_id` (`media_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



CREATE TABLE `tweets` (
  `id` bigint(20) NOT NULL,
  `created_at` varchar(64) DEFAULT NULL,
  `created_ts` timestamp NULL DEFAULT NULL,
  `lang` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `text` varchar(500) CHARACTER SET utf8mb4 DEFAULT NULL,
  `geo_coordinates_0` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `geo_coordinates_1` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `user_screen_name` varchar(140) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_followers_count` int(11) DEFAULT NULL,
  `user_friends_count` int(11) DEFAULT NULL,
  `user_statuses_count` int(11) DEFAULT NULL,
  `user_favourites_count` int(11) DEFAULT NULL,
  `user_geo_enabled` int(1) default NULL,
  `user_time_zone` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `retweeted_status_id` bigint(20) DEFAULT NULL,
  `retweeted_status_user_screen_name` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `retweeted_status_retweet_count` int(11) DEFAULT NULL,
  `retweeted_status_user_id` bigint(20) DEFAULT NULL,
  `retweeted_status_user_time_zone` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `retweeted_status_user_friends_count` int(11) DEFAULT NULL,
  `retweeted_status_user_statuses_count` int(11) DEFAULT NULL,
  `retweeted_status_user_followers_count` int(11) DEFAULT NULL,
  `source` varchar(500) DEFAULT NULL,
  `in_reply_to_screen_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `in_reply_to_status_id` bigint(20) DEFAULT NULL,
  `in_reply_to_user_id` bigint(20) DEFAULT NULL,
  `in_set` int(11) DEFAULT NULL,
  `local_time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_tweets_user_screen_name` (`user_screen_name`),
  KEY `idx_tweets_retweeted_status_id` (`retweeted_status_id`),
  KEY `idx_tweets_retweeted_status_user_id` (`retweeted_status_user_id`),
  KEY `idx_tweets_in_reply_to_user_id` (`in_reply_to_user_id`),
  KEY `idx_tweets_in_reply_to_status_id` (`in_reply_to_status_id`),
  KEY `idx_tweets_user_id` (`user_id`),
  FULLTEXT KEY `idx_tweets_Oso_text` (`text`)
) ENGINE=InnoDB AUTO_INCREMENT=5292305 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `tweet_url` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
    `tweet_id` bigint(20) NOT NULL, 
    `url_id` int(11) NOT NULL,
    KEY (tweet_id),
    KEY (url_id),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;    

CREATE TABLE `tweet_mention` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
    `tweet_id` bigint(20) NOT NULL, 
    `user_id` bigint(20) NOT NULL,
    `tweet_index` int(3) NOT NULL,
    KEY (tweet_id),
    KEY (user_id),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `tweet_media` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
    `tweet_id` bigint(20) NOT NULL, 
    `media_id` int(11) NOT NULL,
    KEY (tweet_id),
    KEY (media_id),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;    
    
CREATE TABLE `tweet_hashtag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
    `tweet_id` bigint(20) NOT NULL, 
    `hashtag_id` int(11) NOT NULL,
    KEY (tweet_id),
    KEY (hashtag_id),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;  


CREATE TABLE `tweet_webpage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
    `tweet_id` bigint(20) NOT NULL, 
    `webpage_id` int(11) NOT NULL,
    KEY (tweet_id),
    KEY (webpage_id),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;  

 
