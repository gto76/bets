<?php

require_once dirname(__FILE__) . '/config.php';
/* prevent random access */
if (isset($_SERVER['SERVER_NAME'])) {
	if (!isset($_GET[secret])) {
		exit('And you are?');
	}
}
require_once path . '/simple_html_dom.php';

/* create a cache directory for html if not exists */
if (!file_exists(path . '/html')) {
	mkdir(path . '/html');
}

/* clear obsolote records */
//$dbh->query("DELETE FROM odds WHERE date_time < (" . (time() - obsolete_time) . ")") or die ($dbh->error . ' in ' . __FILE__ . ' line ' . __LINE__);
$dbh->query("TRUNCATE TABLE `odds`") or die ($dhb->error . ' in ' . __FILE__ . ' line ' . __LINE__);

/* Python scripts */
$exec = shell_exec('cd ..; ./run-all');

/* -> planetwin365 */

$exec = shell_exec(phantomjs . ' planetwin365.js "' . planetwin365_url . '" "' . path . '/html/planetwin365.html" "' . user_agent . '"');
$html = str_get_html(file_get_contents(path . '/html/planetwin365.html'));
if (method_exists($html, 'find')) {
	$bookie_name = 'Planetwin365';
	$bookie_url = planetwin365_url;
	if ($html->find('tr[class=dgAItem],tr[class=dgItem]')) {
		foreach ($html->find('tr[class=dgAItem],tr[class=dgItem]') as $tr) {
			$time = str_replace('.', ':', trim($tr->find('td', 1)->plaintext)) ?: '';
			$player = $dbh->real_escape_string(trim($tr->find('td', 2)->plaintext)) ?: '';
			$odds = $tr->find('td', 3) ?: '';
			if ($odds->find('tr.OddsQuotaItemStyle')) {
				$tr = $odds->find('tr.OddsQuotaItemStyle', 0);
				if ($tr->find('td', 1)) {
					$points = (float)str_replace(',', '.', $tr->find('td', 1)->plaintext);
				} else {
					$points = 0;
				}
				if ($tr->find('td', 2)) {
					$over = (float)str_replace(',', '.', $tr->find('td', 2)->plaintext);
				} else {
					$over = 0;
				}
				if ($tr->find('td', 3)) {
					$under = (float)str_replace(',', '.', $tr->find('td', 3)->plaintext);
				} else {
					$under = 0;
				}
			}
			if (!empty($player) && $points > 0 && $over > 0 && $under > 0) {
				$qd = $dbh->query("SELECT * FROM odds WHERE bookie_url = '$bookie_url' AND player_name = '$player' AND start_time = '$time'") or die ($dbh->error . ' in ' . __FILE__ . ' line ' . __LINE__);
				$rd = $qd->fetch_assoc();
				if (is_null($rd)) {
					$dbh->query("INSERT INTO odds (bookie_name, bookie_url, start_time, player_name, player_total, over, under, date_time) VALUES ('$bookie_name', '$bookie_url', '$time', '$player', " . $points . ", " . $over . ", " . $under . ", " . time() . ")") or die ($dbh->error . ' in ' . __FILE__ . ' line ' . __LINE__);
				} else {
					$dbh->query("UPDATE odds SET player_name = '$player', player_total = " . $points . ", over = " . $over . ", under = " . $under . ", date_time = " . time() . " WHERE id = " . $rd['id']) or die ($dbh->error . ' in ' . __FILE__ . ' line ' . __LINE__);
				}
			}
		}
	}
}

/* <- planetwin365 */

/* -> dvoznak */

