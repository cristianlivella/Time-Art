<?php
require("../config.php");

if ($_POST['update']=="rgb") {
	foreach ($_POST['ledIndex'] as $thisLedId) {
		if (isset($IPs[$thisLedId])) {
			$R = $_POST['RGB'][0];
			$G = $_POST['RGB'][1];
			$B = $_POST['RGB'][2];
			$ch = curl_init();
			curl_setopt($ch, CURLOPT_URL, "http://".$IPs[$thisLedId]."?ledR=".$R."&ledG=".$G."&ledB=".$B);
			curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
			curl_setopt($ch, CURLOPT_CONNECTTIMEOUT_MS, 100);
			$output = curl_exec($ch);
			curl_close($ch);
		}
	}
}
elseif ($_POST['update']=="led") {
	foreach ($_POST['ledIndex'] as $thisLedId) {
		if (isset($IPs[$thisLedId])) {
			$ch = curl_init();
			curl_setopt($ch, CURLOPT_URL, "http://".$IPs[$thisLedId]."?led".$_POST['ledId']."=".$_POST['value']);
			curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
			curl_setopt($ch, CURLOPT_CONNECTTIMEOUT_MS, 100);
			$output = curl_exec($ch);
			curl_close($ch);
		}
	}
}

echo json_encode(print_r($_POST, true));