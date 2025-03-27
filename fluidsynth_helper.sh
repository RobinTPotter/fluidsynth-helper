#!/bin/bash

PYTHON=/home/pi/fluidsynth-helper/venv/bin/python
keyboard=$(aconnect -i | grep -i "client" | grep -i  "Interface" | head -1 | cut -d ' ' -f 2)0
fluidsynth=$(aconnect -o | grep -i  "fluid" | head -1 | cut -d ' ' -f 2)0

echo keyboard $keyboard
echo fluidsynth $fluidsynth


# Configuration
SCRIPT_PATH="/home/pi/fluidsynth-helper/modules/vel100.py"
ARGS="-vm 0 -vo 30 -di $keyboard -do $fluidsynth"
LOG_FILE="fluidsynth_helper.log"
PID_FILE="fluidsynth_helper.pid"

start_service() {
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo "Service is already running."
        exit 1
    fi

    echo "Starting fluidsynth-helper..."
    nohup $PYTHON "$SCRIPT_PATH" $ARGS >> "$LOG_FILE" 2>&1 & 
    echo $! > "$PID_FILE"
    echo "Service started with PID $(cat "$PID_FILE")"
}

stop_service() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        echo "Stopping service (PID $PID)..."
        kill "$PID" && rm -f "$PID_FILE"
        echo "Service stopped."
    else
        echo "No service running."
    fi
}

status_service() {
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo "Service is running (PID $(cat "$PID_FILE"))."
    else
        echo "Service is not running."
    fi
}

case "$1" in
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        stop_service
        start_service
        ;;
    status)
        status_service
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac
