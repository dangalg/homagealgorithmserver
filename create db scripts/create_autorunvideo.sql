CREATE TABLE `autorunvideo` (
  `cycle_id` int(11) NOT NULL,
  `video_id` int(11) DEFAULT NULL,
  `average_score` double DEFAULT NULL,
  `exception` varchar(400) DEFAULT NULL,
  PRIMARY KEY (`cycle_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
