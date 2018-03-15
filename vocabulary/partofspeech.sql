-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.2.11-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for stockevaluation
CREATE DATABASE IF NOT EXISTS `stockevaluation` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `stockevaluation`;

-- Dumping structure for table stockevaluation.stockpartofspeech
CREATE TABLE IF NOT EXISTS `stockpartofspeech` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `word_trad` varchar(255) NOT NULL DEFAULT '',
  `word_simp` varchar(255) NOT NULL DEFAULT '',
  `en` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- Dumping data for table stockevaluation.stockpartofspeech: ~12 rows (approximately)
/*!40000 ALTER TABLE `stockpartofspeech` DISABLE KEYS */;
INSERT IGNORE INTO `stockpartofspeech` (`id`, `word_trad`, `word_simp`, `en`) VALUES
	(1, '不', '不', 'no'),
	(2, '沒', '没', 'no'),
	(3, '負', '负', 'negative'),
	(4, '停', '停', 'stop'),
	(5, '失敗', '失败', 'fail'),
	(6, '否', '否', 'no'),
	(7, '止', '止', 'stop'),
	(8, '減', '减', 'decrease'),
	(9, '不會', '不会', 'no'),
	(10, '無', '无', 'no'),
	(11, '放', '放', 'free'),
	(12, '沒有', '没有', 'no');
/*!40000 ALTER TABLE `stockpartofspeech` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