$str = get_html(dvoznak_url);
$html = str_get_html($str);
if (method_exists($html, 'find')) {
	if ($html->find('li#danas-sport-d_' . date('Y-m-d') . '-s_1-n_3970_i')) {
		foreach ($html->find('li#danas-sport-d_' . date('Y-m-d') . '-s_1-n_3970_i') as $li) {
			if ($li->find('a.s_item')) {
				foreach ($li->find('a.s_item') as $a) {
					$player_url = 'http://dvoznak.com/' . $a->href;
					$exec = shell_exec(phantomjs . ' --ignore-ssl-errors=true dvoznak.js "' . $player_url . '" "' . path . '/html/dvoznak.html" "' . user_agent . '"');
					$player_html = str_get_html(file_get_contents(path . '/html/dvoznak.html'));
					if (method_exists($player_html, 'find')) {
						if ($player_html->find('div#nazivigraca')) {
							$player = $dbh->real_escape_string(trim($player_html->find('div#nazivigraca', 0)->plaintext)) ?: '';
						} else {
							$player = '';
						}
						if ($player_html->find('span.nls_subt_left')) {
							$time = substr($player_html->find('span.nls_subt_left', 0)->plaintext, -5) ?: '';
						} else {
							$time = '';
						}
						if ($player_html->find('table#t14s1_sve_table_0')) {
							$table = $player_html->find('table#t14s1_sve_table_0', 0);
							if ($table->find('tr')) {
								foreach ($table->find('tr') as $tr) {
									if ($tr->find('td', 0)) {
										$bookie_name = $dbh->real_escape_string($tr->find('td', 0)->plaintext);	
									} else {
										$bookie_name = '';
									}
									if ($tr->find('a', 0)) {
										$bookie_url = $dbh->real_escape_string($tr->find('a', 0)->href);
									} else {
										$bookie_url = '';
									}
									if ($tr->find('td', 1)) {
										$points = (float)$tr->find('td', 1)->plaintext;
									} else {
										$points = 0;
									}
									if ($tr->find('td', 2)) {
										$over = (float)$tr->find('td', 2)->plaintext;
									} else {
										$over = 0;
									}
									if ($tr->find('td', 3)) {
										$under = (float)$tr->find('td', 3)->plaintext;
									} else {
										$under = 0;
									}
									if (!empty($player) && !empty($bookie_name) && $points > 0 && $over > 0 && $under > 0) {
										$qd = $dbh->query("SELECT * FROM odds WHERE bookie_url = '$bookie_url' AND player_name = '$player' AND start_time = '$time'") or die ($dbh->error . ' in ' . __FILE__ . ' line ' . __LINE__);
										$rd = $qd->fetch_assoc();
										if (is_null($rd)) {
											$dbh->query("INSERT INTO odds (bookie_name, bookie_url, start_time, player_name, player_total, over, under, date_time) VALUES ('$bookie_name', '$bookie_url', '$time', '$player', " . $points . ", " . $over . ", " . $under . ", " . time() . ")") or die ($dbh->error . ' in ' . __FILE__ . ' line ' . __LINE__);
										} else {
											$dbh->query("UPDATE odds SET player_name = '$player', player_total = " . $points . ", over = " . $over . ", under = " . $under . ", date_time = " . time() . " WHERE id = " . $rd['id']) or die ($dbh->error . ' in ' . __FILE__ . ' line ' . __LINE__);
										}
									}
								}
							}
						}
 						$player_html->clear();
					}
				}
			}
		}
	}
	$html->clear();
}

/* <- dvoznak */

/* -> bet1128 */

$exec = shell_exec(phantomjs . ' --ignore-ssl-errors=true bet1128.js "' . bet1128_url . '" "' . path . '/html/bet1128.html" "' . user_agent . '"');
$html = str_get_html(file_get_contents(path . '/html/bet1128.html'));
$players = array();
if (method_exists($html, 'find')) {
	if ($html->find('table.tournament-table')) {
		$tournament_table = $html->find('table.tournament-table', 0);
		if ($tournament_table->find('tr.event-row')) {
			$i = 0;
			foreach ($tournament_table->find('tr.event-row') as $tr) {
				$time = trim($tr->find('td', 1)->plaintext);
				$player = $dbh->real_escape_string($tr->find('td', 2)->plaintext);
				$players[$i]['time'] = $time;
				$players[$i]['player'] = $player;
				$i++;
			}
		}
		$odds_table = $html->find('table.tournament-table', 1);
		if ($odds_table->find('tr.event-row')) {
			$j = 0;
			foreach ($odds_table->find('tr.event-row') as $tr) {
				$points = (float)trim($tr->find('td', 0)->plaintext);
				$over = (float)trim($tr->find('td', 1)->plaintext);
				$under = (float)trim($tr->find('td', 2)->plaintext);
				$players[$j]['points'] = $points;
				$players[$j]['over'] = $over;
				$players[$j]['under'] = $under;
				$j++;
			}
		}
	}
	$html->clear();
}
$bookie_url = bet1128_url;
$bookie_name = 'Bet1128';
if (count($players) > 0) {
	foreach ($players as $key => $value) {
		if (!empty($value['player']) && $value['points'] > 0 && $value['over'] > 0 && $value['under'] > 0) {
			$player_name = $dbh->real_escape_string($value['player']);
			$time = $value['time'];
			$points = $value['points'];
			$over = $value['over'];
			$under = $value['under'];
			$qd = $dbh->query("SELECT * FROM odds WHERE bookie_url = '$bookie_url' AND player_name = '$player_name' AND start_time = '$time'") or die ($dbh->error . ' in ' . __FILE__ . ' line ' . __LINE__);
			$rd = $qd->fetch_assoc();
			if (is_null($rd)) {
				$dbh->query("INSERT INTO odds (bookie_name, bookie_url, start_time, player_name, player_total, over, under, date_time) VALUES ('$bookie_name', '$bookie_url', '$time', '$player_name', " . $points . ", " . $over . ", " . $under . ", " . time() . ")") or die ($dbh->error . ' in ' . __FILE__ . ' line ' . __LINE__);
			} else {
				$dbh->query("UPDATE odds SET player_name = '$player_name', player_total = " . $points . ", over = " . $over . ", under = " . $under . ", date_time = " . time() . " WHERE id = " . $rd['id']) or die ($dbh->error . ' in ' . __FILE__ . ' line ' . __LINE__);
			}
		}
	}
}
unset($players);

