CREATE TABLE `videos` (
  `video_id` int(11) NOT NULL,
  `video_name` varchar(100) DEFAULT NULL,
  `num_of_frames` int(11) DEFAULT NULL,
  `video_path` varchar(200) DEFAULT NULL,
  `ffmpeg` int(11) DEFAULT NULL,
  PRIMARY KEY (`video_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
