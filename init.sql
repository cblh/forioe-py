-- phpMyAdmin SQL Dump
-- version 4.0.10.9
-- http://www.phpmyadmin.net
--
-- 主机: localhost
-- 生成日期: 2015-04-16 00:36:33
-- 服务器版本: 10.0.15-MariaDB
-- PHP 版本: 5.6.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `forioe`
--

-- --------------------------------------------------------

--
-- 表的结构 `report`
--

CREATE TABLE IF NOT EXISTS `report` (
  `id` int(5) NOT NULL AUTO_INCREMENT,
  `creator` varchar(20) NOT NULL,
  `createtime` varchar(20) NOT NULL,
  `groupid` int(5) NOT NULL,
  `title` varchar(100) NOT NULL,
  `content` mediumtext NOT NULL,
  `isresponsed` varchar(5) NOT NULL DEFAULT '否',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=9 ;

--
-- 转存表中的数据 `report`
--

INSERT INTO `report` (`id`, `creator`, `createtime`, `groupid`, `title`, `content`, `isresponsed`) VALUES
(5, 'grm', '2015-04-14 11:46:57', 2, '开题报告', '<p style="color: rgb(0, 0, 0); font-family: &#039;Tim_d-color: rgb(255, 255, 255);" class="MsoNormal"><b><span style="font-size: 12pt; font-family: 宋体; color: rgb(0, 0, 0);">本选题的意义及国内外研究状况：</span><span style="font-size: 12pt; font-family: &#039;Times New Roman&#039;; color: rgb(0, 0, 0);"><span>     </span></span></b><span style="font-size: 12pt; font-family: &#039;Times New Roman&#039;; color: rgb(0, 0, 0);"><span></span></span></p><p style="color: rgb(0, 0, 0); font-family: &#039;Tim_d-color: rgb(255, 255, 255);" class="MsoNormal"><span style="font-size: 12pt; font-family: &#039;Times New Roman&#039;; color: rgb(0, 0, 0);"> </span></p><p style="color: rgb(0, 0, 0); font-family: &#039;Tim_d-color: rgb(255, 255, 255);" class="MsoNormal"><span style="font-size: 12pt; font-family: 宋体; color: rgb(0, 0, 0);">运维自动化是指将</span><span style="font-size: 12pt; font-family: &#039;Times New Roman&#039;; color: rgb(0, 0, 0);">IT</span><span style="font-size: 12pt; font-family: 宋体; color: rgb(0, 0, 0);">运维中日常的、大量的重复性工作自动化，把过去的手工执行转为自动化操作。自动化是</span><span style="font-size: 12pt; font-family: &#039;Times New Roman&#039;; color: rgb(0, 0, 0);">IT</span><span style="font-size: 12pt; font-family: 宋体; color: rgb(0, 0, 0);">运维工作的升华，</span><span style="font-size: 12pt; font-family: &#039;Times New Roman&#039;; color: rgb(0, 0, 0);">IT</span><span style="font-size: 12pt; font-family: 宋体; color: rgb(0, 0, 0);">运维自动化不单纯是一个维护过程，更是一个管理的提升过程，是</span><span style="font-size: 12pt; font-family: &#039;Times New Roman&#039;; color: rgb(0, 0, 0);">IT</span><span style="font-size: 12pt; font-family: 宋体; color: rgb(0, 0, 0);">运维的最高层次，也是未来的发展趋势。</span><span style="font-size: 12pt; font-family: &#039;Times New Roman&#039;; color: rgb(0, 0, 0);"><span></span></span></p><p style="color: rgb(0, 0, 0); font-family: &#039;Tim_d-color: rgb(255, 255, 255);" class="MsoNormal"><span style="font-size: 12pt; font-family: &#039;Times New Roman&#039;; color: rgb(0, 0, 0);"> </span></p><p style="color: rgb(0, 0, 0); font-family: &#039;Tim_d-color: rgb(255, 255, 255);" class="MsoNormal"><span style="font-size: 12pt; font-family: 宋体; color: rgb(0, 0, 0);">谷歌、腾讯、百度和阿里等规模的公司内一般都有统一的运维团队，有一套或多套自动化运维系统可供参照，运维部门与开发部门会是相互平行的视角。并且也开始更加关注IT基础设施在架构层面的优化以及超大规模集群下的自动化管理和切</span><span style="font-size: 12pt; font-family: 宋体;">换</span><span style="font-size: 12pt; font-family: 宋体;">。</span><span style="font-size: 12pt; font-family: 宋体;"><span></span></span></p><p style="color: rgb(0, 0, 0); font-family: &#039;Tim_d-color: rgb(255, 255, 255);" class="MsoNormal"><span style="font-size: 12pt; font-family: 宋体;"> </span></p><p style="color: rgb(0, 0, 0); font-family: &#039;Tim_d-color: rgb(255, 255, 255);" class="MsoNormal"><span style="font-size: 12pt; font-family: 宋体;">反观游戏运维则在这方面相对薄弱，究其原因。传统互联网与游戏运维存在相当大的不同，适用于互联网的自动化系统并不能完美移植到游戏运维。另一方面，大公司的技术壁垒的存在，使得其技术不能造福于其他</span><span style="font-size: 12pt; font-family: 宋体;">IT公司，自主设计一套自动化运维系统是很有必要的。</span></p>', '是'),
(7, 'grm', '2015-04-14 11:50:11', 2, '开题补充', '<span style="color: rgb(0, 0, 0); font-family: 微软雅黑, &#039;MS Sans S_d-color: rgb(255, 255, 255);">毕业设计的答辩演示的时候，就在虚拟机上面搭建几个服务器，然后初始化好环境，这样就能结合管理后台模拟了</span>', '是');

-- --------------------------------------------------------

--
-- 表的结构 `response`
--

CREATE TABLE IF NOT EXISTS `response` (
  `id` int(5) NOT NULL AUTO_INCREMENT,
  `groupid` int(5) NOT NULL,
  `createtime` varchar(20) NOT NULL,
  `toid` int(5) NOT NULL,
  `towho` varchar(20) NOT NULL,
  `title` varchar(30) DEFAULT NULL,
  `content` mediumtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=8 ;

--
-- 转存表中的数据 `response`
--

INSERT INTO `response` (`id`, `groupid`, `createtime`, `toid`, `towho`, `title`, `content`) VALUES
(2, 2, '2015-04-14 11:48:02', 5, 'grm', '开题报告', '<div style="color: rgb(0, 0, 0); font-family: Arial; font-size: 14px; line-height: 23.7999992370605px;">从论文的角度是否还需要调研一下<span style="font-family: 宋体; font-size: 12pt;">运维自动化特别是游戏运维的现状及一般采用的方法，因为你的研究很多人不熟悉，有些名词需要在写论文的时候做一下必要的解释。</span></div><div style="color: rgb(0, 0, 0); font-family: Arial; font-size: 14px; line-height: 23.7999992370605px;"> </div><div style="color: rgb(0, 0, 0); font-family: Arial; font-size: 14px; line-height: 23.7999992370605px;">你在外面如果上网不方便，自己要把握好各个材料上交的时间节点。</div>'),
(3, 2, '2015-04-14 11:49:10', 5, 'grm', '开题报告', '<span style="color: rgb(0, 0, 0); font-family: Arial; font-size: 14px; line-height: 23.7999992370605px;">你的报告内容很不错，我上次说只是想请你写个东西简单介绍一下你准备做毕业论文的内容，你直接写了开题报告倒是也挺不错的。开题论文后面没有完成的内容你补充一下，按时间上交就可以了。</span>');

-- --------------------------------------------------------

--
-- 表的结构 `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `id` int(5) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT NULL,
  `realname` varchar(20) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `schoolnum` varchar(20) DEFAULT NULL,
  `phonenum` varchar(15) DEFAULT NULL,
  `email` varchar(40) NOT NULL DEFAULT ' ',
  `status` varchar(3) NOT NULL DEFAULT '0',
  `groupid` int(5) DEFAULT '0',
  `last_report` text,
  `last_request` text,
  `delay_count` int(11) DEFAULT '0',
  `start_time` varchar(30) DEFAULT '2014-01-01',
  `end_time` varchar(30) DEFAULT '2015-01-01',
  `process` varchar(30) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=6 ;

--
-- 转存表中的数据 `user`
--

INSERT INTO `user` (`id`, `name`, `realname`, `password`, `schoolnum`, `phonenum`, `email`, `status`, `groupid`, `last_report`, `last_request`, `delay_count`, `start_time`, `end_time`, `process`) VALUES
(2, 'grunmin', 'grunmin', 'c93ccd78b2076528346216b3b2f701e6', 'gz1230', '13422222222', ' ', '3', 1, NULL, NULL, 0, '2014-01-01', '2015-01-01', '0'),
(3, 'grm', 'grm', 'e00cf25ad42683b3df678c61f42c6bda', '20111111111', '13411111111', 'grunmin@foxmail.com', '2', 2, '2015-04-15', '2015-04-17', 2, '2015-02-07', '2015-06-30', '41'),
(4, 'admin', 'admin', 'c93ccd78b2076528346216b3b2f701e6', 'admin', 'admin', ' ', '3', 1, NULL, NULL, 0, '2014-01-01', '2015-01-01', '0');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
