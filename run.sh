#!/bin/bash
cd /home/Keypi/gift_bot
source venv310/bin/activate

while true; do
    echo "Starting bot at $(date)"
    python main.py
    echo "Bot crashed, restarting in 5s..."
    echo "Bot crashed at $(date)" >> crash.log
    sleep 5
done
