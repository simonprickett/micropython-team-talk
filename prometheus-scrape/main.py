import network
import ntptime
import random
import secrets
import time

from microdot import Microdot

rolls = [0, 0, 0, 0, 0, 0]

html_action_list = f"""
    <p>You can:</p>
    <ul>
        <li><a href="/roll">Roll the dice</a>.</li>
        <li><a href="/metrics">View the metrics</a>.</li>
        <li><a href="/reset">Reset the counters</a>.</li>
    </ul>
"""

app = Microdot()

# TODO work on this some more...
def generate_html_page(html_body):
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><title>MicroPython Dice Roll Example</title></head><body>{html_body}</body></html>"""

@app.route("/")
async def index(request):
    return generate_html_page(f"""<h1>MicroPython Dice Roll Example</h1>{html_action_list}"""), {"Content-Type": "text/html"}


@app.route("/roll")
async def rolldice(request):
    this_roll = random.randint(1, 6)
    rolls[this_roll - 1] = rolls[this_roll - 1] + 1
    return generate_html_page(f"<p>You rolled a {this_roll}.</p>{html_action_list}"), {"Content-Type": "text/html"}


@app.route("/reset")
async def reset(request):
    global rolls
    rolls = [0, 0, 0, 0, 0 , 0]
    return generate_html_page(f"<p>Roll counts reset to 0.</p>{html_action_list}"), {"Content-Type": "text/html"}


@app.route("/metrics")
async def metrics(request):
    # TODO tidy this up into Prometheus format.
    return f"""dice_roll{{number="1"}} {rolls[0]}
dice_roll{{number="2"}} {rolls[1]}
dice_roll{{number="3"}} {rolls[2]}
dice_roll{{number="4"}} {rolls[3]}
dice_roll{{number="5"}} {rolls[4]}
dice_roll{{number="6"}} {rolls[5]}
"""

# Connect to the network.
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)

while not wlan.isconnected() and wlan.status() >= 0:
    print("Connecting to wifi...")
    time.sleep(1)

ip_address = wlan.ifconfig()[0]
print(f"Visit http://{ip_address}:{secrets.PORT}")

ntptime.settime()

# Start the server.
app.run(port=secrets.PORT)