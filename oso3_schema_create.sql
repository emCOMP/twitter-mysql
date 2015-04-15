
#create database `oso3` DEFAULT CHARACTER SET=utf8mb4 DEFAULT COLLATE=utf8mb4_unicode_ci;
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

#=====================================
# create tables
#=====================================
DROP TABLE IF EXISTS `urls`;
CREATE TABLE `urls` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `url` varchar(1000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `expanded_url` varchar(2000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `display_url` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `webpages`;
CREATE TABLE `webpages` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `url` varchar(1000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,    
    `title` varchar(1000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `users`;
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

DROP TABLE IF EXISTS `hashtags`;
CREATE TABLE `hashtags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `media`;
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


DROP TABLE IF EXISTS `tweets`;
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
    FOREIGN KEY (tweet_id) REFERENCES tweets(id),
    FOREIGN KEY (url_id) REFERENCES urls(id),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;    

CREATE TABLE `tweet_mention` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
    `tweet_id` bigint(20) NOT NULL, 
    `user_id` bigint(20) NOT NULL,
    `tweet_index` int(3) NOT NULL,
    FOREIGN KEY (tweet_id) REFERENCES tweets(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `tweet_media` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
    `tweet_id` bigint(20) NOT NULL, 
    `media_id` int(11) NOT NULL,
    FOREIGN KEY (tweet_id) REFERENCES tweets(id),
    FOREIGN KEY (media_id) REFERENCES media(id),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;    
    
CREATE TABLE `tweet_hashtag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
    `tweet_id` bigint(20) NOT NULL, 
    `hashtag_id` int(11) NOT NULL,
    FOREIGN KEY (tweet_id) REFERENCES tweets(id),
    FOREIGN KEY (hashtag_id) REFERENCES hashtags(id),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;  


CREATE TABLE `tweet_webpage` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
    `tweet_id` bigint(20) NOT NULL, 
    `webpage_id` int(11) NOT NULL,
    FOREIGN KEY (tweet_id) REFERENCES tweets(id),
    FOREIGN KEY (webpage_id) REFERENCES webpages(id),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;  

 
