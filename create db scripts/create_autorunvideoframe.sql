CREATE TABLE `autorunvideoframe` (
  `cycle_id` int(11) NOT NULL,
  `video_id` int(11) NOT NULL,
  `frame_id` int(11) NOT NULL,
  `score` double DEFAULT NULL,
  PRIMARY KEY (`cycle_id`,`video_id`,`frame_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
