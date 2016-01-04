
/*
 Navicat Premium Data Transfer

 Source Server         : 127.0.0.1
 Source Server Type    : MySQL
 Source Server Version : 50623
 Source Host           : 127.0.0.1
 Source Database       : apollo

 Target Server Type    : MySQL
 Target Server Version : 50623
 File Encoding         : utf-8

 Date: 01/04/2016 09:28:11 AM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

create database apollo;
use apollo;

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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
