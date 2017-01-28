DROP TABLE IF EXISTS `tb1_follows`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb1_follows` (
  `author_id` int(11) NOT NULL DEFAULT '0',
  `last_tweet_follow` datetime DEFAULT NULL,
  PRIMARY KEY (`author_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `tb1_retweets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb1_retweets` (
  `tweet_id` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `tweet_text` text COLLATE utf8mb4_unicode_ci,
  `tweet_time` datetime DEFAULT NULL,
  `author_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` int(1) DEFAULT '0',
  `time_zone` text CHARACTER SET utf8,
  `error` text CHARACTER SET utf8,
  `location` text CHARACTER SET utf8,
  `url` text CHARACTER SET utf8,
  PRIMARY KEY (`tweet_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

