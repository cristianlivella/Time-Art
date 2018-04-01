<?php
include("config.php");

function getUpdate() {
	global $offset, $telegramToken;
	$parameters = ['method' => 'getUpdates', 'offset' => $offset];
	$handle = curl_init("https://api.telegram.org/bot".$telegramToken."/");
	curl_setopt($handle, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($handle, CURLOPT_CONNECTTIMEOUT, 5);
	curl_setopt($handle, CURLOPT_TIMEOUT, 60);
	curl_setopt($handle, CURLOPT_POSTFIELDS, json_encode($parameters));
	curl_setopt($handle, CURLOPT_HTTPHEADER, array("Content-Type: application/json"));
	curl_setopt($handle, CURLOPT_SSL_VERIFYPEER, false);
	$file = curl_exec($handle);
	$file = json_decode($file, true);
	if (!empty($file) AND isset($file['result']) AND count($file['result'])>0) {
		$offset = $file['result'][count($file['result'])-1]['update_id']+1;
		return $file['result'];
	}
	else {
		return array();
	}
}

function sendMessage($chatid, $message) {
	global $telegramToken;
	$parameters = ['chat_id' => $chatid, 'parse_mode' => 'markdown', 'text' => $message, 'method' => 'sendMessage'];
	$handle = curl_init("https://api.telegram.org/bot".$telegramToken."/");
	curl_setopt($handle, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($handle, CURLOPT_CONNECTTIMEOUT, 5);
	curl_setopt($handle, CURLOPT_TIMEOUT, 60);
	curl_setopt($handle, CURLOPT_POSTFIELDS, json_encode($parameters));
	curl_setopt($handle, CURLOPT_HTTPHEADER, array("Content-Type: application/json"));
	curl_setopt($handle, CURLOPT_SSL_VERIFYPEER, false);
	curl_exec($handle);
}

$offset = 0;
$result = getUpdate();
while (true) {
	$result = getUpdate();
	if ($result!=array()) {
		foreach ($result AS $post) {
			try {
				$post = json_encode($post);
				$post = json_decode($post);
				$username = "";
				$chatid = $post->message->chat->id;
				$message = $post->message->text;
				if (isset($post->message->from->username)) {
					$username = $post->message->from->username;
				}
				if (in_array($chatid, $allowedTelegramChatIds)) {
					$message = str_replace("/", "", $message);
					$message = strtolower($message);
					$messageExploded = explode(":", $message);
					if ($message=="start" OR $message=="info" OR $message=="status") {
						$message = "*Hi, Raspberry PI here!*\n\n";
						$command = escapeshellcmd('python /var/www/html/ip.py');
						$output = shell_exec($command);
						$message .= $output;
					}
					elseif ($message=="arduino" OR $message=="arduinoinfo") {
						$online = array();
						$offline = array();
						foreach ($IPs as $thisIp) {
							$ch = curl_init();
							curl_setopt($ch, CURLOPT_URL, "http://".$thisIp);
							curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
							curl_setopt($ch, CURLOPT_CONNECTTIMEOUT_MS, 50);
							$output = curl_exec($ch);
							curl_close($ch);
							if (strlen($output)>0 AND strpos($output, "Arduino here!")!==false) {
								$online[] = $thisIp;
							}
							else {
								$offline[] = $thisIp;
							}
						}
						if (count($online)==count($IPs)) {
							$message = "*All Arduino are online!*\n\n";
							foreach ($online AS $thisIp) {
								$message .= $thisIp."\n";
							}
						}
						elseif (count($offline)==count($IPs)) {
							$message = "*All Arduino are offline!*\n\n";
							foreach ($offline AS $thisIp) {
								$message .= $thisIp."\n";
							}
						}
						else {
							$message = "*Arduino online:*\n";
							foreach ($online AS $thisIp) {
								$message .= $thisIp."\n";
							}
							$message .= "\n*Arduino offline:*\n";
							foreach ($offline AS $thisIp) {
								$message .= $thisIp."\n";
							}
						}
					}
					elseif (isset($messageExploded[2]) AND $messageExploded[1]=="rgb") {
						if ($messageExploded[0]=="a" OR $messageExploded[0]=="all") {
							$count = 0;
							$colors = explode("-", $messageExploded[2]);
							$colors[0] = intval($colors[0])%256;
							$colors[1] = intval($colors[1])%256;
							$colors[2] = intval($colors[2])%256;
							if (isset($colors[2])) {
								foreach ($IPs AS $thisIp) {
									$ch = curl_init();
									curl_setopt($ch, CURLOPT_URL, "http://".$thisIp."?ledR=".$colors[0]."&ledG=".$colors[1]."&ledB=".$colors[2]);
									curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
									curl_setopt($ch, CURLOPT_CONNECTTIMEOUT_MS, 100);
									$output = curl_exec($ch);
									if (strpos($output, "Arduino here!")!==false) {
										$count++;
									}
									curl_close($ch);
								}
								$message = "RGB led set to ($colors[0], $colors[1], $colors[2]) on all Arduino online ($count)";
							}
							else {
								$message = "Syntax error";
							}
						}
						elseif (in_array($messageExploded[0], $IPs)) {
							$count = 0;
							$colors = explode("-", $messageExploded[2]);
							$colors[0] = intval($colors[0])%256;
							$colors[1] = intval($colors[1])%256;
							$colors[2] = intval($colors[2])%256;
							if (isset($colors[2])) {
								$ch = curl_init();
								curl_setopt($ch, CURLOPT_URL, "http://".$messageExploded[0]."?ledR=".$colors[0]."&ledG=".$colors[1]."&ledB=".$colors[2]);
								curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
								curl_setopt($ch, CURLOPT_CONNECTTIMEOUT_MS, 100);
								$output = curl_exec($ch);
								if (strpos($output, "Arduino here!")!==false) {
									$count++;
								}
								curl_close($ch);
								if ($count==1) {
									$message = "RGB led set to ($colors[0], $colors[1], $colors[2]) on Arduino at $messageExploded[0]";
								}
								else {
									$message = "Unable to reach Arduino at $messageExploded[0]";
								}
							}
							else {
								$message = "Syntax error";
							}
						}
						else {
							$message = "Syntax error";
						}
					}
					elseif (isset($messageExploded[2]) AND ($messageExploded[1]=="led1" || $messageExploded[1]=="led2")) {
						if ($messageExploded[0]=="a" OR $messageExploded[0]=="all") {
							$count = 0;
							$value = $messageExploded[2];
							if ($value=="off") {
								$value = 0;
							}
							elseif ($value!=0 OR $value=="on") {
								$value = 1;
							}
							foreach ($IPs AS $thisIp) {
								$ch = curl_init();
								curl_setopt($ch, CURLOPT_URL, "http://".$thisIp."?".$messageExploded[1]."=".$value);
								curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
								curl_setopt($ch, CURLOPT_CONNECTTIMEOUT_MS, 100);
								$output = curl_exec($ch);
								if (strpos($output, "Arduino here!")!==false) {
									$count++;
								}
								curl_close($ch);
							}
							if ($value==0) {
								$value = "OFF";
							}
							else {
								$value = "ON";
							}
							$message = ucfirst($messageExploded[1])." set to $value on all Arduino online ($count)";
						}
						elseif (in_array($messageExploded[0], $IPs)) {
							$count = 0;
							$value = $messageExploded[2];
							if ($value=="off") {
								$value = 0;
							}
							elseif ($value!=0 OR $value=="on") {
								$value = 1;
							}
							$ch = curl_init();
							curl_setopt($ch, CURLOPT_URL, "http://".$messageExploded[0]."?".$messageExploded[1]."=".$value);
							curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
							curl_setopt($ch, CURLOPT_CONNECTTIMEOUT_MS, 100);
							$output = curl_exec($ch);
							if (strpos($output, "Arduino here!")!==false) {
								$count++;
							}
							curl_close($ch);
							if ($value==0) {
								$value = "OFF";
							}
							else {
								$value = "ON";
							}
							if ($count==1) {
								$message = ucfirst($messageExploded[1])." set to $value on Arduino at $messageExploded[0]";
							}
							else {
								$message = "Unable to reach Arduino at $messageExploded[0]";
							}
						}
						else {
							$message = "Syntax error";
						}
					}
					else {
						$message = "Unrecognized command";
					}

					sendMessage($chatid, $message);
				}
				else {
					sendMessage($chatid, "*Hi, Raspberry PI here!*\n\nYou are not allowed to use this bot.\nIf you are the owner, add your chat id in the array _allowedTelegramChatIds_ in the file _config.php_ and restart the bot.\n\n*chat id: ".$chatid."*");
				}
			}
			catch (Exception $e) {
				continue;
			}
		}
	}
}
?>
