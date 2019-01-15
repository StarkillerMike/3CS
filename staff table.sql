CREATE TABLE `staff` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `firstname` varchar(45) NOT NULL,
  `lastname` varchar(45) NOT NULL,
  `active` varchar(45) NOT NULL DEFAULT 'true',
  `married` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`,`firstname`,`lastname`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8