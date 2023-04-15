-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: localhost    Database: adhd_final_project
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `pupils`
--

DROP TABLE IF EXISTS `pupils`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pupils` (
  `id` varchar(10) NOT NULL,
  `parent_id` varchar(10) NOT NULL,
  `teacher_id` varchar(10) NOT NULL,
  `name` varchar(45) NOT NULL,
  `age` int NOT NULL,
  `height` int NOT NULL,
  `sex` enum('FEMALE','MALE') NOT NULL,
  `hystory_id` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `test_idx` (`parent_id`),
  KEY `teacher_idx` (`teacher_id`),
  CONSTRAINT `parent` FOREIGN KEY (`parent_id`) REFERENCES `users` (`personal_id`),
  CONSTRAINT `teacher` FOREIGN KEY (`teacher_id`) REFERENCES `users` (`personal_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pupils`
--

LOCK TABLES `pupils` WRITE;
/*!40000 ALTER TABLE `pupils` DISABLE KEYS */;
INSERT INTO `pupils` VALUES ('0001','214832663','333879096','Ted',11,140,'MALE',NULL),('0002','312364719','333879096','Lili',11,138,'FEMALE',NULL),('0003','772829002','454879633','Peter',12,136,'MALE',NULL);
/*!40000 ALTER TABLE `pupils` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pupils_symptom`
--

DROP TABLE IF EXISTS `pupils_symptom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pupils_symptom` (
  `pupil_id` varchar(10) NOT NULL,
  `symptom_id` int NOT NULL,
  PRIMARY KEY (`pupil_id`,`symptom_id`),
  KEY `symptom_idx` (`symptom_id`),
  CONSTRAINT `child` FOREIGN KEY (`pupil_id`) REFERENCES `pupils` (`id`),
  CONSTRAINT `symptom` FOREIGN KEY (`symptom_id`) REFERENCES `symptoms` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pupils_symptom`
--

LOCK TABLES `pupils_symptom` WRITE;
/*!40000 ALTER TABLE `pupils_symptom` DISABLE KEYS */;
/*!40000 ALTER TABLE `pupils_symptom` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `symptoms`
--

DROP TABLE IF EXISTS `symptoms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `symptoms` (
  `id` int NOT NULL,
  `name` varchar(45) NOT NULL,
  `description` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `symptoms`
--

LOCK TABLES `symptoms` WRITE;
/*!40000 ALTER TABLE `symptoms` DISABLE KEYS */;
INSERT INTO `symptoms` VALUES (1,'TASKFOCUS','Often has trouble staying focused on tasks at work, home, or play'),(2,'CARELESS','Frequently does not pay close attention to details or makes careless mistakes at work or while doing other tasks'),(3,'UNORGAN','Often has trouble organizing tasks or activities'),(4,'EASILYDISTRACT','Is easily distracted'),(5,'NOTFINISH','Frequently does not follow through on instructions or fails to complete work assignments, chores, or other activities'),(6,'FORGETFUL','Often forgets doing routine chores'),(7,'DISLIKEEFFORT','Avoids tasks that require long periods of mental focus'),(8,'LOSINGTHINGS','Often loses items needed to complete tasks or activities'),(9,'NOTLISTEN','Does not appear to be listening even when spoken to directly '),(10,'FIDGET','Often fidgets with or taps hands or feet or squirms in seat.'),(11,'UNSEATED','Often leaves seat in situations when remaining seated is expected'),(12,'RUNNINGCLIMBING','Often runs about or climbs in situations where it is inappropriate.  '),(13,'UNQUIET','Often unable to play or engage in leisure activities quietly. '),(14,'DRIVENMOTOR','Is often “on the go,” acting as if “driven by a motor” (e.g., is unable to remain still — in restaurants or meetings, '),(15,'EXCESSIVETALK','Often talks excessively. '),(16,'BLURTING','Often blurts out an answer before a question has been completed'),(17,'IMPATIENT','Often has difficulty waiting his or her turn'),(18,'INTRUDES','Often interrupts or intrudes on others (e.g., butts into conversations, games, or activities; '),(19,'ANXIETY',NULL),(20,'AGGRESSIVITY',NULL),(21,'ASOCIALITY',NULL);
/*!40000 ALTER TABLE `symptoms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `personal_id` varchar(10) NOT NULL,
  `name` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `permission` enum('TEACHER','PARENT') NOT NULL,
  `phone_number` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`personal_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('214832663','Alice','alice@gmail.com','PARENT',NULL),('312364719','Bob','bob@gmail.com','PARENT',NULL),('333879096','Nikita','docmat63@gmail.com','TEACHER',NULL),('454879633','Elad','elad@gmail.com','TEACHER',NULL),('772829002','Sean','sean@gmail.com','PARENT',NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-15 22:08:20
