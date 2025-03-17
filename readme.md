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

The second part is a flask app, which serves a web page showing all the voices in banks in the soundfont (from commands send via telnet).

The resulting displayed buttons are then pressed to change the voice in fluidsynth:

```
FLASK_APP=app.py flask run --host=0.0.0.0
```

or for convenience:

```
./flask.sh start|stop|restart
```

Install midish to use the script to compress velocity

```
midish < vel100.mdsh
```
