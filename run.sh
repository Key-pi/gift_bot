#!/bin/bash

echo "Bot supervisor started"

while true
do
  echo "Starting bot at $(date)"
  /home/Keypi/gift_bot/venv310/bin/python /home/Keypi/gift_bot/main.py
  echo "Bot crashed. Restarting in 5 seconds..."
  sleep 5
  echo "Bot crashed at $(date)" >> crash.log

done
