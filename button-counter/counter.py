import gc
import network
import ntptime
import requests
import time
import secrets

from machine import Pin
from prometheus_remote_write_payload import PrometheusRemoteWritePayload

DEBOUNCE_MS = 3000

REQUEST_HEADERS = {
    "Content-Encoding": "snappy",
    "Content-Type": "application/x-protobuf",
    "User-Agent": "MicroPython",
    "X-Prometheus-Remote-Write-Version": "1.0.0"
}

PROMETHEUS_AUTH = (secrets.PROMETHEUS_USER, secrets.PROMETHEUS_PASSWORD)

button = Pin(14, Pin.IN, Pin.PULL_UP)
last_press = 0
num_presses = 0

def button_pressed(pin):
    global last_press, num_presses

    ms_now = time.ticks_ms()

    if time.ticks_diff(ms_now, last_press) >= DEBOUNCE_MS:
        print("Pressed!")
        last_press = ms_now
        num_presses += 1

        prometheus = PrometheusRemoteWritePayload()

        prometheus.add_data(
            "button", # Name
            {
                "instance": ip_address
            }, # Labels
            num_presses, # Data
            int(time.time() * 1000) # Timestamp
        )

        print("Sending data...")

        response = requests.post(
            secrets.PROMETHEUS_ENDPOINT,
            headers = REQUEST_HEADERS,
            data = prometheus.get_payload(),
            auth = PROMETHEUS_AUTH
        )

        if response.status_code == 200:
            print(f"Data sent: num_presses {num_presses}.")
        else:
            print(f"Error sending data: {response.status_code} {response.text}")

        gc.collect() # Clean up memory... :(


button.irq(trigger=Pin.IRQ_FALLING, handler=button_pressed)

# Connect to the network.
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)

while not wlan.isconnected() and wlan.status() >= 0:
    print("Connecting to wifi...")
    time.sleep(1)

ip_address = wlan.ifconfig()[0]
ntptime.settime()

print(f"Connected, IP address: {ip_address}, time: {time.time()}")


while True:
    time.sleep(0.25)
