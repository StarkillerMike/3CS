CREATE TABLE `pets` (
  `petID` int(10) NOT NULL AUTO_INCREMENT,
  `ownerName` varchar(45) NOT NULL,
  `petName` varchar(45) NOT NULL,
  `color` varchar(45) NOT NULL,
  PRIMARY KEY (`petID`,`ownerName`,`petName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8