-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: adhd_final_project
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
-- Table structure for table `nutrition_relief`
--

DROP TABLE IF EXISTS `nutrition_relief`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nutrition_relief` (
  `ID` int NOT NULL,
  `name` varchar(45) NOT NULL,
  `symptom` varchar(45) NOT NULL,
  `efficiency` float NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `treatment_idx` (`name`),
  CONSTRAINT `treatment` FOREIGN KEY (`name`) REFERENCES `nutritions` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nutrition_relief`
--

LOCK TABLES `nutrition_relief` WRITE;
/*!40000 ALTER TABLE `nutrition_relief` DISABLE KEYS */;
INSERT INTO `nutrition_relief` VALUES (1,'zinc','hyperactivity',0.26),(2,'zinc','impulsivity',0.18),(3,'iron','hyperactivity',0.63),(4,'iron','inattention',0.92),(5,'EFAs','hyperactivity',0.26),(6,'EFAs','inattention',0.48),(7,'pycnogenol','hyperactivity',0.87),(8,'pycnogenol','inattention',1),(9,'Ningdong','inattention',0.59),(10,'Ningdong','hyperactivity',0.59),(11,'Ningdong','impulsivity',0.59);
/*!40000 ALTER TABLE `nutrition_relief` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nutritions`
--

DROP TABLE IF EXISTS `nutritions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nutritions` (
  `ID` int NOT NULL,
  `name` varchar(45) NOT NULL,
  `dose` varchar(45) NOT NULL,
  `type` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nutritions`
--

LOCK TABLES `nutritions` WRITE;
/*!40000 ALTER TABLE `nutritions` DISABLE KEYS */;
INSERT INTO `nutritions` VALUES (1,'zinc','8 mg/day','Nutrients'),(2,'iron','10 mg/day','Nutrients'),(3,'EFAs','1.8 grams of total omega-3/day','Nutrients'),(4,'pycnogenol','1-2 pills','Herbs'),(5,'Ningdong','5 mg/day','Herbs');
/*!40000 ALTER TABLE `nutritions` ENABLE KEYS */;
UNLOCK TABLES;

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
  `symptom` varchar(45) DEFAULT NULL,
  `chat_recomendations` varchar(4096) DEFAULT NULL,
  `programm` varchar(4096) DEFAULT NULL,
  `criteria` varchar(256) DEFAULT NULL,
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
INSERT INTO `pupils` VALUES ('12478','3333888877','333879096','Yosi Biton',15,132,'MALE','hyperactivity/impulsivity','Here is a sample menu for a day that includes 8 mg of zinc, 10 mg of iron, and 1.8 grams of total omega-3 fatty acids:\n\nBreakfast:\n- 2 slices of whole grain toast with 1 tbsp peanut butter (contains 0.9 mg of zinc and 0.35 mg of iron)\n- 1 medium banana (contains 0.2 mg of zinc and 0.3 mg of iron)\n- 1 cup of unsweetened almond milk (contains 0.45 mg of zinc and 0.9 mg of iron)\n\nSnack:\n- 1/2 cup of roasted pumpkin seeds (contains 2.6 mg of zinc and 2.2 mg of iron)\n\nLunch:\n- Grilled salmon salad with mixed greens, cherry tomatoes, cucumbers, avocado, and a drizzle of lemon vinaigrette (contains approximately 1.5 grams of total omega-3 fatty acids, as well as 0.5 mg of zinc and 1.5 mg of iron)\n\nSnack:\n- 1 small apple with 1 tbsp almond butter (contains 0.2 mg of zinc)\n\nDinner:\n- Quinoa and black bean bowl with roasted sweet potatoes, sautéed kale, and a sprinkle of pumpkin seeds (contains approximately 0.3 mg of zinc, 3.6 mg of iron, and 0.3 grams of total omega-3 fatty acids)\n\nNote: The nutrient content of foods can vary depending on factors such as growing conditions, preparation methods, and serving sizes. Please consult with a registered dietitian to develop a personalized meal plan that meets your individual nutrient needs.\n\nNote: This menu is a general guideline and may not meet individual dietary needs. It is always a good idea to consult with a healthcare professional or a registered dietitian for personalized dietary recommendations.\n','ADHD treatment program for:\n\nName: Yosi Biton\nID: 12478\n\nRecommendations:\nDiagnosis: hyperactivity/impulsivity\n\nNutritional Supplements:\n- zinc: 8 mg/day. Expected improvement in hyperactivity is: 10.4\n- zinc: 8 mg/day. Expected improvement in impulsivity is: 7.2\n- iron: 10 mg/day. Expected improvement in hyperactivity is: 25.2\n- EFAs: 1.8 grams of total omega-3/day. Expected improvement in hyperactivity is: 10.4\n- pycnogenol: 1-2 pills. Expected improvement in hyperactivity is: 34.8\n- Ningdong: 5 mg/day. Expected improvement in hyperactivity is: 23.6\n- Ningdong: 5 mg/day. Expected improvement in impulsivity is: 23.6\n\nSports Activities:\n Dance/Yoga\n	On Wednesday\n Team Games\n	On Thursday\n','UNQUIET/DRIVENMOTOR/EXCESSIVETALK/BLURTING/IMPATIENT/INTRUDES'),('223654785','3697412853','333879096','Yosi Mualem',13,120,'MALE','hyperactivity/impulsivity','Breakfast:\n- Greek yogurt parfait with mixed berries and a sprinkle of chia seeds (contains zinc and omega-3)\n\nSnack:\n- A handful of pumpkin seeds (contains zinc and iron)\n\nLunch:\n- Grilled chicken salad with mixed greens, avocado, and a side of quinoa (contains zinc and iron)\n\nSnack:\n- Carrot sticks and hummus (contains zinc and omega-3)\n\nDinner:\n- Grilled salmon with roasted asparagus and sweet potato wedges (contains zinc, iron, and omega-3)\n\nNote: This menu is a general guideline and may not meet individual dietary needs. It is always a good idea to consult with a healthcare professional or a registered dietitian for personalized dietary recommendations.\n','ADHD treatment program for:\n\nName: Yosi Mualem\nID: 223654785\n\nRecommendations:\nDiagnosis: hyperactivity/impulsivity\n\nNutritional Supplements:\n- zinc: 8 mg/day. Expected improvement in hyperactivity is: 10.4\n- zinc: 8 mg/day. Expected improvement in impulsivity is: 7.2\n- iron: 10 mg/day. Expected improvement in hyperactivity is: 25.2\n- EFAs: 1.8 grams of total omega-3/day. Expected improvement in hyperactivity is: 10.4\n- pycnogenol: 1-2 pills. Expected improvement in hyperactivity is: 34.8\n- Ningdong: 5 mg/day. Expected improvement in hyperactivity is: 23.6\n- Ningdong: 5 mg/day. Expected improvement in impulsivity is: 23.6\n\nSports Activities:\n Martial arts\n	On Monday\n Team Games\n	On Thursday\n',NULL),('3423423','3697412853','333879096','wefwd',223,2342,'MALE','inattention','Breakfast:\n- Oatmeal with nuts and seeds (chia, flax, sunflower)\n- Glass of orange juice\n\nLunch:\n- Grilled salmon with quinoa and steamed broccoli\n- Fresh fruit salad (strawberries, blueberries, mango)\n\nDinner:\n- Beef stir-fry with spinach and brown rice\n- Side salad with almonds, avocado, and a vinaigrette dressing\n\nSnacks:\n- Apple slices with almond butter\n- Carrots and hummus\n- Trail mix with nuts, seeds, and dried fruit\n\nNote: This menu is a general guideline and may not meet individual dietary needs. It is always a good idea to consult with a healthcare professional or a registered dietitian for personalized dietary recommendations.\n','ADHD treatment program for:\n\nName: wefwd\nID: 3423423\n\nRecommendations:\nDiagnosis: inattention\n\nNutritional Supplements:\n- iron: 10 mg/day. Expected improvement in inattention is: 36.8\n- EFAs: 1.8 grams of total omega-3/day. Expected improvement in inattention is: 19.2\n- pycnogenol: 1-2 pills. Expected improvement in inattention is: 40.0\n- Ningdong: 5 mg/day. Expected improvement in inattention is: 23.6\n\nSports Activities:\n Team Games\n	On Tuesday\n Martial arts\n	On Wednesday\n','TASKFOCUS/CARELESS/UNORGAN/EASILYDISTRACT/NOTFINISH/FORGETFUL/RUNNINGCLIMBING/UNQUIET/DRIVENMOTOR/EXCESSIVETALK/BLURTING'),('34627128','666555444','333879096','Moshe Amar',13,130,'MALE','inattention','Breakfast:\n- Greek yogurt with 1 tablespoon of chia seeds and ½ cup of blueberries (contains 0.4 grams of omega-3s)\n- 2 slices of whole grain toast with avocado and a poached egg\n\nSnack:\n- 1 medium apple with 1 tablespoon of Almond butter (contains 0.07 grams of omega-3s)\n\nLunch:\n- Salad with 3 oz of spinach, 3 oz of chicken breast, 1 oz almonds, ½ cup of mandarin oranges with a tablespoon of olive oil and balsamic vinegar (contains 0.3 grams of omega-3s)\n\nSnack:\n- 1/2 cup of edamame (contains 0.5 grams of omega-3s)\n\nDinner:\n- 3 oz grilled salmon fillet with roasted vegetables (carrots, broccoli, and kale) drizzled with a tablespoon of olive oil (contains 1.3 grams of omega-3s)\n\nSnack:\n- 1 cup of air-popped popcorn sprinkled with ¼ teaspoon of salt and a tablespoon of olive oil\n\nNote: The above menu only provides 6.5 grams of Omega-3s. You can always add more food sources of omega-3s, such as flaxseed oil, walnuts, salmon, or mackerel to increase your intake. Consult with a registered dietitian or healthcare provider for individualized recommendations.\n\nNote: This menu is a general guideline and may not meet individual dietary needs. It is always a good idea to consult with a healthcare professional or a registered dietitian for personalized dietary recommendations.\n','ADHD treatment program for:\n\nName: Moshe Amar\nID: 34627128\n\nRecommendations:\nDiagnosis: inattention\n\nNutritional Supplements:\n- iron: 10 mg/day. Expected improvement in inattention is: 36.8\n- EFAs: 1.8 grams of total omega-3/day. Expected improvement in inattention is: 19.2\n- pycnogenol: 1-2 pills. Expected improvement in inattention is: 40.0\n- Ningdong: 5 mg/day. Expected improvement in inattention is: 23.6\n\nSports Activities:\n Aerobics\n	On Monday\n Martial arts\n	On Thursday\n',NULL);
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
INSERT INTO `users` VALUES ('3333888877','Moshe Biton','matatov.nikita@gmail.com','PARENT','0549026496'),('333879096','Nikita Matatov','docmat63@gmail.com','TEACHER','0549026400'),('3697412853','Ofer Mualem','nikita.matatov@gmail.com','PARENT','555647896'),('454879633','Elad','eladlichtenberg@gmail.com','TEACHER',NULL),('666555444','Shlomit Amar','qqnikita@gmail.com','PARENT','896748569'),('89698778','Moshe Biton','xfgsdfg','PARENT','0549026496');
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

-- Dump completed on 2023-06-26  0:43:45
