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

// Test
$exec1 = shell_exec('ls');
$myfile1 = fopen("newfile1.txt", "w") or die("Unable to open file!");
fwrite($myfile1, $exec1);
fclose($myfile1);

/* Python scripts */
# $exec = shell_exec('./run-all');
#$exec = shell_exec('DISPLAY=:99 xvfb-run -a ./wwin-all.py');
#$exec = shell_exec('DISPLAY=:99 xvfb-run -a python3 wwin-all.py');
#$exec = shell_exec('sudo ./run-all');
$exec = shell_exec('cd ..; sudo ./run-all');

#$exec = shell_exec('DISPLAY=:99 xvfb-run -a firefox');
$myfile = fopen("newfile.txt", "w") or die("Unable to open file!");
fwrite($myfile, $exec);
fclose($myfile);

/* redirect to the html file */
if (!isset($_SERVER['SERVER_NAME'])) {
	exit;
} else {
	header('Location:index.php?' . secret);
}

?>
