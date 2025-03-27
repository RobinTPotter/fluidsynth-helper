
import config
import subprocess

CURRENT_ID = 1

def get_instruments(id=1):
    """Fetch instruments list from Fluidsynth via Telnet."""
    try:
            response = subprocess.run(
                f"{{ echo \"inst {id}\"; sleep 1; }} |"
                f"telnet {config.TELNET_HOST} {config.TELNET_PORT};",
                shell=True, capture_output=True
            )
            lines = response.stdout.decode("utf-8", "ignore").split("\n")
            instruments = []
            print (f"response size: {len(lines)}")
            for line in lines:
                try:
                    parts = line.split(" ", 1)
                    parts = parts[0].split("-") + [parts[1]]
                    if len(parts) > 2 and parts[0].isdigit() and parts[1].isdigit():
                        bank = parts[0]
                        voice = parts[1]
                        name = " ".join(parts[2:])
                        instruments.append({"bank": bank, "voice": voice, "name": name})
                except Exception as e:
                    print(e)
            return instruments
    except Exception as e:
        print(e)
        return []

def get_fonts():
    """Fetch list of files from soundfonts directory."""
    import os
    print(os.listdir("."))
    try:
        fonts = [f for f in os.listdir(config.SOUNDFONT_PATH) if f.lower().endswith(".sf2")]
        print(fonts)
        return fonts
    except Exception as e:
        print(e)
        return []

def change_font(name, none):
    """unload currect soundfont and load new soundfont."""
    try:
        #response = subprocess.run(
        #    f"{{ echo \"unload {id}\"; sleep 2; echo \"load {config.SOUNDFONT_PATH}/{name}\"; sleep 2; }}"
        #    f" | telnet {config.TELNET_HOST} {config.TELNET_PORT};",
        #    shell=True,
        #    capture_output=True
        #)
        none = " none" if none else ""
        response = subprocess.run(
            f"if pidof fluidsynth ; then kill $(pidof fluidsynth); fi && /home/pi/fluidsynth-helper/fluidsynth.sh \"{config.SOUNDFONT_PATH}/{name}\"{none}",
            shell=True,
            capture_output=True
        )
        print(response)
        new_id = response.stdout.decode("utf-8","ignore").split(" ")[-1]
        return new_id
    except Exception as e:
        return f"Error: {e}"

def get_name():
    try:
        response = subprocess.run(
            f"{{ echo \"fonts\"; sleep 1; }}"
            f" | telnet {config.TELNET_HOST} {config.TELNET_PORT};",
            shell=True,
            capture_output=True
        )
    
        dat = response.stdout.decode("utf-8", "ignore").split("\n")
        dat = [d for d in dat if config.SOUNDFONT_PATH in d][0]
        return "/" +  "/".join(dat.split("/")[1:])


    except:
        pass

def change_voice(bank, voice, id=1, channel=0):
    try:
        response = subprocess.run(
            f"{{ echo \"select {channel} {id} {bank} {voice}\"; sleep 1; }}"
            f" | telnet {config.TELNET_HOST} {config.TELNET_PORT};",
            shell=True,
            capture_output=True
        )
    except Exception as e:
        return f"Error: {e}"

def get_connections_in():
    try:
        response = subprocess.run(
            f"{{ aconnect -i; }}",
            shell=True,
            capture_output=True
        )
        connections = response.stdout.decode("utf-8", "ignore").split("\n")
        connections = [{"id": c.split(" ")[1]+"0", "name": " ".join(c.split(" ")[2:])} for c in connections if "client" in c]
        return connections
    except Exception as e:
        return f"Error: {e}"
    
def get_connections_out():
    try:
        response = subprocess.run(
            f"{{ aconnect -o; }}",
            shell=True,
            capture_output=True
        )
        connections = response.stdout.decode("utf-8", "ignore").split("\n")
        connections = [{"id": c.split(" ")[1], "name": " ".join(c.split(" ")[2:])} for c in connections if "client" in c]
        return connections
    except Exception as e:
        return f"Error: {e}"
