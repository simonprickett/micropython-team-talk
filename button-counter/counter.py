import gc
import network
import ntptime
import requests
import time
import secrets

from machine import Pin
from prometheus_remote_write_payload import PrometheusRemoteWritePayload

DEBOUNCE_MS = 2000

REQUEST_HEADERS = {
    "Content-Encoding": "snappy",
    "Content-Type": "application/x-protobuf",
    "User-Agent": "MicroPython",
    "X-Prometheus-Remote-Write-Version": "1.0.0"
}

PROMETHEUS_AUTH = (secrets.PROMETHEUS_USER, secrets.PROMETHEUS_PASSWORD)

count_button = Pin(14, Pin.IN, Pin.PULL_UP)
reset_button = Pin(9, Pin.IN, Pin.PULL_UP)

last_count_press = 0
last_reset_press = 0
num_presses = 0

def count_button_pressed(pin):
    global last_count_press, num_presses

    ms_now = time.ticks_ms()

    if time.ticks_diff(ms_now, last_count_press) >= DEBOUNCE_MS:
        is_sending = True
        print("Pressed!")
        last_count_press = ms_now
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

def reset_button_pressed(pin):
    global last_reset_press, num_presses

    ms_now = time.ticks_ms()

    if time.ticks_diff(ms_now, last_reset_press) >= DEBOUNCE_MS:
        num_presses = 0
        print("Count reset to 0.")
        last_reset_press = ms_now


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

count_button.irq(trigger=Pin.IRQ_FALLING, handler=count_button_pressed)
reset_button.irq(trigger=Pin.IRQ_FALLING, handler=reset_button_pressed)

while True:
    time.sleep(0.25)
