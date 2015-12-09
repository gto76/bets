<?php

/* test if shell_exec() is enabled - this is a must to be able to exec phantomjs */
if (!function_exists('shell_exec')) {
	exit('Fatal error: In order to run this script the PHP "shell_exec()" function must be enabled!');
}

/* set memory limit to at least 256 MB, else script will run OOM */
ini_set('memory_limit', '256M');
ini_set('display_errors', 0);
ini_set('max_execution_time', 0);
date_default_timezone_set('Europe/Zagreb');

/* -> define functional variables */
define('secret', 'ThePostmanAlwaysRingsTwice');
define('path', dirname(__FILE__));
define('user_agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.13) Gecko/20080311 Firefox/2.0.0.13');
define('curlopt_timeout', 30);
define('curlopt_connect_timeout', 30);
define('system_architecture', php_uname('m'));
if (system_architecture == 'x86_64') {
	define('phantomjs', path . '/phantomjs-x86_64');
} else {
	define('phantomjs', path . '/phantomjs-i686');
}
define('DB_HOST', 'localhost');
define('DB_USER', 'denis');
define('DB_PASSWORD', 'Klada1977&');
define('DB_NAME', 'odds');
define('obsolete_time', 12*3600);
/* <- define functional variables */

/* -> define URLs to be scraped */
define('dvoznak_url', 'http://dvoznak.com/');
define('planetwin365_url', 'http://www.planetwin365.com/Sport/OddsAsync.aspx?eventid=176082');
define('bet1128_url', 'http://www.bet1128.com/en-GB/SportsBook/EventsOdds.aspx#4/events/2-254451-51129-0,');
define('parimatch_url', 'http://www.parimatchru.com/en/sport/basketbol/nba-duehl-igrokov-ochki');
/* <- define URLs to be scraped */

/* -> DB connection handle */
$dbh = new mysqli(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME) or die ($dbh->error . ' in ' . __FILE__ . ' line ' . __LINE__);
/* <- DB connection handle */

/* -> functions */
function get_html($url) { /* get the html content as string to be passed to simple_html_dom */
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_USERAGENT, user_agent);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
	curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
	curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, curlopt_connect_timeout);
	curl_setopt($ch, CURLOPT_TIMEOUT, curlopt_timeout);
	curl_setopt($ch, CURLOPT_COOKIEJAR, path . '/cookie.txt');
	curl_setopt($ch, CURLOPT_COOKIEFILE, path . '/cookie.txt');
	$string = curl_exec($ch);
	curl_close($ch);
	return $string;
}
/* <- functions */

?>
