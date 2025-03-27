from flask import Flask, render_template, request, redirect, url_for
import subprocess
import time
import modules.fluids as fluids
import urllib.parse
import threading
import os


app = Flask(__name__)
app.connection_thread = None
app.stop_event = None
app.cached_instruments = None
app.cached_instrument_choice = None
app.cached_font_choice = None
app.velocity_multiplier = 1.0
app.velocity_output = 0



def cache_instruments(force=False):
    if not app.cached_instruments or force:
        app.cached_instruments = fluids.get_instruments()
    return app.cached_instruments

def cache_instrument_choice(name):
    app.cached_instrument_choice = name

def cache_font_choice(font):
    app.cached_font_choice = font

@app.route("/fancy")
@app.route("/")
def fancy():
    """Render the instrument selection page."""
    instruments = cache_instruments()
    name = fluids.get_name()
    return render_template("fancy.html", instruments=instruments, name=name, selected=app.cached_instrument_choice)

@app.route("/fonts")
def fonts():
    """Render the instrument selection page."""
    fonts = [{"name": f, "quote": urllib.parse.quote_plus(f)} for f in fluids.get_fonts()]
    cache_instruments()
    return render_template("fonts.html", fonts=fonts, selected=app.cached_font_choice)

@app.route("/connect")
def connect():
    return render_template(
        "connect.html"
        , connections_in=fluids.get_connections_in()
        , connections_out=fluids.get_connections_out()
        , velocity_multiplier=app.velocity_multiplier
        , velocity_output=app.velocity_output,
        )

@app.route("/stops")
def stops():
    """Render the instrument selection page."""
    instruments = fluids.get_instruments()
    return render_template("stops.html", instruments=instruments)




@app.route("/select", methods=["POST","GET"])
def select_instrument():
    """Send 'select 0 1 bank voice' command via Telnet."""

    if request.form:
        bank = request.form["bank"]
        voice = request.form["voice"]
        name = request.form["name"]
    else:
        bank = request.args.get("bank")
        voice = request.args.get("voice")
        name = urllib.parse.unquote(request.args.get("name"))

    cache_instrument_choice(name)
    fluids.change_voice(bank, voice) #, fluids.CURRENT_ID)

    return redirect(url_for("fancy"))

@app.route("/font/<name>/<none>", methods=["GET"])
def select_font(name, none):
    none = True if none=="true" else False
    new_id = fluids.change_font(urllib.parse.unquote_plus(name), none)
    cache_font_choice(urllib.parse.unquote_plus(name))
    cache_instruments(force=True)
    print("changed to " + str(new_id))
    return redirect(url_for("fonts"))

@app.route("/connect_stop")
def connect_stop():
    if app.connection_thread:
        print("setting stop event")
        app.stop_event.set()
        print(f"joining {app.connection_thread}")
        app.connection_thread.join()
        print("joined")
        app.stop_event = threading.Event()
    return redirect(url_for("connect"))

@app.route("/shutdown/<really>")
def shutdown(really):
    if really=="yes":
        os.system("sudo shutdown now")

@app.route('/connect_up', methods=['POST'])
def connect_up():
    import modules.vel100 as vel100
    import threading

    app.stop_event
    if app.stop_event is None:
        app.stop_event = threading.Event()
        print("made stop event")

    if app.connection_thread:
        print("setting stop event")
        app.stop_event.set()
        print(f"joining {app.connection_thread}")
        app.connection_thread.join()
        print("joined")
        app.stop_event = threading.Event()
    else:
        print("no connection_thread")

    velocity_multiplier = float(request.form['velocity_multiplier'])
    velocity_output = int(request.form['velocity_output'])
    app.velocity_multiplier = velocity_multiplier
    app.velocity_output = velocity_output
    device_in = request.form['midi_input']
    device_out = request.form['midi_output']
    
    test = vel100.get_args()
    app.logger.info(test)
    test.velocity_multiplier = velocity_multiplier
    test.velocity = velocity_output
    test.device_in = device_in
    test.device_out = device_out
        
    app.connection_thread = vel100.start_thread(test, app.stop_event)
    
    return redirect(url_for('connect'))


if __name__ == "__main__":
    app.run(debug=True)

