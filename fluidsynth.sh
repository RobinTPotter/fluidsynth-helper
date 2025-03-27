#!/bin/bash



# Print help message
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    echo "Usage: $0 soundfont.sf2 [sleep_time] [interface]"
    echo
    echo "Arguments:"
    echo "  soundfont.sf2  Path to the SoundFont file."
    echo "  sleep_time     Optional. Default: 5. Time to wait before connecting MIDI devices."
    echo "  interface      Optional. Default: 'Interface'. Used to filter MIDI input devices."
    exit 0
fi

# Assign default values to optional arguments
soundfont="$1"
sleep_time="${2:-2}"
interface="${3:-Interface}"
echo soundfont $soundfont
echo sleep_time $sleep_time
echo interface $interface

if pidof fluidsynth &>/dev/null; then
    kill $(pidof fluidsynth)
else
    fluidsynth --server --no-shell --audio-driver=alsa -o audio.period-size=128 -o audio.periods=2 -r 44100 -g 1.0 "$soundfont" &>/dev/null &
    
    keyboard=$(aconnect -i | grep -i "client" | grep -i "$interface" | head -1 | cut -d ' ' -f 2)0
    fluidsynth=$(aconnect -o | grep -i "fluid" | head -1 | cut -d ' ' -f 2)0

    if [[ "$sleep_time" == "none" ]]; then
        echo "not connecting: $keyboard -> $fluidsynth"
        exit
    fi
    sleep "$sleep_time"
    echo "Connecting: $keyboard -> $fluidsynth"
    aconnect "$keyboard" "$fluidsynth"
fi

