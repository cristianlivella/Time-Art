<?php
function led($ledId, $ledState) {
	if ($ledState==0) {
		$ledState = "off";
	}
	else {
		$ledState = "on";
	}
	file_get_contents("http://192.168.1.1$ledId?led$ledState");
	echo "led $ledId $ledState \n";
}

while (1==1) {
	led(1, 1);
	led(2, 0);
	sleep(1);
	led(1, 0);
	led(2, 1);
	sleep(1);
}
?>
