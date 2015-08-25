drop database if exists `oso3`;
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
DROP TABLE IF EXISTS `tweet_snapshots`;
DROP TABLE IF EXISTS `tweets`;
DROP TABLE IF EXISTS `hashtags`;
DROP TABLE IF EXISTS `webpages`;
DROP TABLE IF EXISTS `urls`;
DROP TABLE IF EXISTS `users`;

#=====================================
# create tables
#=====================================

CREATE TABLE `urls` (
    `id` int NOT NULL AUTO_INCREMENT,
    `url` varchar(1000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `expanded_url` varchar(2000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `display_url` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `webpages` (
    `id` int NOT NULL AUTO_INCREMENT,
    `url` varchar(1000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,    
    `title` varchar(1000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `users` (
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

  PRIMARY KEY (`id`),
  KEY `idx_user_screen_name` (`screen_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `hashtags` (
  `id` int NOT NULL AUTO_INCREMENT,
  `text` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `media` (
  `id` int NOT NULL AUTO_INCREMENT,
    `type` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `media_id` bigint DEFAULT NULL,
    `source_status_id` bigint DEFAULT NULL,
  `expanded_url` varchar(1000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `display_url` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `media_url` varchar(1000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `idx_media_media_id` (`media_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `tweet_snapshots` (
  `id` int NOT NULL AUTO_INCREMENT,
  `snapshot_tweet_id` bigint NOT NULL,
  `snapshot_time` DATETIME NOT NULL,
  `retweet_source_id` bigint DEFAULT NULL,

  `tweet_id` bigint NOT NULL,
  `created_at` varchar(64) DEFAULT NULL,
  `created_ts` DATETIME NULL DEFAULT NULL,
  `lang` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `text` varchar(500) CHARACTER SET utf8mb4 DEFAULT NULL,
  `geo_coordinates_0` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `geo_coordinates_1` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
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
  `retweet_count` int DEFAULT NULL,
  `favorite_count` int DEFAULT NULL,
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
  `in_set` int DEFAULT NULL,
  `local_time` DATETIME NULL DEFAULT NULL,

  PRIMARY KEY (`id`),
  KEY `idx_tweets_tweet_id` (`tweet_id`),
  KEY `idx_tweets_retweeted_status_id` (`retweeted_status_id`),
  FOREIGN KEY (`retweeted_status_user_id`) REFERENCES users(`id`),
  FOREIGN KEY (`in_reply_to_user_id`) REFERENCES users(`id`),
  KEY `idx_tweets_in_reply_to_status_id` (`in_reply_to_status_id`),
  FOREIGN KEY (`user_id`) REFERENCES users(`id`),
  KEY `idx_tweets_retweet_source_id` (`retweet_source_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5292305 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `tweets` (
  `id` bigint NOT NULL,
  `created_at` varchar(64) DEFAULT NULL,
  `created_ts` DATETIME NULL DEFAULT NULL,
  `lang` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `text` varchar(500) CHARACTER SET utf8mb4 DEFAULT NULL,
  `geo_coordinates_0` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `geo_coordinates_1` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_id` bigint DEFAULT NULL,
  `user_screen_name` varchar(140) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_followers_count` int DEFAULT NULL,
  `user_friends_count` int DEFAULT NULL,
  `user_statuses_count` int DEFAULT NULL,
  `user_favourites_count` int DEFAULT NULL,
  `user_geo_enabled` int(1) default NULL,
  `user_time_zone` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `retweet_count` int DEFAULT NULL,
  `favorite_count` int DEFAULT NULL,
  `retweeted` int(1) DEFAULT 0,
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
  `local_time` DATETIME NULL DEFAULT NULL,
  `retweet_source_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_tweets_user_screen_name` (`user_screen_name`),
  FOREIGN KEY (`retweeted_status_id`) REFERENCES tweets(`id`),
  FOREIGN KEY (`retweeted_status_user_id`) REFERENCES users(`id`),
  FOREIGN KEY (`in_reply_to_user_id`) REFERENCES users(`id`),
  FOREIGN KEY (`in_reply_to_status_id`) REFERENCES tweets(`id`),
  FOREIGN KEY (`user_id`) REFERENCES users(`id`),
  FOREIGN KEY (`retweet_source_id`) REFERENCES tweets(`id`),
  FULLTEXT KEY `idx_tweets_oso_text` (`text`)
) ENGINE=InnoDB AUTO_INCREMENT=5292305 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



CREATE TABLE `tweet_url` (
  `id` int NOT NULL AUTO_INCREMENT,
    `tweet_id` bigint NOT NULL, 
    `url_id` int NOT NULL,
    FOREIGN KEY (`tweet_id`) REFERENCES tweets(`id`),
    FOREIGN KEY (`url_id`) REFERENCES urls(`id`),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;    

CREATE TABLE `tweet_mention` (
  `id` int NOT NULL AUTO_INCREMENT,
    `tweet_id` bigint NOT NULL, 
    `user_id` bigint NOT NULL,
    `tweet_index` int(3) NOT NULL,
    FOREIGN KEY (`tweet_id`) REFERENCES tweets(`id`),
    FOREIGN KEY (`user_id`) REFERENCES users(`id`),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `tweet_media` (
  `id` int NOT NULL AUTO_INCREMENT,
    `tweet_id` bigint NOT NULL, 
    `media_id` int NOT NULL,
    FOREIGN KEY (`tweet_id`) REFERENCES tweets(`id`),
    FOREIGN KEY (`media_id`) REFERENCES media(`id`),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;    
    
CREATE TABLE `tweet_hashtag` (
  `id` int NOT NULL AUTO_INCREMENT,
    `tweet_id` bigint NOT NULL, 
    `hashtag_id` int NOT NULL,
    FOREIGN KEY (`tweet_id`) REFERENCES tweets(`id`),
    FOREIGN KEY (`hashtag_id`) REFERENCES hashtags(`id`),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;  


CREATE TABLE `tweet_webpage` (
  `id` int NOT NULL AUTO_INCREMENT,
    `tweet_id` bigint NOT NULL, 
    `webpage_id` int NOT NULL,
    FOREIGN KEY (`tweet_id`) REFERENCES tweets(`id`),
    FOREIGN KEY (`webpage_id`) REFERENCES webpages(`id`),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;  

 
