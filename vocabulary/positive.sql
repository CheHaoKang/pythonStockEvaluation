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

-- Dumping structure for table stockevaluation.stockpositivevocabulary
CREATE TABLE IF NOT EXISTS `stockpositivevocabulary` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `word_trad` varchar(255) NOT NULL DEFAULT '',
  `word_simp` varchar(255) NOT NULL DEFAULT '',
  `en` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=99 DEFAULT CHARSET=utf8;

-- Dumping data for table stockevaluation.stockpositivevocabulary: ~96 rows (approximately)
/*!40000 ALTER TABLE `stockpositivevocabulary` DISABLE KEYS */;
INSERT IGNORE INTO `stockpositivevocabulary` (`id`, `word_trad`, `word_simp`, `en`) VALUES
	(1, '增', '增', 'increase'),
	(2, '升', '升', 'increase'),
	(3, '盈', '盈', 'make a profit'),
	(4, '漲', '涨', 'go up'),
	(5, '解套', '解套', 'stock release'),
	(6, '牛', '牛', 'perfect'),
	(7, '多頭', '多头', 'bull market'),
	(8, '利多', '利多', 'lots of incentives'),
	(9, '做多', '做多', 'Long '),
	(10, '短多', '短多', 'make money in a short period of time'),
	(11, '長多', '长多', 'make money in a long period of time'),
	(12, '軋空', '轧空', 'Corners'),
	(13, '彈', '弹', 'go up'),
	(14, '買', '买', 'buy'),
	(15, '上', '上', 'up'),
	(16, '強', '强', 'strong'),
	(17, '高', '高', 'high'),
	(18, '賺', '赚', 'make a profit'),
	(19, '勝', '胜', 'win'),
	(20, '贏', '赢', 'win'),
	(21, '獲利', '获利', 'make a profit'),
	(22, '牛市', '牛市', 'bull market'),
	(23, '成長', '成长', 'grow up'),
	(24, '優', '优', 'great'),
	(25, '沖', '冲', 'roar'),
	(26, '好', '好', 'good'),
	(27, '穩', '稳', 'stable'),
	(28, '善', '善', 'benign'),
	(29, '良', '良', 'good'),
	(30, '順', '顺', 'smooth'),
	(31, '成功', '成功', 'success'),
	(32, '峰', '峰', 'peak'),
	(33, '佳', '佳', 'good'),
	(34, '暖', '暖', 'warm'),
	(35, '熱', '热', 'hot'),
	(36, '揚', '扬', 'go up'),
	(37, '紅', '红', 'popular'),
	(38, '投資', '投资', 'investment'),
	(39, '沛', '沛', 'abundance'),
	(40, '益', '益', 'profit'),
	(41, '促', '促', 'facilitate'),
	(42, '不錯', '不错', 'nice'),
	(43, '利潤', '利润', 'profit'),
	(44, '加倉', '加仓', 'buy more'),
	(45, '飆', '飙', 'roar'),
	(46, '融', '融', 'increase'),
	(47, '獲', '获', 'obtain'),
	(48, '提', '提', 'raise'),
	(49, '振', '振', 'cheer up'),
	(50, '吉', '吉', 'good sign'),
	(51, '泰', '泰', 'good sign'),
	(52, '滿倉', '满仓', 'put all money into the stock market'),
	(53, '贊', '贊', 'good'),
	(54, '讚', '赞', 'good'),
	(55, '衝', '冲', 'rush'),
	(56, '飛', '飞', 'fly'),
	(57, '蓬', '蓬', 'abundant'),
	(58, '勃', '勃', 'abundant'),
	(59, '潛力', '潜力', 'potential'),
	(60, '躍', '跃', 'active'),
	(61, '資金', '资金', 'investment'),
	(62, '扭轉', '扭转', 'revert'),
	(63, '高送轉', '高送转', 'potential'),
	(64, '平反', '平反', 'say something good'),
	(65, '合作', '合作', 'cooperation'),
	(67, '支撐', '支撑', 'support'),
	(68, '持', '持', 'hold'),
	(69, '補', '补', 'add'),
	(70, '信心', '信心', 'confidence'),
	(71, '踏實', '踏实', 'feel confident'),
	(72, '抬', '抬', 'raise'),
	(73, '可觀', '可观', 'a huge amount'),
	(74, '突破', '突破', 'breakthorugh'),
	(76, '加', '加', 'add'),
	(77, '頂', '顶', 'top'),
	(78, '完美', '完美', 'perfect'),
	(79, '敬', '敬', 'respect'),
	(80, '回', '回', 'go up'),
	(81, '漲停', '涨停', 'Limit Up'),
	(82, '富', '富', 'rich'),
	(83, '健康', '健康', 'healthy'),
	(84, '前途', '前途', 'future'),
	(85, '堅', '坚', 'strong'),
	(86, '挺', '挺', 'strong'),
	(87, '穫', '穫', 'harvest'),
	(88, '高大上', '高大上', 'great'),
	(89, '低估', '低估', 'underestimate'),
	(90, '掙', '挣', 'earn'),
	(91, '大肉', '大肉', 'benefit'),
	(92, '風險低', '风险低', 'low risk'),
	(93, '品質高', '品质高', 'high quality'),
	(94, '壯', '壮', 'strong'),
	(95, '實在', '实在', 'firmly'),
	(96, '翻倍', '翻倍', 'double'),
	(97, '耕', '耕', 'invest'),
	(98, '成熟', '成熟', 'mature');
/*!40000 ALTER TABLE `stockpositivevocabulary` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
