/*
 Navicat Premium Data Transfer

 Source Server         : 127.0.0.1
 Source Server Type    : MySQL
 Source Server Version : 50714
 Source Host           : localhost
 Source Database       : article_spider

 Target Server Type    : MySQL
 Target Server Version : 50714
 File Encoding         : utf-8

 Date: 07/04/2017 23:15:31 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `jobbole_article`
-- ----------------------------
DROP TABLE IF EXISTS `jobbole_article`;
CREATE TABLE `jobbole_article` (
  `title` varchar(200) NOT NULL,
  `create_date` date DEFAULT NULL,
  `url` varchar(300) NOT NULL,
  `url_object_id` varchar(50) NOT NULL,
  `front_image_url` varchar(300) DEFAULT NULL,
  `front_image_path` varchar(200) DEFAULT NULL,
  `comment_nums` int(11) NOT NULL DEFAULT '0',
  `fav_nums` int(11) NOT NULL DEFAULT '0',
  `praise_nums` int(11) NOT NULL DEFAULT '0',
  `tags` varchar(200) DEFAULT NULL,
  `content` longtext NOT NULL,
  PRIMARY KEY (`url_object_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
