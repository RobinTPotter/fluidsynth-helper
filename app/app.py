from flask import Flask, render_template, request, redirect, url_for
import subprocess
import time
import fluids

app = Flask(__name__)


@app.route("/")
def index():
    """Render the instrument selection page."""
    instruments = fluids.get_instruments()
    return render_template("index.html", instruments=instruments)

@app.route("/stops")
def stops():
    """Render the instrument selection page."""
    instruments = fluids.get_instruments()
    return render_template("stops.html", instruments=instruments)

@app.route("/fancy")
def fancy():
    """Render the instrument selection page."""
    instruments = fluids.get_instruments()
    return render_template("fancy.html", instruments=instruments)

@app.route("/fonts")
def fancy():
    """Render the instrument selection page."""
    instruments = fluids.get_fonts()
    return render_template("fonts.html", instruments=instruments)

@app.route("/select", methods=["POST","GET"])
def select_instrument():
    """Send 'select 0 1 bank voice' command via Telnet."""

    if request.form:
        bank = request.form["bank"]
        voice = request.form["voice"]
    else:
        bank = request.args.get("bank")
        voice = request.args.get("voice")

    fluids.change_voice(bank, voice)

    return redirect(url_for("index"))

@app.route("/font", methods=["POST","GET"])
def select_font():
    

    if request.form:
        name = request.form["name"]
    else:
        name = request.args.get("name")

    fluids.change_font(name)

    return redirect(url_for("fonts"))

if __name__ == "__main__":
    app.run(debug=True)

