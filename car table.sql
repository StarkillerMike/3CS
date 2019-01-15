CREATE TABLE `car` (
  `carID` int(10) NOT NULL AUTO_INCREMENT,
  `ownerName` varchar(45) NOT NULL,
  `model` varchar(45) NOT NULL,
  `color` varchar(45) NOT NULL,
  PRIMARY KEY (`carID`,`ownerName`,`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8