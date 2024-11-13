#!/bin/bash

PY=$HOME/.miniconda/envs/bot.env/bin/python
CONFIG=$HOME/configs/omniunibot/bot_server.json
CMD="${PY} -m omniunibot.server -c ${CONFIG}"

echo -n "Stop omniunibot server ... "
pkill -u $(id -u) -f "${CMD}"
echo "[OK]"

echo -n "Start omniunibot server ... "
nohup $CMD > /dev/null 2>&1  &
sleep 0.1
pid=`ps ux | grep "$CMD" | grep -v grep | awk '{print $2}'`
if [ -z $pid ]; then
echo "[FAIL]"
else
echo "[OK] [PID=$pid]"
fi

