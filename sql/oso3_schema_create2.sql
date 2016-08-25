
USE `oso3`;

# update to local time
update tweets set local_time = DATE_SUB(created_ts, interval 7 hour) where id > 0;
update tweet_snapshots set local_time = DATE_SUB(created_ts, interval 7 hour) where id > 0;

DROP TABLE IF EXISTS `user_account_types`;
DROP TABLE IF EXISTS `account_types`;
DROP TABLE IF EXISTS `tweet_subset_tags`;
DROP TABLE IF EXISTS `user_subset_tags`;
DROP TABLE IF EXISTS `subset_tags`;


CREATE TABLE `account_types` (
    `id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `set_id` int NULL,
    `description` TEXT COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `idx_account_types_name` (`name`),
    KEY `idx_account_types_set` (`set_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



CREATE TABLE `user_account_types` (
	`id` int NOT NULL AUTO_INCREMENT,
    `account_type_id` int NOT NULL,
    `user_id` bigint NOT NULL,
    PRIMARY KEY (`id`),
    KEY `idx_user_account_type_account_type_id` (`account_type_id`),
    FOREIGN KEY (`user_id`) REFERENCES users(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



CREATE TABLE `subset_tags` (
	`id` int NOT NULL AUTO_INCREMENT,
	`name` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `description` TEXT COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `idx_subset_tags_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



CREATE TABLE `tweet_subset_tags` (
	`id` int NOT NULL AUTO_INCREMENT,
    `subset_tag_id` int NOT NULL,
    `tweet_id` bigint NOT NULL,
    PRIMARY KEY (`id`),
    KEY `idx_tweet_subset_tags_subset_tag_id` (`subset_tag_id`),
    FOREIGN KEY (`tweet_id`) REFERENCES tweets(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `user_subset_tags` (
	`id` int NOT NULL AUTO_INCREMENT,
    `subset_tag_id` int NOT NULL,
    `user_id` bigint NOT NULL,
    PRIMARY KEY (`id`),
    KEY `idx_user_subset_tag_subset_tag_id` (`subset_tag_id`),
    FOREIGN KEY (`user_id`) REFERENCES users(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

#
# 530 slide data
#
#truncate subset_tags;
insert into subset_tags (`name`, `description`) values ('530slide', 'all tweets where text includes 530slide');
set @last_id_530slide_tag = (select last_insert_id());

# insert relations where either of these words appear
insert into tweet_subset_tags (`subset_tag_id`, `tweet_id`) 
	select @last_id_530slide_tag as `subset_tag_id`, t.id as tweet_id
    from tweets t where t.text like '%530slide%' or t.text like '%530 slide%';


# insert relations 
insert into user_subset_tags (`subset_tag_id`, `user_id`)
	select @last_id_530slide_tag as `subset_tag_id`, t.user_id as user_id
    from tweets t 
		inner join tweet_subset_tags twst on twst.tweet_id = t.id
		where twst.subset_tag_id = @last_id_530slide_tag
        group by user_id;


#
# osostrong
#
insert into subset_tags (`name`, `description`) values ('osostrong', 'all tweets/users where text includes osostrong');
set @last_id_osostrong_tag = (select last_insert_id());

# insert relations where either of these words appear
insert into tweet_subset_tags (`subset_tag_id`, `tweet_id`) 
	select @last_id_osostrong_tag as `subset_tag_id`, t.id as tweet_id
    from tweets t where t.text like '%osostrong%' or t.text like '%oso strong%';


# insert relations 
insert into user_subset_tags (`subset_tag_id`, `user_id`)
	select @last_id_osostrong_tag as `subset_tag_id`, t.user_id as user_id
    from tweets t 
		inner join tweet_subset_tags twst on twst.tweet_id = t.id
		where twst.subset_tag_id = @last_id_osostrong_tag
        group by user_id;

#
# 530 or oso & slide
#
insert into subset_tags (`name`, `description`) values ('oso slide', 'all tweets and users that have slide plus either 530 or oso');
set @last_id_slide_tag = (select last_insert_id());

# insert relations where either of these words appear
insert into tweet_subset_tags (`subset_tag_id`, `tweet_id`) 
    select @last_id_slide_tag as `subset_tag_id`, t.id as tweet_id
    from tweets t where t.text like '%oso%' and  t.text like '%slide%';


# insert relations 
insert into user_subset_tags (`subset_tag_id`, `user_id`)
    select @last_id_slide_tag as `subset_tag_id`, t.user_id as user_id
    from tweets t 
        inner join tweet_subset_tags twst on twst.tweet_id = t.id
        where twst.subset_tag_id = @last_id_slide_tag
        group by user_id;



