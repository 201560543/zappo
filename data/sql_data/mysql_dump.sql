-- MySQL dump 10.13  Distrib 8.0.19, for osx10.15 (x86_64)
--
-- Host: localhost    Database: zappo
-- ------------------------------------------------------
-- Server version	8.0.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `organization_id` int unsigned NOT NULL COMMENT 'An organization can have one or multimple account accross time. Account could be closed. Another one opened.',
  `address_id` int unsigned NOT NULL DEFAULT '0',
  `account_number` char(32) NOT NULL COMMENT 'Possible account number (auto-generated)',
  `account_name` varchar(50) NOT NULL,
  `is_active` tinyint unsigned NOT NULL DEFAULT '1' COMMENT 'Allow track if account is active or de-activated (non payment). Inactive account cannot login.',
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `is_deleted` tinyint unsigned NOT NULL DEFAULT '0',
  `timezone_name` varchar(50) NOT NULL COMMENT 'Timezone of the account.',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account`
--

LOCK TABLES `account` WRITE;
/*!40000 ALTER TABLE `account` DISABLE KEYS */;
INSERT INTO `account` VALUES (1,1,0,'7d6ad4d080c911eab51c0aedbe94','Truffles Cafe',1,'2020-04-17 16:35:46',NULL,0,''),(2,5,0,'b893684f82a711eab51c0aedbe94','Truffles Truck 2',1,'2020-04-20 01:39:05',NULL,0,''),(3,6,0,'2789b95682a911eab51c0aedbe94','Truffles Cafe Anvil Cntr',1,'2020-04-20 01:49:21',NULL,0,''),(4,8,0,'debddd3782a911eab51c0aedbe94','Oscar\'s Pub',1,'2020-04-20 01:54:28',NULL,0,''),(5,10,0,'8e87af2382aa11eab51c0aedbe94','FUUD FOODS',1,'2020-04-20 01:59:23',NULL,0,'');
/*!40000 ALTER TABLE `account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_plan`
--

DROP TABLE IF EXISTS `account_plan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_plan` (
  `id` smallint unsigned NOT NULL AUTO_INCREMENT,
  `plan_name` varchar(100) NOT NULL COMMENT 'Basic, Premium, Pro',
  `plan_price` decimal(5,2) unsigned NOT NULL,
  `total_unit` int unsigned NOT NULL DEFAULT '0',
  `length_measure` int DEFAULT NULL COMMENT 'Day, Week, Month',
  `is_active` tinyint unsigned NOT NULL DEFAULT '1' COMMENT 'Plan could be de-activated',
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Subscription plan for an account';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_plan`
--

