#!/bin/sh

if ps ax | grep -v grep | grep var/www/html/_telegrambot.php > /dev/null
then
    echo "Telegram bot is running, everything is fine"
else
    echo "Telegram bot is not running"
    /usr/bin/php7.0 /var/www/html/_telegrambot.php &
fi
