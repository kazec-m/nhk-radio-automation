#!/bin/bash
set -a
source "$(dirname "$0")/.env"
set +a

export XDG_RUNTIME_DIR=/run/user/1000
pactl set-default-sink "$ECHO_SINK_NAME"
sleep 5
wpctl set-volume 72 80%
sleep 1
xvfb-run -a python3 "/home/$PI_USER/Desktop/nhk_radio_echo.py"
