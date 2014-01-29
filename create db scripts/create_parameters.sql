CREATE TABLE `parameters` (
  `param_name` varchar(45) NOT NULL,
  `param_min` double DEFAULT NULL,
  `param_max` double DEFAULT NULL,
  `param_change` double DEFAULT NULL,
  `param_default` double DEFAULT NULL,
  PRIMARY KEY (`param_name`),
  UNIQUE KEY `param_name_UNIQUE` (`param_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
