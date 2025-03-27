# fluidsynth-helper

fluidsynth is a software soundfont renderer which can be started as a shell or as a server.

In server mode, it can be attached to using telnet, i.e. ```telnet localhost 9800```

There are two parts to this repo, ```fluidsynth.sh``` is used to start fluidsynth server and use aconnect to attach a midi controller to fluidsynth server:

```
Usage: ./fluidsynth.sh soundfont.sf2 [sleep_time] [interface]

Arguments:
  soundfont.sf2  Path to the SoundFont file.
  sleep_time     Optional. Default: 5. Time to wait before connecting MIDI devices.
  interface      Optional. Default: 'Interface'. Used to filter MIDI input devices.
```

For example:

```
bash fluidsynth.sh ../GM\ DLS\ Remastered\ Version\ 2.sf2
```

If sleep_time "none" is used the script exits before aconnect makes the connections

If fluidsynth is running alreay in some form running the command will kill any existing


The second part is a flask app, which serves a web page showing all the voices in banks in the soundfont (from commands send via telnet).

The resulting displayed buttons are then pressed to change the voice in fluidsynth:

```
PYTHONPATH=modules:. FLASK_APP=app.py flask run --host=0.0.0.0
```

or 

```
set PYTHONPATH=modules;. && python app\app.py
```

or for convenience:

```
./flask.sh start|stop|restart
```

Install mido and rtmidi python libraries to use the script to compress velocity

```
python vel100.py
```

this reads the queue of events from 24:0, resets the velocity to 100 and writes to 128:0


# installing 

see ```requirements.txt```

and for pi zero w2 ubuntu image:

```
sudo apt install build-essential python3-dev libasound2-dev fluidsynth alsa-tools alsa-utils python3-venv
```