LOCK TABLES `account_plan` WRITE;
/*!40000 ALTER TABLE `account_plan` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_plan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_subscription_period`
--

DROP TABLE IF EXISTS `account_subscription_period`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_subscription_period` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `account_id` int unsigned NOT NULL,
  `account_plan_id` smallint unsigned NOT NULL,
  `from_date` date NOT NULL,
  `thru_date` date DEFAULT NULL,
  `is_active` tinyint unsigned NOT NULL DEFAULT '1',
  `is_trial` tinyint unsigned NOT NULL DEFAULT '0',
  `is_delinquent` tinyint unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_account_subscription_period_account_plan` (`account_plan_id`),
  CONSTRAINT `fk_account_subscription_period_account_plan` FOREIGN KEY (`account_plan_id`) REFERENCES `account_plan` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Subscription period for an account.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_subscription_period`
--

LOCK TABLES `account_subscription_period` WRITE;
/*!40000 ALTER TABLE `account_subscription_period` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_subscription_period` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `address`
--

DROP TABLE IF EXISTS `address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `address` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `organization_id` int unsigned NOT NULL,
  `address_type_id` tinyint unsigned NOT NULL COMMENT 'Shipping, Business etc ...',
  `country_id` smallint unsigned NOT NULL,
  `address_name` varchar(100) NOT NULL,
  `address_name_additional` varchar(100) DEFAULT NULL,
  `postal_code` varchar(20) NOT NULL,
  `city_name` varchar(65) NOT NULL,
  `is_active` tinyint unsigned NOT NULL DEFAULT '1' COMMENT 'Business could move to another address, address could change.',
  `from_date` date NOT NULL COMMENT 'Active Address From Date',
  `thru_date` date DEFAULT NULL COMMENT 'Active at this address till.',
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `is_deleted` tinyint unsigned NOT NULL DEFAULT '0' COMMENT 'Soft delete.',
  PRIMARY KEY (`id`),
  KEY `fk_address_address_type` (`address_type_id`),
  KEY `fk_address_country` (`country_id`),
  CONSTRAINT `fk_address_address_type` FOREIGN KEY (`address_type_id`) REFERENCES `address_type` (`id`),
  CONSTRAINT `fk_address_country` FOREIGN KEY (`country_id`) REFERENCES `country` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1 COMMENT='Organization Address, Restaurant  Address, Invoice Ship To Address, etc ..';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `address`
--

LOCK TABLES `address` WRITE;
/*!40000 ALTER TABLE `address` DISABLE KEYS */;
INSERT INTO `address` VALUES (1,2,1,40,'310-6893 PRENTER',NULL,'BC V5E 4L3','BURNABY',1,'0000-00-00',NULL,'0000-00-00 00:00:00',NULL,0),(2,1,2,40,'555 BROOKSBANK BLD 2 /110',NULL,'BC V7J 3S5','NORTH VANCOUVER ',1,'0000-00-00',NULL,'0000-00-00 00:00:00',NULL,0),(3,4,3,40,'1346 KINGSWAY AVE PORT COQUITLAM',NULL,'BC V3C 6G4','COQUITLAM',1,'0000-00-00',NULL,'0000-00-00 00:00:00',NULL,0),(4,5,2,40,'555 BROOKSBANK BLD 2 /110',NULL,'BC V7J 3S5','NORTH VANCOUVER ',1,'0000-00-00',NULL,'0000-00-00 00:00:00',NULL,0),(5,6,2,40,'777 Columbia St',NULL,'BC V3M 1B6','New Westminster',1,'0000-00-00',NULL,'0000-00-00 00:00:00',NULL,0),(6,7,1,40,'7995 Rosewood Street',NULL,'BC V5E 2H4','BURNABY',1,'0000-00-00',NULL,'0000-00-00 00:00:00',NULL,0),(7,8,2,40,'3684 E Hastings St',NULL,'BC V5K 2A9','VANCOUVER',1,'0000-00-00',NULL,'0000-00-00 00:00:00',NULL,0),(8,9,1,40,'111-3191 THUNDERBIRD CRES',NULL,'BC V5A 3G1','BURNABY',1,'0000-00-00',NULL,'0000-00-00 00:00:00',NULL,0),(9,10,2,40,'111-3191 THUNDERBIRD CRES',NULL,'BC V5A 3G1','BURNABY',1,'0000-00-00',NULL,'0000-00-00 00:00:00',NULL,0),(10,2,2,40,'testPost',NULL,'testPost','testPost',1,'9999-01-01',NULL,'2020-04-28 11:05:54',NULL,0),(11,2,2,40,'testPost',NULL,'testPost','testPost',1,'9999-01-01',NULL,'2020-04-28 11:08:19',NULL,0),(12,2,2,40,'testPost',NULL,'testPost','testPost',1,'9999-01-01',NULL,'2020-04-28 11:09:42',NULL,1);
/*!40000 ALTER TABLE `address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `address_type`
--

DROP TABLE IF EXISTS `address_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `address_type` (
  `id` tinyint unsigned NOT NULL AUTO_INCREMENT,
  `address_type_name` varchar(35) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COMMENT='Business Address,  Invoice Ship To Address,  Billing Address';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `address_type`
--

LOCK TABLES `address_type` WRITE;
/*!40000 ALTER TABLE `address_type` DISABLE KEYS */;
INSERT INTO `address_type` VALUES (1,'Sold To Address','2020-04-17 16:40:59',NULL),(2,'Ship To Address','2020-04-17 16:40:59',NULL),(3,'Regular Address','2020-04-17 16:40:59',NULL);
/*!40000 ALTER TABLE `address_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('2fb465668819');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `country`
--

DROP TABLE IF EXISTS `country`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `country` (
  `id` smallint unsigned NOT NULL AUTO_INCREMENT,
  `country_name` varchar(100) NOT NULL,
  `country_code` char(3) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_code` (`country_code`)
) ENGINE=InnoDB AUTO_INCREMENT=250 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `country`
--

LOCK TABLES `country` WRITE;
/*!40000 ALTER TABLE `country` DISABLE KEYS */;
INSERT INTO `country` VALUES (1,'Andorra','and','2020-04-17 17:52:56','2020-04-17 17:52:56'),(2,'Afghanistan','afg','2020-04-17 17:52:56','2020-04-17 17:52:56'),(3,'Antigua and Barbuda','atg','2020-04-17 17:52:56','2020-04-17 17:52:56'),(4,'Anguilla','aia','2020-04-17 17:52:56','2020-04-17 17:52:56'),(5,'Albania','alb','2020-04-17 17:52:56','2020-04-17 17:52:56'),(6,'Armenia','arm','2020-04-17 17:52:56','2020-04-17 17:52:56'),(7,'Angola','ago','2020-04-17 17:52:56','2020-04-17 17:52:56'),(8,'Antarctica','ata','2020-04-17 17:52:56','2020-04-17 17:52:56'),(9,'Argentina','arg','2020-04-17 17:52:56','2020-04-17 17:52:56'),(10,'American Samoa','asm','2020-04-17 17:52:56','2020-04-17 17:52:56'),(11,'Australia','aus','2020-04-17 17:52:56','2020-04-17 17:52:56'),(12,'Aruba','abw','2020-04-17 17:52:56','2020-04-17 17:52:56'),(13,'?land Islands','ala','2020-04-17 17:52:56','2020-04-17 17:52:56'),(14,'Azerbaijan','aze','2020-04-17 17:52:56','2020-04-17 17:52:56'),(15,'Austria','aut','2020-04-17 17:52:56','2020-04-17 17:52:56'),(16,'Algeria','dza','2020-04-17 17:52:56','2020-04-17 17:52:56'),(17,'Bahamas','bhs','2020-04-17 17:52:56','2020-04-17 17:52:56'),(18,'Bahrain','bhr','2020-04-17 17:52:56','2020-04-17 17:52:56'),(19,'Bangladesh','bgd','2020-04-17 17:52:56','2020-04-17 17:52:56'),(20,'Barbados','brb','2020-04-17 17:52:56','2020-04-17 17:52:56'),(21,'Belarus','blr','2020-04-17 17:52:56','2020-04-17 17:52:56'),(22,'Belgium','bel','2020-04-17 17:52:56','2020-04-17 17:52:56'),(23,'Belize','blz','2020-04-17 17:52:56','2020-04-17 17:52:56'),(24,'Benin','ben','2020-04-17 17:52:56','2020-04-17 17:52:56'),(25,'Bermuda','bmu','2020-04-17 17:52:56','2020-04-17 17:52:56'),(26,'Bhutan','btn','2020-04-17 17:52:56','2020-04-17 17:52:56'),(27,'Plurinational State of Bolivia','bol','2020-04-17 17:52:56','2020-04-17 17:52:56'),(28,'Sint Eustatius and Saba Bonaire','bes','2020-04-17 17:52:56','2020-04-17 17:52:56'),(29,'Bosnia and Herzegowina','bih','2020-04-17 17:52:56','2020-04-17 17:52:56'),(30,'Botswana','bwa','2020-04-17 17:52:56','2020-04-17 17:52:56'),(31,'Bouvet Island','bvt','2020-04-17 17:52:56','2020-04-17 17:52:56'),(32,'Brazil','bra','2020-04-17 17:52:56','2020-04-17 17:52:56'),(33,'British Indian Ocean Territory','iot','2020-04-17 17:52:56','2020-04-17 17:52:56'),(34,'Brunei Darussalam','brn','2020-04-17 17:52:56','2020-04-17 17:52:56'),(35,'Bulgaria','bgr','2020-04-17 17:52:56','2020-04-17 17:52:56'),(36,'Burkina Faso','bfa','2020-04-17 17:52:56','2020-04-17 17:52:56'),(37,'Burundi','bdi','2020-04-17 17:52:56','2020-04-17 17:52:56'),(38,'Cambodia','khm','2020-04-17 17:52:56','2020-04-17 17:52:56'),(39,'Cameroon','cmr','2020-04-17 17:52:56','2020-04-17 17:52:56'),(40,'Canada','can','2020-04-17 17:52:56','2020-04-17 17:52:56'),(41,'Cape Verde','cpv','2020-04-17 17:52:56','2020-04-17 17:52:56'),(42,'Cayman Islands','cym','2020-04-17 17:52:56','2020-04-17 17:52:56'),(43,'Central African Republic','caf','2020-04-17 17:52:56','2020-04-17 17:52:56'),(44,'Chad','tcd','2020-04-17 17:52:56','2020-04-17 17:52:56'),(45,'Chile','chl','2020-04-17 17:52:56','2020-04-17 17:52:56'),(46,'China','chn','2020-04-17 17:52:56','2020-04-17 17:52:56'),(47,'Christmas Island','cxr','2020-04-17 17:52:56','2020-04-17 17:52:56'),(48,'Cocos  Islands','cck','2020-04-17 17:52:56','2020-04-17 17:52:56'),(49,'Colombia','col','2020-04-17 17:52:56','2020-04-17 17:52:56'),(50,'Comoros','com','2020-04-17 17:52:56','2020-04-17 17:52:56'),(51,'Congo','cog','2020-04-17 17:52:56','2020-04-17 17:52:56'),(52,'The Democratic Republic of The Congo','cod','2020-04-17 17:52:56','2020-04-17 17:52:56'),(53,'Cook Islands','cok','2020-04-17 17:52:56','2020-04-17 17:52:56'),(54,'Costa Rica','cri','2020-04-17 17:52:56','2020-04-17 17:52:56'),(55,'C?te d\'Ivoire','civ','2020-04-17 17:52:56','2020-04-17 17:52:56'),(56,'Croatia ','hrv','2020-04-17 17:52:56','2020-04-17 17:52:56'),(57,'Cuba','cub','2020-04-17 17:52:56','2020-04-17 17:52:56'),(58,'Cura?ao','cuw','2020-04-17 17:52:56','2020-04-17 17:52:56'),(59,'Cyprus','cyp','2020-04-17 17:52:56','2020-04-17 17:52:56'),(60,'Czech Republic','cze','2020-04-17 17:52:56','2020-04-17 17:52:56'),(61,'Denmark','dnk','2020-04-17 17:52:56','2020-04-17 17:52:56'),(62,'Djibouti','dji','2020-04-17 17:52:56','2020-04-17 17:52:56'),(63,'Dominica','dma','2020-04-17 17:52:56','2020-04-17 17:52:56'),(64,'Dominican Republic','dom','2020-04-17 17:52:56','2020-04-17 17:52:56'),(65,'Ecuador','ecu','2020-04-17 17:52:56','2020-04-17 17:52:56'),(66,'Egypt','egy','2020-04-17 17:52:56','2020-04-17 17:52:56'),(67,'El Salvador','slv','2020-04-17 17:52:56','2020-04-17 17:52:56'),(68,'Equatorial Guinea','gnq','2020-04-17 17:52:56','2020-04-17 17:52:56'),(69,'Eritrea','eri','2020-04-17 17:52:56','2020-04-17 17:52:56'),(70,'Estonia','est','2020-04-17 17:52:56','2020-04-17 17:52:56'),(71,'Ethiopia','eth','2020-04-17 17:52:56','2020-04-17 17:52:56'),(72,'Falkland Islands ','flk','2020-04-17 17:52:56','2020-04-17 17:52:56'),(73,'Faroe Islands','fro','2020-04-17 17:52:56','2020-04-17 17:52:56'),(74,'Fiji','fji','2020-04-17 17:52:56','2020-04-17 17:52:56'),(75,'Finland','fin','2020-04-17 17:52:56','2020-04-17 17:52:56'),(76,'France','fra','2020-04-17 17:52:56','2020-04-17 17:52:56'),(77,'French Guiana','guf','2020-04-17 17:52:56','2020-04-17 17:52:56'),(78,'French Polynesia','pyf','2020-04-17 17:52:56','2020-04-17 17:52:56'),(79,'French Southern Territories','atf','2020-04-17 17:52:56','2020-04-17 17:52:56'),(80,'Gabon','gab','2020-04-17 17:52:56','2020-04-17 17:52:56'),(81,'Gambia','gmb','2020-04-17 17:52:56','2020-04-17 17:52:56'),(82,'Georgia','geo','2020-04-17 17:52:56','2020-04-17 17:52:56'),(83,'Germany','deu','2020-04-17 17:52:56','2020-04-17 17:52:56'),(84,'Ghana','gha','2020-04-17 17:52:56','2020-04-17 17:52:56'),(85,'Gibraltar','gib','2020-04-17 17:52:56','2020-04-17 17:52:56'),(86,'Greece','grc','2020-04-17 17:52:56','2020-04-17 17:52:56'),(87,'Greenland','grl','2020-04-17 17:52:56','2020-04-17 17:52:56'),(88,'Grenada','grd','2020-04-17 17:52:56','2020-04-17 17:52:56'),(89,'Guadeloupe','glp','2020-04-17 17:52:56','2020-04-17 17:52:56'),(90,'Guam','gum','2020-04-17 17:52:56','2020-04-17 17:52:56'),(91,'Guatemala','gtm','2020-04-17 17:52:56','2020-04-17 17:52:56'),(92,'Guernsey','ggy','2020-04-17 17:52:56','2020-04-17 17:52:56'),(93,'Guinea','gin','2020-04-17 17:52:56','2020-04-17 17:52:56'),(94,'Guinea-bissau','gnb','2020-04-17 17:52:56','2020-04-17 17:52:56'),(95,'Guyana','guy','2020-04-17 17:52:56','2020-04-17 17:52:56'),(96,'Haiti','hti','2020-04-17 17:52:56','2020-04-17 17:52:56'),(97,'Heard and McDonald Islands','hmd','2020-04-17 17:52:56','2020-04-17 17:52:56'),(98,'Holy See ','vat','2020-04-17 17:52:56','2020-04-17 17:52:56'),(99,'Honduras','hnd','2020-04-17 17:52:56','2020-04-17 17:52:56'),(100,'Hong Kong','hkg','2020-04-17 17:52:56','2020-04-17 17:52:56'),(101,'Hungary','hun','2020-04-17 17:52:56','2020-04-17 17:52:56'),(102,'Iceland','isl','2020-04-17 17:52:56','2020-04-17 17:52:56'),(103,'India','ind','2020-04-17 17:52:56','2020-04-17 17:52:56'),(104,'Indonesia','idn','2020-04-17 17:52:56','2020-04-17 17:52:56'),(105,'Iran ','irn','2020-04-17 17:52:56','2020-04-17 17:52:56'),(106,'Iraq','irq','2020-04-17 17:52:56','2020-04-17 17:52:56'),(107,'Ireland','irl','2020-04-17 17:52:56','2020-04-17 17:52:56'),(108,'Isle of Man','imn','2020-04-17 17:52:56','2020-04-17 17:52:56'),(109,'Israel','isr','2020-04-17 17:52:56','2020-04-17 17:52:56'),(110,'Italy','ita','2020-04-17 17:52:56','2020-04-17 17:52:56'),(111,'Jamaica','jam','2020-04-17 17:52:56','2020-04-17 17:52:56'),(112,'Japan','jpn','2020-04-17 17:52:56','2020-04-17 17:52:56'),(113,'Jersey','jey','2020-04-17 17:52:56','2020-04-17 17:52:56'),(114,'Jordan','jor','2020-04-17 17:52:56','2020-04-17 17:52:56'),(115,'Kazakhstan','kaz','2020-04-17 17:52:56','2020-04-17 17:52:56'),(116,'Kenya','ken','2020-04-17 17:52:56','2020-04-17 17:52:56'),(117,'Kiribati','kir','2020-04-17 17:52:56','2020-04-17 17:52:56'),(118,'Democratic People\'s Republic of Korea','prk','2020-04-17 17:52:56','2020-04-17 17:52:56'),(119,'Republic of Korea','kor','2020-04-17 17:52:56','2020-04-17 17:52:56'),(120,'Kuwait','kwt','2020-04-17 17:52:56','2020-04-17 17:52:56'),(121,'Kyrgyzstan','kgz','2020-04-17 17:52:56','2020-04-17 17:52:56'),(122,'Lao People\'s Democratic Republic','lao','2020-04-17 17:52:56','2020-04-17 17:52:56'),(123,'Latvia','lva','2020-04-17 17:52:56','2020-04-17 17:52:56'),(124,'Lebanon','lbn','2020-04-17 17:52:56','2020-04-17 17:52:56'),(125,'Lesotho','lso','2020-04-17 17:52:56','2020-04-17 17:52:56'),(126,'Liberia','lbr','2020-04-17 17:52:56','2020-04-17 17:52:56'),(127,'Libya','lby','2020-04-17 17:52:56','2020-04-17 17:52:56'),(128,'Liechtenstein','lie','2020-04-17 17:52:56','2020-04-17 17:52:56'),(129,'Lithuania','ltu','2020-04-17 17:52:56','2020-04-17 17:52:56'),(130,'Luxembourg','lux','2020-04-17 17:52:56','2020-04-17 17:52:56'),(131,'Macao','mac','2020-04-17 17:52:56','2020-04-17 17:52:56'),(132,'The Former Yugoslav Republic of Macedonia','mkd','2020-04-17 17:52:56','2020-04-17 17:52:56'),(133,'Madagascar','mdg','2020-04-17 17:52:56','2020-04-17 17:52:56'),(134,'Malawi','mwi','2020-04-17 17:52:56','2020-04-17 17:52:56'),(135,'Malaysia','mys','2020-04-17 17:52:56','2020-04-17 17:52:56'),(136,'Maldives','mdv','2020-04-17 17:52:56','2020-04-17 17:52:56'),(137,'Mali','mli','2020-04-17 17:52:56','2020-04-17 17:52:56'),(138,'Malta','mlt','2020-04-17 17:52:56','2020-04-17 17:52:56'),(139,'Marshall Islands','mhl','2020-04-17 17:52:56','2020-04-17 17:52:56'),(140,'Martinique','mtq','2020-04-17 17:52:56','2020-04-17 17:52:56'),(141,'Mauritania','mrt','2020-04-17 17:52:56','2020-04-17 17:52:56'),(142,'Mauritius','mus','2020-04-17 17:52:56','2020-04-17 17:52:56'),(143,'Mayotte','myt','2020-04-17 17:52:56','2020-04-17 17:52:56'),(144,'Mexico','mex','2020-04-17 17:52:56','2020-04-17 17:52:56'),(145,'Federated States of Micronesia','fsm','2020-04-17 17:52:56','2020-04-17 17:52:56'),(146,'Republic of Moldova','mda','2020-04-17 17:52:56','2020-04-17 17:52:56'),(147,'Monaco','mco','2020-04-17 17:52:56','2020-04-17 17:52:56'),(148,'Mongolia','mng','2020-04-17 17:52:56','2020-04-17 17:52:56'),(149,'Montenegro','mne','2020-04-17 17:52:56','2020-04-17 17:52:56'),(150,'Montserrat','msr','2020-04-17 17:52:56','2020-04-17 17:52:56'),(151,'Morocco','mar','2020-04-17 17:52:56','2020-04-17 17:52:56'),(152,'Mozambique','moz','2020-04-17 17:52:56','2020-04-17 17:52:56'),(153,'Myanmar','mmr','2020-04-17 17:52:56','2020-04-17 17:52:56'),(154,'Namibia','nam','2020-04-17 17:52:56','2020-04-17 17:52:56'),(155,'Nauru','nru','2020-04-17 17:52:56','2020-04-17 17:52:56'),(156,'Nepal','npl','2020-04-17 17:52:56','2020-04-17 17:52:56'),(157,'Netherlands','nld','2020-04-17 17:52:56','2020-04-17 17:52:56'),(158,'New Caledonia','ncl','2020-04-17 17:52:56','2020-04-17 17:52:56'),(159,'New Zealand','nzl','2020-04-17 17:52:56','2020-04-17 17:52:56'),(160,'Nicaragua','nic','2020-04-17 17:52:56','2020-04-17 17:52:56'),(161,'Niger','ner','2020-04-17 17:52:56','2020-04-17 17:52:56'),(162,'Nigeria','nga','2020-04-17 17:52:56','2020-04-17 17:52:56'),(163,'Niue','niu','2020-04-17 17:52:56','2020-04-17 17:52:56'),(164,'Norfolk Island','nfk','2020-04-17 17:52:56','2020-04-17 17:52:56'),(165,'Northern Mariana Islands','mnp','2020-04-17 17:52:56','2020-04-17 17:52:56'),(166,'Norway','nor','2020-04-17 17:52:56','2020-04-17 17:52:56'),(167,'Oman','omn','2020-04-17 17:52:56','2020-04-17 17:52:56'),(168,'Pakistan','pak','2020-04-17 17:52:56','2020-04-17 17:52:56'),(169,'Palau','plw','2020-04-17 17:52:56','2020-04-17 17:52:56'),(170,'State of Palestine','pse','2020-04-17 17:52:56','2020-04-17 17:52:56'),(171,'Panama','pan','2020-04-17 17:52:56','2020-04-17 17:52:56'),(172,'Papua New Guinea','png','2020-04-17 17:52:56','2020-04-17 17:52:56'),(173,'Paraguay','pry','2020-04-17 17:52:56','2020-04-17 17:52:56'),(174,'Peru','per','2020-04-17 17:52:56','2020-04-17 17:52:56'),(175,'Philippines','phl','2020-04-17 17:52:56','2020-04-17 17:52:56'),(176,'Pitcairn','pcn','2020-04-17 17:52:56','2020-04-17 17:52:56'),(177,'Poland','pol','2020-04-17 17:52:56','2020-04-17 17:52:56'),(178,'Portugal','prt','2020-04-17 17:52:56','2020-04-17 17:52:56'),(179,'Puerto Rico','pri','2020-04-17 17:52:56','2020-04-17 17:52:56'),(180,'Qatar','qat','2020-04-17 17:52:56','2020-04-17 17:52:56'),(181,'R?union','reu','2020-04-17 17:52:56','2020-04-17 17:52:56'),(182,'Romania','rou','2020-04-17 17:52:56','2020-04-17 17:52:56'),(183,'Russian Federation','rus','2020-04-17 17:52:56','2020-04-17 17:52:56'),(184,'Rwanda','rwa','2020-04-17 17:52:56','2020-04-17 17:52:56'),(185,'Ascension and Tristan Da Cunha Saint Helena','shn','2020-04-17 17:52:56','2020-04-17 17:52:56'),(186,'Saint Barth?lemy','blm','2020-04-17 17:52:56','2020-04-17 17:52:56'),(187,'Saint Kitts and Nevis','kna','2020-04-17 17:52:56','2020-04-17 17:52:56'),(188,'Saint Lucia','lca','2020-04-17 17:52:56','2020-04-17 17:52:56'),(189,'Saint Pierre and Miquelon','spm','2020-04-17 17:52:56','2020-04-17 17:52:56'),(190,'Saint Vincent and The Grenadines','vct','2020-04-17 17:52:56','2020-04-17 17:52:56'),(191,'Samoa','wsm','2020-04-17 17:52:56','2020-04-17 17:52:56'),(192,'San Marino','smr','2020-04-17 17:52:56','2020-04-17 17:52:56'),(193,'Sao Tome and Principe','stp','2020-04-17 17:52:56','2020-04-17 17:52:56'),(194,'Saudi Arabia','sau','2020-04-17 17:52:56','2020-04-17 17:52:56'),(195,'Senegal','sen','2020-04-17 17:52:56','2020-04-17 17:52:56'),(196,'Serbia','srb','2020-04-17 17:52:56','2020-04-17 17:52:56'),(197,'Seychelles','syc','2020-04-17 17:52:56','2020-04-17 17:52:56'),(198,'Sierra Leone','sle','2020-04-17 17:52:56','2020-04-17 17:52:56'),(199,'Singapore','sgp','2020-04-17 17:52:56','2020-04-17 17:52:56'),(200,'Sint Maarten ','sxm','2020-04-17 17:52:56','2020-04-17 17:52:56'),(201,'Slovakia','svk','2020-04-17 17:52:56','2020-04-17 17:52:56'),(202,'Slovenia','svn','2020-04-17 17:52:56','2020-04-17 17:52:56'),(203,'Solomon Islands','slb','2020-04-17 17:52:56','2020-04-17 17:52:56'),(204,'Somalia','som','2020-04-17 17:52:56','2020-04-17 17:52:56'),(205,'South Africa','zaf','2020-04-17 17:52:56','2020-04-17 17:52:56'),(206,'South Georgia and The South Sandwich Islands','sgs','2020-04-17 17:52:56','2020-04-17 17:52:56'),(207,'South Sudan','ssd','2020-04-17 17:52:56','2020-04-17 17:52:56'),(208,'Spain','esp','2020-04-17 17:52:56','2020-04-17 17:52:56'),(209,'Sri Lanka','lka','2020-04-17 17:52:56','2020-04-17 17:52:56'),(210,'Sudan','sdn','2020-04-17 17:52:56','2020-04-17 17:52:56'),(211,'Suriname','sur','2020-04-17 17:52:56','2020-04-17 17:52:56'),(212,'Svalbard and Jan Mayen Islands','sjm','2020-04-17 17:52:56','2020-04-17 17:52:56'),(213,'Swaziland','swz','2020-04-17 17:52:56','2020-04-17 17:52:56'),(214,'Sweden','swe','2020-04-17 17:52:56','2020-04-17 17:52:56'),(215,'Switzerland','che','2020-04-17 17:52:56','2020-04-17 17:52:56'),(216,'Syrian Arab Republic','syr','2020-04-17 17:52:56','2020-04-17 17:52:56'),(217,'Province of China Taiwan','twn','2020-04-17 17:52:56','2020-04-17 17:52:56'),(218,'Tajikistan','tjk','2020-04-17 17:52:56','2020-04-17 17:52:56'),(219,'United Republic of Tanzania','tza','2020-04-17 17:52:56','2020-04-17 17:52:56'),(220,'Thailand','tha','2020-04-17 17:52:56','2020-04-17 17:52:56'),(221,'Timor-leste','tls','2020-04-17 17:52:56','2020-04-17 17:52:56'),(222,'Togo','tgo','2020-04-17 17:52:56','2020-04-17 17:52:56'),(223,'Tokelau','tkl','2020-04-17 17:52:56','2020-04-17 17:52:56'),(224,'Tonga','ton','2020-04-17 17:52:56','2020-04-17 17:52:56'),(225,'Trinidad and Tobago','tto','2020-04-17 17:52:56','2020-04-17 17:52:56'),(226,'Tunisia','tun','2020-04-17 17:52:56','2020-04-17 17:52:56'),(227,'Turkey','tur','2020-04-17 17:52:56','2020-04-17 17:52:56'),(228,'Turkmenistan','tkm','2020-04-17 17:52:56','2020-04-17 17:52:56'),(229,'Turks and Caicos Islands','tca','2020-04-17 17:52:56','2020-04-17 17:52:56'),(230,'Tuvalu','tuv','2020-04-17 17:52:56','2020-04-17 17:52:56'),(231,'Uganda','uga','2020-04-17 17:52:56','2020-04-17 17:52:56'),(232,'Ukraine','ukr','2020-04-17 17:52:56','2020-04-17 17:52:56'),(233,'United Arab Emirates','are','2020-04-17 17:52:56','2020-04-17 17:52:56'),(234,'United Kingdom','gbr','2020-04-17 17:52:56','2020-04-17 17:52:56'),(235,'United States','usa','2020-04-17 17:52:56','2020-04-17 17:52:56'),(236,'United States Minor Outlying Islands','umi','2020-04-17 17:52:56','2020-04-17 17:52:56'),(237,'Uruguay','ury','2020-04-17 17:52:56','2020-04-17 17:52:56'),(238,'Uzbekistan','uzb','2020-04-17 17:52:56','2020-04-17 17:52:56'),(239,'Vanuatu','vut','2020-04-17 17:52:56','2020-04-17 17:52:56'),(240,'Bolivarian Republic of Venezuela','ven','2020-04-17 17:52:56','2020-04-17 17:52:56'),(241,'Vietnam','vnm','2020-04-17 17:52:56','2020-04-17 17:52:56'),(242,'Virgin Islands (British)','vgb','2020-04-17 17:52:56','2020-04-17 17:52:56'),(243,'Virgin Islands (US)','vir','2020-04-17 17:52:56','2020-04-17 17:52:56'),(244,'Wallis and Futuna Islands','wlf','2020-04-17 17:52:56','2020-04-17 17:52:56'),(245,'Western Sahara','esh','2020-04-17 17:52:56','2020-04-17 17:52:56'),(246,'Yemen','yem','2020-04-17 17:52:56','2020-04-17 17:52:56'),(247,'Zambia','zmb','2020-04-17 17:52:56','2020-04-17 17:52:56'),(248,'Zimbabwe','zwe','2020-04-17 17:52:56','2020-04-17 17:52:56'),(249,'country_name','cou','0000-00-00 00:00:00','0000-00-00 00:00:00');
/*!40000 ALTER TABLE `country` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `country_import`
--

DROP TABLE IF EXISTS `country_import`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `country_import` (
  `SK_Country` int DEFAULT NULL,
  `CountryName` varchar(255) DEFAULT NULL,
  `Alpha3Code` char(3) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `country_import`
--

LOCK TABLES `country_import` WRITE;
/*!40000 ALTER TABLE `country_import` DISABLE KEYS */;
INSERT INTO `country_import` VALUES (0,'CountryName','Alp'),(1,'Andorra','and'),(2,'Afghanistan','afg'),(3,'Antigua and Barbuda','atg'),(4,'Anguilla','aia'),(5,'Albania','alb'),(6,'Armenia','arm'),(7,'Angola','ago'),(8,'Antarctica','ata'),(9,'Argentina','arg'),(10,'American Samoa','asm'),(11,'Australia','aus'),(12,'Aruba','abw'),(13,'?land Islands','ala'),(14,'Azerbaijan','aze'),(15,'Austria','aut'),(16,'Algeria','dza'),(17,'Bahamas','bhs'),(18,'Bahrain','bhr'),(19,'Bangladesh','bgd'),(20,'Barbados','brb'),(21,'Belarus','blr'),(22,'Belgium','bel'),(23,'Belize','blz'),(24,'Benin','ben'),(25,'Bermuda','bmu'),(26,'Bhutan','btn'),(27,'Plurinational State of Bolivia','bol'),(28,'Sint Eustatius and Saba Bonaire','bes'),(29,'Bosnia and Herzegowina','bih'),(30,'Botswana','bwa'),(31,'Bouvet Island','bvt'),(32,'Brazil','bra'),(33,'British Indian Ocean Territory','iot'),(34,'Brunei Darussalam','brn'),(35,'Bulgaria','bgr'),(36,'Burkina Faso','bfa'),(37,'Burundi','bdi'),(38,'Cambodia','khm'),(39,'Cameroon','cmr'),(40,'Canada','can'),(41,'Cape Verde','cpv'),(42,'Cayman Islands','cym'),(43,'Central African Republic','caf'),(44,'Chad','tcd'),(45,'Chile','chl'),(46,'China','chn'),(47,'Christmas Island','cxr'),(48,'Cocos  Islands','cck'),(49,'Colombia','col'),(50,'Comoros','com'),(51,'Congo','cog'),(52,'The Democratic Republic of The Congo','cod'),(53,'Cook Islands','cok'),(54,'Costa Rica','cri'),(55,'C?te d\'Ivoire','civ'),(56,'Croatia ','hrv'),(57,'Cuba','cub'),(58,'Cura?ao','cuw'),(59,'Cyprus','cyp'),(60,'Czech Republic','cze'),(61,'Denmark','dnk'),(62,'Djibouti','dji'),(63,'Dominica','dma'),(64,'Dominican Republic','dom'),(65,'Ecuador','ecu'),(66,'Egypt','egy'),(67,'El Salvador','slv'),(68,'Equatorial Guinea','gnq'),(69,'Eritrea','eri'),(70,'Estonia','est'),(71,'Ethiopia','eth'),(72,'Falkland Islands ','flk'),(73,'Faroe Islands','fro'),(74,'Fiji','fji'),(75,'Finland','fin'),(76,'France','fra'),(77,'French Guiana','guf'),(78,'French Polynesia','pyf'),(79,'French Southern Territories','atf'),(80,'Gabon','gab'),(81,'Gambia','gmb'),(82,'Georgia','geo'),(83,'Germany','deu'),(84,'Ghana','gha'),(85,'Gibraltar','gib'),(86,'Greece','grc'),(87,'Greenland','grl'),(88,'Grenada','grd'),(89,'Guadeloupe','glp'),(90,'Guam','gum'),(91,'Guatemala','gtm'),(92,'Guernsey','ggy'),(93,'Guinea','gin'),(94,'Guinea-bissau','gnb'),(95,'Guyana','guy'),(96,'Haiti','hti'),(97,'Heard and McDonald Islands','hmd'),(98,'Holy See ','vat'),(99,'Honduras','hnd'),(100,'Hong Kong','hkg'),(101,'Hungary','hun'),(102,'Iceland','isl'),(103,'India','ind'),(104,'Indonesia','idn'),(105,'Iran ','irn'),(106,'Iraq','irq'),(107,'Ireland','irl'),(108,'Isle of Man','imn'),(109,'Israel','isr'),(110,'Italy','ita'),(111,'Jamaica','jam'),(112,'Japan','jpn'),(113,'Jersey','jey'),(114,'Jordan','jor'),(115,'Kazakhstan','kaz'),(116,'Kenya','ken'),(117,'Kiribati','kir'),(118,'Democratic People\'s Republic of Korea','prk'),(119,'Republic of Korea','kor'),(120,'Kuwait','kwt'),(121,'Kyrgyzstan','kgz'),(122,'Lao People\'s Democratic Republic','lao'),(123,'Latvia','lva'),(124,'Lebanon','lbn'),(125,'Lesotho','lso'),(126,'Liberia','lbr'),(127,'Libya','lby'),(128,'Liechtenstein','lie'),(129,'Lithuania','ltu'),(130,'Luxembourg','lux'),(131,'Macao','mac'),(132,'The Former Yugoslav Republic of Macedonia','mkd'),(133,'Madagascar','mdg'),(134,'Malawi','mwi'),(135,'Malaysia','mys'),(136,'Maldives','mdv'),(137,'Mali','mli'),(138,'Malta','mlt'),(139,'Marshall Islands','mhl'),(140,'Martinique','mtq'),(141,'Mauritania','mrt'),(142,'Mauritius','mus'),(143,'Mayotte','myt'),(144,'Mexico','mex'),(145,'Federated States of Micronesia','fsm'),(146,'Republic of Moldova','mda'),(147,'Monaco','mco'),(148,'Mongolia','mng'),(149,'Montenegro','mne'),(150,'Montserrat','msr'),(151,'Morocco','mar'),(152,'Mozambique','moz'),(153,'Myanmar','mmr'),(154,'Namibia','nam'),(155,'Nauru','nru'),(156,'Nepal','npl'),(157,'Netherlands','nld'),(158,'New Caledonia','ncl'),(159,'New Zealand','nzl'),(160,'Nicaragua','nic'),(161,'Niger','ner'),(162,'Nigeria','nga'),(163,'Niue','niu'),(164,'Norfolk Island','nfk'),(165,'Northern Mariana Islands','mnp'),(166,'Norway','nor'),(167,'Oman','omn'),(168,'Pakistan','pak'),(169,'Palau','plw'),(170,'State of Palestine','pse'),(171,'Panama','pan'),(172,'Papua New Guinea','png'),(173,'Paraguay','pry'),(174,'Peru','per'),(175,'Philippines','phl'),(176,'Pitcairn','pcn'),(177,'Poland','pol'),(178,'Portugal','prt'),(179,'Puerto Rico','pri'),(180,'Qatar','qat'),(181,'R?union','reu'),(182,'Romania','rou'),(183,'Russian Federation','rus'),(184,'Rwanda','rwa'),(185,'Ascension and Tristan Da Cunha Saint Helena','shn'),(186,'Saint Barth?lemy','blm'),(187,'Saint Kitts and Nevis','kna'),(188,'Saint Lucia','lca'),(189,'Saint Pierre and Miquelon','spm'),(190,'Saint Vincent and The Grenadines','vct'),(191,'Samoa','wsm'),(192,'San Marino','smr'),(193,'Sao Tome and Principe','stp'),(194,'Saudi Arabia','sau'),(195,'Senegal','sen'),(196,'Serbia','srb'),(197,'Seychelles','syc'),(198,'Sierra Leone','sle'),(199,'Singapore','sgp'),(200,'Sint Maarten ','sxm'),(201,'Slovakia','svk'),(202,'Slovenia','svn'),(203,'Solomon Islands','slb'),(204,'Somalia','som'),(205,'South Africa','zaf'),(206,'South Georgia and The South Sandwich Islands','sgs'),(207,'South Sudan','ssd'),(208,'Spain','esp'),(209,'Sri Lanka','lka'),(210,'Sudan','sdn'),(211,'Suriname','sur'),(212,'Svalbard and Jan Mayen Islands','sjm'),(213,'Swaziland','swz'),(214,'Sweden','swe'),(215,'Switzerland','che'),(216,'Syrian Arab Republic','syr'),(217,'Province of China Taiwan','twn'),(218,'Tajikistan','tjk'),(219,'United Republic of Tanzania','tza'),(220,'Thailand','tha'),(221,'Timor-leste','tls'),(222,'Togo','tgo'),(223,'Tokelau','tkl'),(224,'Tonga','ton'),(225,'Trinidad and Tobago','tto'),(226,'Tunisia','tun'),(227,'Turkey','tur'),(228,'Turkmenistan','tkm'),(229,'Turks and Caicos Islands','tca'),(230,'Tuvalu','tuv'),(231,'Uganda','uga'),(232,'Ukraine','ukr'),(233,'United Arab Emirates','are'),(234,'United Kingdom','gbr'),(235,'United States','usa'),(236,'United States Minor Outlying Islands','umi'),(237,'Uruguay','ury'),(238,'Uzbekistan','uzb'),(239,'Vanuatu','vut'),(240,'Bolivarian Republic of Venezuela','ven'),(241,'Vietnam','vnm'),(242,'Virgin Islands (British)','vgb'),(243,'Virgin Islands (US)','vir'),(244,'Wallis and Futuna Islands','wlf'),(245,'Western Sahara','esh'),(246,'Yemen','yem'),(247,'Zambia','zmb'),(248,'Zimbabwe','zwe'),(1,'Andorra','and'),(2,'Afghanistan','afg'),(3,'Antigua and Barbuda','atg'),(4,'Anguilla','aia'),(5,'Albania','alb'),(6,'Armenia','arm'),(7,'Angola','ago'),(8,'Antarctica','ata'),(9,'Argentina','arg'),(10,'American Samoa','asm'),(11,'Australia','aus'),(12,'Aruba','abw');
/*!40000 ALTER TABLE `country_import` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `industry`
--

DROP TABLE IF EXISTS `industry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `industry` (
  `id` smallint unsigned NOT NULL AUTO_INCREMENT,
  `industry_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `industry`
--

LOCK TABLES `industry` WRITE;
/*!40000 ALTER TABLE `industry` DISABLE KEYS */;
INSERT INTO `industry` VALUES (1,'Restaurant'),(2,'industry_name');
/*!40000 ALTER TABLE `industry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order` (
  `account_number` varchar(32) DEFAULT NULL,
  `invoice_number` varchar(32) NOT NULL,
  `invoice_term_name` varchar(32) DEFAULT NULL,
  `invoice_date` varchar(32) DEFAULT NULL,
  `supplier` varchar(32) DEFAULT NULL,
  `customer_account_number` varchar(32) DEFAULT NULL,
  `vendor` varchar(32) DEFAULT NULL,
  `order_items` varchar(32) DEFAULT NULL,
  `raw_sold_to_info` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`invoice_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
/*!40000 ALTER TABLE `order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_item`
--

DROP TABLE IF EXISTS `order_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_item` (
  `order_item_id` varchar(32) NOT NULL,
  `item_number` varchar(32) DEFAULT NULL,
  `order_quantity` varchar(32) DEFAULT NULL,
  `shipped_quantity` varchar(32) DEFAULT NULL,
  `unit` varchar(32) DEFAULT NULL,
  `size` varchar(32) DEFAULT NULL,
  `brand` varchar(32) DEFAULT NULL,
  `description` varchar(32) DEFAULT NULL,
  `weight` varchar(32) DEFAULT NULL,
  `price` varchar(32) DEFAULT NULL,
  `total_price` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`order_item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_item`
--

LOCK TABLES `order_item` WRITE;
/*!40000 ALTER TABLE `order_item` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `organization`
--

DROP TABLE IF EXISTS `organization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `organization` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `parent_organization_id` int unsigned DEFAULT NULL,
  `organization_type_id` smallint unsigned NOT NULL COMMENT 'Zappo, Supplier, Restaurant (other industry)',
  `organization_number` varchar(32) NOT NULL DEFAULT '',
  `industry_id` smallint unsigned NOT NULL,
  `organization_name` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `website_url` varchar(65) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `is_deleted` tinyint unsigned NOT NULL DEFAULT '0',
  `timezone_name` varchar(50) NOT NULL DEFAULT 'Pacific Daylight Time/Vancouver',
  PRIMARY KEY (`id`),
  KEY `fk_organization_organization_type` (`organization_type_id`),
  KEY `fk_organization_industry` (`industry_id`),
  KEY `idx_org_number` (`organization_number`),
  KEY `idx_parent_id` (`parent_organization_id`),
  CONSTRAINT `fk_organization_industry` FOREIGN KEY (`industry_id`) REFERENCES `industry` (`id`),
  CONSTRAINT `fk_organization_organization_type` FOREIGN KEY (`organization_type_id`) REFERENCES `organization_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `organization`
--

LOCK TABLES `organization` WRITE;
/*!40000 ALTER TABLE `organization` DISABLE KEYS */;
INSERT INTO `organization` VALUES (1,2,2,'d0a6750c85ce11eab51c0aedbe94',1,'Truffles Cafe',NULL,'2020-04-17 16:33:36',NULL,0,'Pacific Daylight Time/Vancouver'),(2,NULL,4,'d589cb7d85ce11eab51c0aedbe94',1,'TRUFFLES FINE FOODS LTD.',NULL,'2020-04-17 16:33:36',NULL,0,'Pacific Daylight Time/Vancouver'),(3,NULL,3,'d69e334c85ce11eab51c0aedbe94',1,'Sysco Canada, Inc',NULL,'2020-04-17 16:33:36',NULL,0,'Pacific Daylight Time/Vancouver'),(4,3,3,'d7a8755d85ce11eab51c0aedbe94',1,'Sysco Vancouver',NULL,'2020-04-17 16:33:36',NULL,0,'Pacific Daylight Time/Vancouver'),(5,2,2,'d8c2411685ce11eab51c0aedbe94',1,'Truffles Truck 2',NULL,'2020-04-20 01:35:47',NULL,0,'Pacific Daylight Time/Vancouver'),(6,2,2,'da707ff085ce11eab51c0aedbe94',1,'Truffles Cafe Anvil Cntr',NULL,'2020-04-20 01:49:04',NULL,0,'Pacific Daylight Time/Vancouver'),(7,NULL,4,'dbc2dee985ce11eab51c0aedbe94',1,'Oscar\'s Pub',NULL,'2020-04-20 01:52:56',NULL,0,'Pacific Daylight Time/Vancouver'),(8,7,2,'dcefc9fe85ce11eab51c0aedbe94',1,'Oscar\'s Pub',NULL,'2020-04-20 01:54:01',NULL,0,'Pacific Daylight Time/Vancouver'),(9,NULL,4,'de41cffc85ce11eab51c0aedbe94',1,'FUUD FOODS INC.',NULL,'2020-04-20 01:58:17',NULL,0,'Pacific Daylight Time/Vancouver'),(10,9,2,'dfa9dd2f85ce11eab51c0aedbe94',1,'FUUD FOODS',NULL,'2020-04-20 01:58:56',NULL,0,'Pacific Daylight Time/Vancouver'),(11,NULL,3,'f0dba2fd0e8f9bd6bddaab9e2229',1,'Gordon Food Service',NULL,'2020-05-03 20:08:53',NULL,0,'Pacific Daylight Time/Vancouver'),(12,NULL,3,'2c9fb715f5c21ec8f8618efd31b7',1,'Freshpoint Canada',NULL,'2020-05-03 20:10:13',NULL,0,'Pacific Daylight Time/Vancouver'),(13,NULL,3,'d566b38ce530d52aee5dfcd684fe',1,'Cioffi\'s Group',NULL,'2020-05-03 20:10:15',NULL,0,'Pacific Daylight Time/Vancouver'),(14,NULL,3,'',1,'Snowcap Interior Food Services Ltd',NULL,'2020-05-03 20:10:15',NULL,1,'Pacific Daylight Time/Vancouver'),(15,NULL,3,'',1,'Cioffi\'s Group',NULL,'2020-05-03 20:10:17',NULL,1,'Pacific Daylight Time/Vancouver'),(16,NULL,3,'58af45984e59ab45ae500984e5d7',1,'Snowcap Interior Food Services Ltd',NULL,'2020-05-03 20:10:17',NULL,0,'Pacific Daylight Time/Vancouver');
/*!40000 ALTER TABLE `organization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `organization_type`
--

DROP TABLE IF EXISTS `organization_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `organization_type` (
  `id` smallint unsigned NOT NULL AUTO_INCREMENT,
  `organization_type_name` varchar(50) NOT NULL COMMENT 'Zappo, Supplier, Restaurant, Other (industries)',
  `is_active` tinyint unsigned NOT NULL DEFAULT '1' COMMENT 'Flag that states if ooganization type is active in the UI. (selectable)',
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1 COMMENT='Restaurant, Supplier, zappo_track, Accounting, ...';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `organization_type`
--

LOCK TABLES `organization_type` WRITE;
/*!40000 ALTER TABLE `organization_type` DISABLE KEYS */;
INSERT INTO `organization_type` VALUES (1,'Zappo Track',1,'2020-04-17 16:30:06',NULL),(2,'Restaurant',1,'2020-04-17 16:30:06',NULL),(3,'Supplier',1,'2020-04-17 16:30:06',NULL),(4,'Corporation',1,'2020-04-17 16:30:06',NULL),(5,'organization_type_name',0,'0000-00-00 00:00:00','0000-00-00 00:00:00');
/*!40000 ALTER TABLE `organization_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `person`
--

DROP TABLE IF EXISTS `person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `person` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `organization_id` int unsigned NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(65) NOT NULL,
  `username` varchar(65) NOT NULL,
  `password` varchar(100) NOT NULL,
  `is_active` tinyint unsigned NOT NULL DEFAULT '1',
  `created_at` datetime NOT NULL,
  `udpated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='A person (user) who works for an organization (restaurant, supplier, zappotrack ...).';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `person`
--

LOCK TABLES `person` WRITE;
/*!40000 ALTER TABLE `person` DISABLE KEYS */;
/*!40000 ALTER TABLE `person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `person_account`
--

DROP TABLE IF EXISTS `person_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `person_account` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `account_id` int unsigned NOT NULL,
  `person_id` int unsigned NOT NULL,
  `is_admin` tinyint unsigned NOT NULL DEFAULT '1',
  `role_name` varchar(100) NOT NULL DEFAULT 'Viewer',
  `from_date` datetime NOT NULL,
  `thru_date` datetime DEFAULT NULL,
  `is_active` tinyint unsigned NOT NULL DEFAULT '1',
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_person_account_person` (`person_id`),
  CONSTRAINT `fk_person_account_person` FOREIGN KEY (`person_id`) REFERENCES `person` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Associating a person to an account. An account can have multiple users, and a user can be associated to multiple accounts.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `person_account`
--

LOCK TABLES `person_account` WRITE;
/*!40000 ALTER TABLE `person_account` DISABLE KEYS */;
/*!40000 ALTER TABLE `person_account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `restaurant`
--

DROP TABLE IF EXISTS `restaurant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `restaurant` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `organization_id` int unsigned NOT NULL,
  `restaurant_name` varchar(100) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `is_deleted` tinyint unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `restaurant`
--

LOCK TABLES `restaurant` WRITE;
/*!40000 ALTER TABLE `restaurant` DISABLE KEYS */;
INSERT INTO `restaurant` VALUES (1,1,'Trffles Cafe','2020-04-17 16:30:06',NULL,0),(2,5,'Truffles Truck 2','2020-04-20 01:47:28',NULL,0),(3,6,'Truffles Cafe Anvil Cntr','2020-04-20 01:51:05',NULL,0),(4,8,'Oscar\'s Pub','2020-04-20 01:56:45',NULL,0),(5,10,'FUUD FOODS','2020-04-20 02:01:28',NULL,0),(6,0,'restaurant_name','0000-00-00 00:00:00','0000-00-00 00:00:00',0);
/*!40000 ALTER TABLE `restaurant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `supplier`
--

DROP TABLE IF EXISTS `supplier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `supplier` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `organization_id` int unsigned NOT NULL,
  `supplier_name` varchar(100) NOT NULL,
  `business_name` varchar(100) DEFAULT NULL,
  `template_name` varchar(100) DEFAULT NULL,
  `logo_path` varchar(100) DEFAULT NULL,
  `url` varchar(100) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `is_deleted` tinyint unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `supplier`
--

LOCK TABLES `supplier` WRITE;
/*!40000 ALTER TABLE `supplier` DISABLE KEYS */;
INSERT INTO `supplier` VALUES (1,4,'Sysco','Sysco Vancouver, Division of Sysco','sysco.json',NULL,NULL,'2020-04-17 16:40:59',NULL,0),(2,11,'GFS','Gordon Food Service','gfs.json',NULL,NULL,'2020-04-25 23:41:09',NULL,0),(3,12,'Freshpoint','Freshpoint Canada','freshpoint.json',NULL,NULL,'2020-04-25 23:42:11',NULL,0),(4,13,'Cioffi\'s Meat Market & Deli','Cioffi\'s Group','cioffi.json',NULL,NULL,'2020-04-25 23:43:12',NULL,0),(5,16,'Snowcap','Snowcap Interior Food Services Ltd','snowcap.json',NULL,NULL,'2020-04-25 23:43:52',NULL,0);
/*!40000 ALTER TABLE `supplier` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `firstName` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_user_firstName` (`firstName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `zappo_track`
--

DROP TABLE IF EXISTS `zappo_track`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `zappo_track` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `oganization_id` int unsigned NOT NULL,
  `name` varchar(100) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zappo_track`
--

LOCK TABLES `zappo_track` WRITE;
/*!40000 ALTER TABLE `zappo_track` DISABLE KEYS */;
/*!40000 ALTER TABLE `zappo_track` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-05-11 12:45:11
