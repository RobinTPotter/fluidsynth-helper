import config
import subprocess

def get_instruments():
    """Fetch instruments list from Fluidsynth via Telnet."""
    try:
            response = subprocess.run(
                "{ echo \"inst 1\"; sleep 1; } |"
                f"telnet {config.TELNET_HOST} {config.TELNET_PORT};",
                shell=True, capture_output=True
            )
            lines = response.stdout.decode("utf-8", "ignore").split("\n")
            instruments = []
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

def change_voice(bank, voice):
    try:
        response = subprocess.run(
            f"{{ echo \"select 0 1 {bank} {voice}\"; sleep 1; }}"
            f" | telnet {config.TELNET_HOST} {config.TELNET_PORT};",
            shell=True,
            capture_output=True
        )
    except Exception as e:
        return f"Error: {e}"