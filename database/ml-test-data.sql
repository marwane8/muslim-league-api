
-- Muslim League Test Data 

INSERT INTO `season` VALUES (3,'Summer',2021);

INSERT INTO `players` VALUES (54,'Hassan Azeem',9,'C'),(55,'Mobeen Azeem',0,'F'),(56,'Azeem Indawala',25,'G'),(57,'Mohammad Shaikh',7,'G'),(58,'Abubaker Mohammed',1,'F'),(59,'Mohammed Sayeed',8,'G'),(60,'Hasnain Pathan',11,'F'),(61,'Emaad Mohammed',3,'G'),(62,'Mustakim Dalal',14,'G'),(63,'Faiz Bhinde',20,'G'),(64,'Hussein Mohamoud',13,'G'),(65,'Leban Mohamoud',15,'F'),(66,'Hassan Ismail',1,'F'),(67,'Ahmed Awale',0,'G'),(68,'Adam Dalmer',2,'G'),(69,'Ibrahim Mohamoud',3,'F'),(70,'Muse Mohamoud',5,'C'),(71,'Will Jackson',8,'F'),(72,'Zackeriah Muse',14,'F'),(73,'Mohamed Kane',23,'G');

INSERT INTO `teams` VALUES (16,3,'The Akatsuki',54,1,7,309,0),(17,3,'Dub Nation',NULL,4,4,352,0),(18,3,'Top Akhs',NULL,6,2,383,0),(19,3,'MaliWorld',64,5,3,357,0),(20,3,'The Moors',NULL,3,5,392,0),(21,3,'The Young Sahabs',NULL,5,3,276,0);

INSERT INTO `teams_players` VALUES (16,54),(16,55),(16,56),(16,57),(16,58),(16,59),(16,60),(16,61),(16,62),(16,63),(19,64),(19,65),(19,66),(19,67),(19,68),(19,69),(19,70),(19,71),(19,72),(19,73);

INSERT INTO `location` VALUES (13,'Vale Court 1','1280 Newfield St','Middletown','CT');

INSERT INTO `games` VALUES (12,16,19,13,20210619,'7:00 PM',NULL),(13,17,18,13,20210619,'8:00 PM',NULL),(14,20,21,13,20210619,'9:00 PM',NULL),(15,17,20,13,20210626,'7:00 PM',NULL),(16,19,21,13,20210626,'8:00 PM',NULL),(17,16,18,13,20210626,'9:00 PM',NULL),(18,16,21,13,20210703,'7:00 PM',NULL),(19,18,20,13,20210703,'8:00 PM',NULL),(20,17,19,13,20210703,'9:00 PM',NULL),(21,18,19,13,20210710,'7:00 PM',NULL),(22,17,21,13,20210710,'8:00 PM',NULL),(23,16,20,13,20210710,'9:00 PM',NULL),(24,18,21,13,20210717,'7:00 PM',NULL),(25,16,17,13,20210717,'8:00 PM',NULL),(26,19,20,13,20210717,'9:00 PM',NULL),(35,16,20,13,20210724,'7:00 PM',NULL),(36,19,21,13,20210724,'8:00 PM',NULL),(37,17,18,13,20210724,'9:00 PM',NULL),(38,18,16,13,20210731,'7:00 PM',NULL),(39,17,21,13,20210731,'8:00 PM',NULL),(40,20,19,13,20210731,'9:00 PM',NULL),(41,20,17,13,20210807,'7:00 PM',NULL),(42,18,19,13,20210807,'8:00 PM',NULL),(43,16,21,13,20210807,'9:00 PM',NULL);

INSERT INTO `statistics` VALUES (135,12,54,5,10,0),(136,12,55,3,3,2),(137,12,56,11,4,3),(138,12,57,0,2,0),(139,12,58,2,3,0),(140,12,59,10,5,0),(141,12,60,3,4,0),(142,12,61,17,3,2),(144,12,63,1,3,1),(145,12,64,3,1,0),(146,12,65,5,7,0),(147,12,66,2,0,2),(148,12,67,14,1,0),(149,12,68,7,9,1),(150,12,69,16,3,0),(151,12,70,6,6,2),(152,12,71,18,6,2);
