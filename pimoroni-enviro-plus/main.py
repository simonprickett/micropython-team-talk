import network
import ntptime
import secrets
import time

from prometheus_remote_write_payload import PrometheusRemoteWritePayload

PROMETHEUS_AUTH = (secrets.PROMETHEUS_USER, secrets.PROMETHEUS_PASSWORD)

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
