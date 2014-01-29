CREATE TABLE `autorun` (
  `cycle_id` int(11) NOT NULL,
  `algo_version` double DEFAULT NULL,
  `params` varchar(45) DEFAULT NULL,
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  `avg_score` double DEFAULT NULL,
  PRIMARY KEY (`cycle_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
