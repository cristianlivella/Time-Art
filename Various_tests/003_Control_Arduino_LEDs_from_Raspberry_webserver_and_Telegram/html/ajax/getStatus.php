<?php
require("../config.php");
$array = array();
$id = 0;

foreach ($IPs as $thisKey => $thisIp) {
	$array[$id]['status'] = 0;
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, "http://".$thisIp);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($ch, CURLOPT_CONNECTTIMEOUT_MS, 200);
	$output = curl_exec($ch);
	curl_close($ch);
	if (strlen($output)>0) {
		$output = explode("-", $output);
		if (count($output)==6) {
			$array[$id]['status'] = 1;
			for ($x = 1; $x<6; $x++) {
				$explode = explode(":", $output[$x]);
				$array[$id][$explode[0]] = $explode[1];
			}
		}
	}
	$id++;
}

echo json_encode($array);
