<?php
require_once dirname(__FILE__) . '/config.php';
if (!isset($_GET[secret])) {
	exit('And you are?');
}
?>
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<base href="<?php echo 'http://' . $_SERVER['SERVER_NAME'] . '/';?>">
		<title>Odds Comparison</title>
		<link rel="stylesheet" href="jquery.dataTables.css">
		<link rel="stylesheet" href="bootstrap.min.css">
		<script type="text/javascript" src="jquery-1.11.3.min.js"></script>
		<script type="text/javascript" src="bootstrap.min.js"></script>
	</head>
	<body>
		<div class="container">
		<?php
		if (isset($_GET['way']) && !empty($_GET['way'])) {
			$way = strtoupper(preg_replace('/[^a-z]/', '', $_GET['way']));
		} else {
			$way = "ASC";
		}
		if (isset($_GET['sort0']) || isset($_GET['sort1']) || isset($_GET['sort2']) || isset($_GET['sort3'])) {
			$sort = "ORDER BY";
			if (isset($_GET['sort0']) && !empty($_GET['sort0'])) {
				$sort0 = preg_replace('/[^a-z\_]/', '', $_GET['sort0']);
				$sort .= " " . $sort0 . " " . $way;
			}
			if (isset($_GET['sort1']) && !empty($_GET['sort1'])) {
				$sort1 = preg_replace('/[^a-z\_]/', '', $_GET['sort1']);
				$sort .= ", " . $sort1 . " " . $way;
			}
			if (isset($_GET['sort2']) && !empty($_GET['sort2'])) {
				$sort2 = preg_replace('/[^a-z\_]/', '', $_GET['sort2']);
				$sort .= ", " . $sort2 . " " . $way;
			}
			if (isset($_GET['sort3']) && !empty($_GET['sort3'])) {
				$sort3 = preg_replace('/[^a-z\_]/', '', $_GET['sort3']);
				$sort .= ", " . $sort3 . " " . $way;
			}
		} else {
			$sort = '';
		}
		if (isset($_GET['q']) && !empty($_GET['q'])) {
			$q = $dbh->real_escape_string(trim($_GET['q']));
			$filter = " WHERE player_name LIKE '%" . $q . "%'";
		} else {
			$filter = '';
		}
		$qo = $dbh->query("SELECT * FROM odds " . $filter . " " . $sort) or die ($dbh->error . ' in ' . __FILE__ . ' line ' . __LINE__);
		$co = $qo->num_rows;
		if ($co == 0) {
			echo '<div class="alert alert-danger">No records in the database!</div>';
		} else {
			echo '<h3 class="text-center">' . $co . ' records</h3>';
			echo '
			<form id="search-form" class="form form-horizontal" role="form" method="get" action="/">
				<input type="hidden" name="' . secret . '">
				<div class="form-group">
					<div class="col-sm-4">
						<label>Search by player name:</label>
						<input type="text" name="q" class="form-control"'; if (isset($_GET['q'])) { echo ' value="' . $_GET['q'] . '"'; } echo '>
					</div>
					<div class="col-sm-4">
						<label>Sort results:</label>
						<select name="way" class="form-control">
							<option value="asc"'; if (isset($_GET['way']) && $_GET['way'] == 'asc') { echo ' selected="selected"'; } echo '>Ascending</option>
							<option value="desc"'; if (isset($_GET['way']) && $_GET['way'] == 'desc') { echo ' selected="selected"'; } echo '>Descending</option>
						</select>
					</div>
					<div class="col-sm-4">
						<label>Sorting criteria:</label>
						<select name="sort0" class="form-control">
							<option value="player_name"'; if (isset($_GET['sort0']) && $_GET['sort0'] == 'player_name') { echo ' selected="selected"'; } echo '>Player Name</option>
							<option value="start_time"'; if (isset($_GET['sort0']) && $_GET['sort0'] == 'start_time') { echo ' selected="selected"'; } echo '>Start Time</option>
							<option value="bookie_name"'; if (isset($_GET['sort0']) && $_GET['sort0'] == 'bookie_name') { echo ' selected="selected"'; } echo '>Bookie</option>
							<option value="player_total"'; if (isset($_GET['sort0']) && $_GET['sort0'] == 'player_total') { echo ' selected="selected"'; } echo '>Total points</option>
						</select>
						<br>
						<select name="sort1" class="form-control">
							<option value="player_name"'; if (isset($_GET['sort1']) && $_GET['sort1'] == 'player_name') { echo ' selected="selected"'; } echo '>Player Name</option>
							<option value="start_time"'; if (isset($_GET['sort1']) && $_GET['sort1'] == 'start_time') { echo ' selected="selected"'; } echo '>Start Time</option>
							<option value="bookie_name"'; if (isset($_GET['sort1']) && $_GET['sort1'] == 'bookie_name') { echo ' selected="selected"'; } echo '>Bookie</option>
							<option value="player_total"'; if (isset($_GET['sort1']) && $_GET['sort1'] == 'player_total') { echo ' selected="selected"'; } echo '>Total points</option>
						</select>
						<br>
						<select name="sort2" class="form-control">
							<option value="player_name"'; if (isset($_GET['sort2']) && $_GET['sort2'] == 'player_name') { echo ' selected="selected"'; } echo '>Player Name</option>
							<option value="start_time"'; if (isset($_GET['sort2']) && $_GET['sort2'] == 'start_time') { echo ' selected="selected"'; } echo '>Start Time</option>
							<option value="bookie_name"'; if (isset($_GET['sort2']) && $_GET['sort2'] == 'bookie_name') { echo ' selected="selected"'; } echo '>Bookie</option>
							<option value="player_total"'; if (isset($_GET['sort2']) && $_GET['sort2'] == 'player_total') { echo ' selected="selected"'; } echo '>Total points</option>
						</select>
						<br>
						<select name="sort3" class="form-control">
							<option value="player_name"'; if (isset($_GET['sort3']) && $_GET['sort3'] == 'player_name') { echo ' selected="selected"'; } echo '>Player Name</option>
							<option value="start_time"'; if (isset($_GET['sort3']) && $_GET['sort3'] == 'start_time') { echo ' selected="selected"'; } echo '>Start Time</option>
							<option value="bookie_name"'; if (isset($_GET['sort3']) && $_GET['sort3'] == 'bookie_name') { echo ' selected="selected"'; } echo '>Bookie</option>
							<option value="player_total"'; if (isset($_GET['sort3']) && $_GET['sort3'] == 'player_total') { echo ' selected="selected"'; } echo '>Total points</option>
						</select>
					</div>
				</div>
				<hr>
				<div class="form-group text-center">
					<input type="submit" class="btn btn-default" value="Search">
					&nbsp;
					<a href="/index.php?' . secret . '" class="btn btn-success">Reset search form</a>
				</div>
			</form>
			<hr>
			<table class="table table-responsive">
				<thead>
					<tr>
						<th>Bookie</th>
						<th>Time</th>
						<th>Player</th>
						<th>Points</th>
						<th>Over</th>
						<th>Under</th>
						<th>Last update time</th>
					</tr>
				</thead>
				<tbody>
				';
				while ($ro = $qo->fetch_assoc()) {
					echo '
					<tr>
						<td>
							<a href="' . $ro['bookie_url'] . '" target="_blank">' . $ro['bookie_name'] . '</a>
						</td>
						<td>' . $ro['start_time'] . '</td>
						<td>' . $ro['player_name'] . '</td>
						<td>' . $ro['player_total'] . '</td>
						<td>' . $ro['over'] . '</td>
						<td>' . $ro['under'] . '</td>
						<td>' . date('Y-m-d H:i:s', $ro['date_time']) . '</td>
					</tr>
					';
				}
				echo '
				</tbody>
			</table>
			';
		}
		?>
		</div>
	</body>
</html>
