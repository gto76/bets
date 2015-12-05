-- database name = odds

-- "SELECT * FROM odds WHERE bookie_url = '$bookie_url' AND player_name = '$player' AND start_time = '$time'"

-- "INSERT INTO odds (bookie_name, bookie_url, start_time, player_name, player_total, over, under, date_time) VALUES ('$bookie_name', '$bookie_url', '$time', '$player', " . $points . ", " . $over . ", " . $under . ", " . time() . ")"

-- "UPDATE odds SET player_name = '$player', player_total = " . $points . ", over = " . $over . ", under = " . $under . ", date_time = " . time() . " WHERE id = " . $rd['id']

-- odds:
--   bookie_name, bookie_url, start_time, player_name, player_total, over, under, date_time


CREATE TABLE IF NOT EXISTS `odds` (
  `odds_id` int(11) NOT NULL AUTO_INCREMENT,
  `bookie_name` varchar(100) NOT NULL,
  `bookie_url` varchar(300) NOT NULL,
  `start_time` datetime NOT NULL,
  `player_name` varchar(100) NOT NULL,
  `player_total` float(2,1) NOT NULL,
  `over` float(1,2) NOT NULL,
  `under` float(1,2) NOT NULL,
  `date_time` datetime NOT NULL,
  PRIMARY KEY (`odds_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 ;