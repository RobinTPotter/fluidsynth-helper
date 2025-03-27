#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

export PYTHONPATH=$SCRIPT_DIR:$SCRIPT_DIR/modules
FLASK_APP="app/app.py"
FLASK_CMD="/home/pi/fluidsynth-helper/venv/bin/flask run --host=0.0.0.0"
PID_FILE="flask.pid"
echo $PYTHONPATH
start() {
    if [ -f "$PID_FILE" ]; then
        ps aux | grep $(cat $PID_FILE) | grep flask | grep -v grep && echo "Flask is already running (PID: $(cat $PID_FILE))" && exit 1
    fi

    echo "Starting Flask..."
    export FLASK_APP=$FLASK_APP
    nohup $FLASK_CMD > flask.log 2>&1 & echo $! > $PID_FILE
    echo "Flask started with PID $(cat $PID_FILE)"
}

stop() {
    if [ ! -f "$PID_FILE" ]; then
        echo "Flask is not running."
        exit 1
    fi

    PID=$(cat $PID_FILE)
    echo "Stopping Flask (PID: $PID)..."
    kill $PID && rm -f $PID_FILE
    echo "Flask stopped."
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        start
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac

