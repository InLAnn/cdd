#!/bin/sh

# export LD_LIBRARY_PATH=./

while true; do
    server=`ps -aux | grep python3 | grep weibo_monitor`
    if [ ! "$server" ]; then
        time=$(date "+%Y%M%D-%H:%M:%S")
        echo "weibo_monitor.py breakdown at ${time}"
        nohup python3 -u weibo_monitor.py >> log_weibo.log 2>&1 & 
        sleep 10
    fi
    sleep 60
done
