/*
 Navicat Premium Data Transfer

 Source Server         : 10.37.63.8
 Source Server Type    : MySQL
 Source Server Version : 50627
 Source Host           : 10.37.63.8
 Source Database       : apollo

 Target Server Type    : MySQL
 Target Server Version : 50627
 File Encoding         : utf-8

 Date: 01/07/2016 09:50:47 AM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `accounts`
-- ----------------------------
DROP TABLE IF EXISTS `accounts`;
CREATE TABLE `accounts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `passwd` varchar(64) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `login_name` varchar(64) DEFAULT NULL,
  `mobile` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `book_tag`
-- ----------------------------
DROP TABLE IF EXISTS `book_tag`;
CREATE TABLE `book_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `book_id` int(11) DEFAULT NULL,
  `tag_id` int(11) DEFAULT NULL,
  `count` int(11) DEFAULT NULL COMMENT '被标记的数量',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `books`
-- ----------------------------
DROP TABLE IF EXISTS `books`;
CREATE TABLE `books` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(64) NOT NULL COMMENT '书名',
  `isbn13` varchar(15) DEFAULT NULL,
  `author` varchar(128) DEFAULT NULL COMMENT '作者',
  `rating` float DEFAULT NULL COMMENT '豆瓣评分',
  `pubdate` varchar(16) DEFAULT NULL COMMENT '出版日期',
  `image` varchar(128) DEFAULT NULL COMMENT '封面',
  `douban_id` bigint(20) DEFAULT NULL,
  `publisher` varchar(64) DEFAULT NULL COMMENT '出版社',
  `douban_url` varchar(128) DEFAULT NULL,
  `summary` text COMMENT '摘要',
  `price` varchar(32) DEFAULT NULL COMMENT '价格',
  `pages` varchar(32) DEFAULT NULL COMMENT '页数',
  `catalog` text COMMENT '目录',
  `owner_name` varchar(64) DEFAULT NULL COMMENT '贡献人',
  `owner_id` int(11) DEFAULT NULL,
  `borrow_name` varchar(64) DEFAULT NULL COMMENT '当前借书人',
  `borrow_id` int(11) DEFAULT NULL,
  `borrow_counts` int(11) DEFAULT NULL COMMENT '借阅次数',
  `borrow_log_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `borrow_log`
-- ----------------------------
DROP TABLE IF EXISTS `borrow_log`;
CREATE TABLE `borrow_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `account_id` int(11) DEFAULT NULL COMMENT '借阅人ID',
  `book_id` int(11) DEFAULT NULL COMMENT '书籍ID',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '借阅时间',
  `reback_time` date DEFAULT NULL COMMENT '还书时间',
  `borrow_days` int(6) DEFAULT NULL COMMENT '借阅天数',
  `real_reback_time` datetime DEFAULT NULL COMMENT '实际还书时间',
  `account_name` varchar(64) DEFAULT NULL COMMENT '借阅人',
  `book_name` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `tags`
-- ----------------------------
DROP TABLE IF EXISTS `tags`;
CREATE TABLE `tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

SET FOREIGN_KEY_CHECKS = 1;
