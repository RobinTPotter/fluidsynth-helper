from flask import Flask, render_template, request, redirect, url_for
import telnetlib
import subprocess
import time

app = Flask(__name__)

TELNET_HOST = "localhost"
TELNET_PORT = 9800

def get_instruments():
    """Fetch instruments list from Fluidsynth via Telnet."""
    try:
            response = subprocess.run('{ echo "inst 1"; sleep 1; } | telnet localhost 9800;', shell=True, capture_output=True)
            #print(response)
            lines = response.stdout.decode("utf-8", "ignore").split("\n")
            print(lines)
            instruments = []
            for line in lines:
                try:
                    print(line)
                    parts = line.split(" ", 1)
                    parts = parts[0].split("-") + [parts[1]]
                    print(parts)
                    if len(parts) > 2 and parts[0].isdigit() and parts[1].isdigit():
                        bank = parts[0]
                        voice = parts[1]
                        name = " ".join(parts[2:])
                        instruments.append({"bank": bank, "voice": voice, "name": name})
                except Exception as e:
                    print(e)
            print(instruments)
            return instruments
    except Exception as e:
        print(e)
        return []

@app.route("/")
def index():
    """Render the instrument selection page."""
    instruments = get_instruments()
    return render_template("index.html", instruments=instruments)

@app.route("/stops")
def stops():
    """Render the instrument selection page."""
    #instruments = [
    #{ "bank": 1, "voice": 2, "name": "pooo"},
    #{ "bank": 1, "voice": 6, "name": "pp"}
    #]
    instruments = get_instruments()
    return render_template("stops.html", instruments=instruments)

@app.route("/select", methods=["POST","GET"])
def select_instrument():
    """Send 'select 0 1 bank voice' command via Telnet."""

    if request.form:
        bank = request.form["bank"]
        voice = request.form["voice"]
    else:
        bank = request.args.get("bank")
        voice = request.args.get("voice")

    print((request, bank, voice))


    print((request, bank, voice))

    try:
        response = subprocess.run(f"{{ echo \"select 0 1 {bank} {voice}\"; sleep 1; }} | telnet localhost 9800;", shell=True, capture_output=True)
    except Exception as e:
        return f"Error: {e}"

    return redirect(url_for("index"))

#return "Instrument Selected", 200

if __name__ == "__main__":
    app.run(debug=True)