/* <- bet1128 */

/* -> parimatchru */

$exec = shell_exec(phantomjs . ' --ignore-ssl-errors=true parimatch.js "' . parimatch_url . '" "' . path . '/html/parimatch.html" "' . user_agent . '"');
$html = str_get_html(file_get_contents(path . '/html/parimatch.html'));
if (method_exists($html, 'find')) {
	if ($html->find('tr.bk')) {
		$bookie_url = parimatch_url;
		$bookie_name = 'ParimatchRu';
		foreach ($html->find('tr.bk') as $tr) {
			$time = substr($tr->find('td', 1)->plaintext, -5) ?: '';
			$players = explode('<br>', $tr->find('td', 2)->innertext);
			$player1 = $dbh->real_escape_string($players['0']);
			$player2 = $dbh->real_escape_string($players['1']);
			$points1 = (float)$tr->find('td', 11)->find('b', 0)->plaintext;
			$points2 = (float)$tr->find('td', 11)->find('b', 1)->plaintext;
			$over1 = (float)$tr->find('td', 12)->find('a', 0)->plaintext;
			$over2 = (float)$tr->find('td', 12)->find('a', 1)->plaintext;
			$under1 = (float)$tr->find('td', 13)->find('a', 0)->plaintext;
			$under2 = (float)$tr->find('td', 13)->find('a', 1)->plaintext;
			if (!empty($player1) && $points1 > 0 && $over1 > 0 && $under1 > 0) {
				$qd = $dbh->query("SELECT * FROM odds WHERE bookie_url = '$bookie_url' AND player_name = '$player1' AND start_time = '$time'") or die ($dbh->error . ' in ' . __FILE__ . ' line ' . __LINE__);
				$rd = $qd->fetch_assoc();
				if (is_null($rd)) {
					$dbh->query("INSERT INTO odds (bookie_name, bookie_url, start_time, player_name, player_total, over, under, date_time) VALUES ('$bookie_name', '$bookie_url', '$time', '$player1', " . $points1 . ", " . $over1 . ", " . $under1 . ", " . time() . ")") or die ($dbh->error . ' in ' . __FILE__ . ' line ' . __LINE__);
				} else {
					$dbh->query("UPDATE odds SET player_name = '$player1', player_total = " . $points1 . ", over = " . $over1 . ", under = " . $under1 . ", date_time = " . time() . " WHERE id = " . $rd['id']) or die ($dbh->error . ' in ' . __FILE__ . ' line ' . __LINE__);
				}
			}
			if (!empty($player2) && $points2 > 0 && $over2 > 0 && $under2 > 0) {
				$qd = $dbh->query("SELECT * FROM odds WHERE bookie_url = '$bookie_url' AND player_name = '$player2' AND start_time = '$time'") or die ($dbh->error . ' in ' . __FILE__ . ' line ' . __LINE__);
				$rd = $qd->fetch_assoc();
				if (is_null($rd)) {
					$dbh->query("INSERT INTO odds (bookie_name, bookie_url, start_time, player_name, player_total, over, under, date_time) VALUES ('$bookie_name', '$bookie_url', '$time', '$player2', " . $points2 . ", " . $over2 . ", " . $under2 . ", " . time() . ")") or die ($dbh->error . ' in ' . __FILE__ . ' line ' . __LINE__);
				} else {
					$dbh->query("UPDATE odds SET player_name = '$player2', player_total = " . $points2 . ", over = " . $over2 . ", under = " . $under2 . ", date_time = " . time() . " WHERE id = " . $rd['id']) or die ($dbh->error . ' in ' . __FILE__ . ' line ' . __LINE__);
				}
			}
		}
	}
	$html->clear();
}

/* <- parimatchru */


/* clear the html cached files */
$cache = scandir(path . '/html');
foreach ($cache as $key => $value) {
	if ($value != '.' && $value != '..') {
		@unlink(path . '/html/' . $value);
	}
}

/* redirect to the html file */
if (!isset($_SERVER['SERVER_NAME'])) {
	exit;
} else {
	header('Location:index.php?' . secret);
}

?>
