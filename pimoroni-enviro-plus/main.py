import network
import ntptime
import secrets
import time

from breakout_bme68x import BreakoutBME68X, STATUS_HEATER_STABLE
from machine import Pin, ADC
from picographics import PicoGraphics, DISPLAY_ENVIRO_PLUS
from pimoroni_i2c import PimoroniI2C
from breakout_ltr559 import BreakoutLTR559
from prometheus_remote_write_payload import PrometheusRemoteWritePayload

PROMETHEUS_AUTH = (secrets.PROMETHEUS_USER, secrets.PROMETHEUS_PASSWORD)

# Set up the display.
display = PicoGraphics(display=DISPLAY_ENVIRO_PLUS)
display.set_backlight(1.0)

# Connect to the network.
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)

while not wlan.isconnected() and wlan.status() >= 0:
    # TODO Update the screen.
    print("Connecting to wifi...")
    time.sleep(1)

ip_address = wlan.ifconfig()[0]
ntptime.settime()

print(f"Connected, IP address: {ip_address}, time: {time.time()}")

# Set up the Pico W's I2C.
PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}
i2c = PimoroniI2C(**PINS_BREAKOUT_GARDEN)

# Set up BME688 and LTR559 sensors.
bme = BreakoutBME68X(i2c, address=0x77)
ltr = BreakoutLTR559(i2c)

# Set up analog channel for microphone.
mic = ADC(Pin(26))

# TODO Update the screen.

while True:
    print("Reading sensors...")

    # Read BME688.
    temperature, pressure, humidity, gas, status, _, _ = bme.read()
    pressure = pressure / 100
    heater = "Stable" if status & STATUS_HEATER_STABLE else "Unstable"

    # Correct temperature and humidity using an offset.
    corrected_temperature = temperature - 3
    dewpoint = temperature - ((100 - humidity) / 5)
    corrected_humidity = 100 - (5 * (corrected_temperature - dewpoint))

    # Read LTR559.
    ltr_reading = ltr.get_reading()
    lux = ltr_reading[BreakoutLTR559.LUX]
    prox = ltr_reading[BreakoutLTR559.PROXIMITY]

    # Read mic.
    mic_reading = mic.read_u16()

    if heater == "Stable" and ltr_reading is not None:
        print(f"Temperature: {corrected_temperature}")
        print(f"Humidity: {corrected_humidity}")
        print(f"Pressure: {pressure}")
        print(f"Gas: {gas}")
        print(f"Light: {lux}")
        print(f"Sound: {mic_reading}")

        # TODO Update the screen.

        # TODO Send to Prometheus remote write endpoint.
    else:
        print("Sensors not ready yet or not reporting.")

    print("Sleeping...")
    time.sleep(int(secrets.SAMPLE_INTERVAL))
