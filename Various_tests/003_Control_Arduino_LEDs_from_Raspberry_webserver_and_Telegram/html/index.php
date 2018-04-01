<?php
require("config.php");
?>
<!doctype html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
		<title>Arduino control dashboard</title>
		<link href="css/bootstrap.min.css" rel="stylesheet">
		<link href="css/color-picker.min.css" rel="stylesheet">
		<link href="css/custom.css" rel="stylesheet">
	</head>
	<body>
		<header>
			<div class="navbar navbar-dark bg-dark box-shadow">
				<div class="container d-flex justify-content-between">
					<span class="navbar-brand d-flex align-items-center">
						<strong>Arduino control dashboard</strong>
					</span>
					<span class="navbar-brand d-flex align-items-center">
						<strong>v 1.0</strong>
					</span>
				</div>
			</div>
		</header>
		<main role="main">
			<div class="container main">
				<div class="row">
					<div class="col-md-4">
						<h2>LED RGB</h2>
						<div class="card mb-4 box-shadow color-picker-container">
							<section id="color-picker"></section>
						</div>
					</div>					 
					<div class="col-md-4">
						<h2>LED 1</h2>
						<div class="card mb-4 box-shadow">
							<img src="img/green_led.png"/ class="ledimg">
							<button id="led1on" type="button" class="btn btn-primary btnled">ON</button>
							<button id="led1off" type="button" class="btn btn-secondary btnled">OFF</button>
						</div>
					</div>
					<div class="col-md-4">
						<h2>LED 2</h2>
						<div class="card mb-4 box-shadow">
							<img src="img/red_led.png"/ class="ledimg">
							<button id="led2on" type="button" class="btn btn-primary btnled">ON</button>
							<button id="led2off" type="button" class="btn btn-secondary btnled">OFF</button>
						</div>
					</div>
				</div>
				<div class="row">
					<table class="table table-bordered">
						<thead>
							<tr>
								<th scope="col">IP</th>
								<th scope="col" class="center">Control</th>
								<th scope="col" class="center">Status</th>
								<th scope="col" class="center">LED RGB</th>
								<th scope="col" class="center">LED 1</th>
								<th scope="col" class="center">LED 2</th>
							</tr>
						</thead>
						<tbody>
							<?php
							foreach ($IPs as $thisKey => $thisIp) {
								?>
								<tr>
									<th><?php echo $thisIp;?></th>
									<td>
										<div class="form-check checkboxcontainer">
										<input class="form-check-input checkboxbig" type="checkbox" value="" id="controlCheck_<?php echo $thisKey;?>">
										</div>
									</td>
									<td><div id="status_<?php echo $thisKey;?>" class="circle"></div></td>
									<td><div id="rgb_<?php echo $thisKey;?>" class="circle"></div></td>
									<td><div id="led1_<?php echo $thisKey;?>" class="circle"></div></td>
									<td><div id="led2_<?php echo $thisKey;?>" class="circle"></div></td>
								</tr>	
								<?php
							}
							?>														
						</tbody>
					</table>
				</div>
			</div>
		</main>
		<script src="js/jquery.min.js"></script>
		<script src="js/popper.min.js"></script>
		<script src="js/bootstrap.min.js"></script>
		<script src="js/holder.min.js"></script>	
		<script src="js/color-picker.min.js"></script>
		<script>
		var led = [];
		var container = document.querySelector('#color-picker'),
			picker = new CP(container, false, container);
		picker.picker.classList.add('static');
		picker.enter();
		picker.on("change", function(color) {
			container.parentNode.style.backgroundColor = '#' + color;
			led = []
			for (i = 0; i < <?php echo count($IPs);?>; i++) { 
				if ($('#controlCheck_'+i).is(':checked')) {
					led.push(i);
				}
			}
			rgbUpdate(led, CP.HEX2RGB(color));
		});
		
		var updateCount = 0;
		var rgbCount = 0;
		
		function updateStatus() {
			$.ajax({
				type: "POST",
				url: "ajax/getStatus.php",
				dataType: "json",
				timeout: 10000,
				cache: false,
				success: function(data) {
					if (data) {
						if (data.length == <?php echo count($IPs);?>) {
							$(data).each(function(ledIndex, ledStatus) {
								if (ledStatus['status'] == 1) {									
									$("#status_"+ledIndex).css("background-color", "rgb(40, 168, 40)");
									$("#rgb_"+ledIndex).css("background-color", "rgb(" + ledStatus['LedR'] + ", " + ledStatus['LedG'] + ", " + ledStatus['LedB'] + ")");
									if (ledStatus['Led1']==1) {
										$("#led1_"+ledIndex).css("background-color", "rgb(40, 168, 40)");
									}
									else {
										$("#led1_"+ledIndex).css("background-color", "rgb(255, 255, 255)");
									}
									if (ledStatus['Led2']==1) {
										$("#led2_"+ledIndex).css("background-color", "rgb(255, 0, 0)");
									}
									else {
										$("#led2_"+ledIndex).css("background-color", "rgb(255, 255, 255)");
									}
									if (updateCount==0) {
										$("#controlCheck_"+ledIndex).prop('checked', true);
									}
								}
								else {
									$("#status_"+ledIndex).css("background-color", "rgb(255, 0, 0)");
									$("#rgb_"+ledIndex).css("background-color", "rgb(255, 255, 255");
									$("#led1_"+ledIndex).css("background-color", "rgb(255, 255, 255)");
									$("#led2_"+ledIndex).css("background-color", "rgb(255, 255, 255)");
									$("#controlCheck_"+ledIndex).prop('checked', false);
								}
							});
						}						
						updateCount++;
					}
				}
			});
		}
		
		function rgbUpdate(ledIndex, color) {			
			rgbCount++;
			var thisCount = rgbCount;
			setTimeout(function () {
				if (thisCount==rgbCount) {
					$.ajax({
						type: "POST",
						url: "ajax/update.php",
						dataType: "json",
						timeout: 10000,
						cache: false,
						data: {
							"update" : "rgb",
							"ledIndex" : ledIndex,
							"RGB" : color
						},
						success: function(data) {
							if (data) {
								updateStatus();
							}
						}
					});
				}
				
			}, 200);			
		}
		
		
		function ledUpdate(ledIndex, ledId, value) {
			$.ajax({
				type: "POST",
				url: "ajax/update.php",
				dataType: "json",
				timeout: 10000,
				cache: false,
				data: {
					"update" : "led",
					"ledIndex" : ledIndex,
					"ledId" : ledId,
					"value" : value
				},
				success: function(data) {
					if (data) {
						updateStatus();
					}
				}
			});				
		}
		
		$("#led1on").click(function() {
			led = []
			for (i = 0; i < <?php echo count($IPs);?>; i++) { 
				if ($('#controlCheck_'+i).is(':checked')) {
					led.push(i);
				}
			}
			ledUpdate(led, 1, 1);
		});
		
		$("#led1off").click(function() {
			led = []
			for (i = 0; i < <?php echo count($IPs);?>; i++) { 
				if ($('#controlCheck_'+i).is(':checked')) {
					led.push(i);
				}
			}
			ledUpdate(led, 1, 0);
		});
		
		$("#led2on").click(function() {
			led = []
			for (i = 0; i < <?php echo count($IPs);?>; i++) { 
				if ($('#controlCheck_'+i).is(':checked')) {
					led.push(i);
				}
			}
			ledUpdate(led, 2, 1);
		});
		
		$("#led2off").click(function() {
			led = []
			for (i = 0; i < <?php echo count($IPs);?>; i++) { 
				if ($('#controlCheck_'+i).is(':checked')) {
					led.push(i);
				}
			}
			ledUpdate(led, 2, 0);			
		});
		
		updateStatus();
		setInterval(updateStatus, 30000);
		</script>
	</body>
</html>
