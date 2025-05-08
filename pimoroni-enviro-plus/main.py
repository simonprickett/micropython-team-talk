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

def clear_screen():
    display.set_pen(BLACK_PEN)
    display.clear()


# Set up the display.
display = PicoGraphics(display=DISPLAY_ENVIRO_PLUS)
display.set_backlight(1.0)
display.set_font("bitmap8")

# Some pens we'll use for drawing.
WHITE_PEN = display.create_pen(255, 255, 255)
BLACK_PEN = display.create_pen(0, 0, 0)
RED_PEN = display.create_pen(255, 0, 0)
GREEN_PEN = display.create_pen(0, 255, 0)

WIDTH, HEIGHT = display.get_bounds()

# Connect to the network.
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)

while not wlan.isconnected() and wlan.status() >= 0:
    # TODO Update the screen.
    print("Connecting to wifi...")
    clear_screen()
    display.set_pen(WHITE_PEN)
    display.text("Connecting to wifi...", 10, 10, WIDTH, scale=3)
    display.update()
    time.sleep(1)

ip_address = wlan.ifconfig()[0]
ntptime.settime()

print(f"Connected, IP address: {ip_address}, time: {time.time()}")
clear_screen()
display.set_pen(GREEN_PEN)
display.text("Wifi connected!", 10, 10, WIDTH, scale=3)
display.text(f"IP: {ip_address}", 10, 50, WIDTH, scale=3)
display.text(f"Time: {time.time()}", 10, 90, WIDTH, scale=3)
display.update()
time.sleep(3)
clear_screen()

# Set up the Pico W's I2C.
PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}
i2c = PimoroniI2C(**PINS_BREAKOUT_GARDEN)

# Set up BME688 and LTR559 sensors.
bme = BreakoutBME68X(i2c, address=0x77)
ltr = BreakoutLTR559(i2c)

# Set up analog channel for microphone.
mic = ADC(Pin(26))

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
        clear_screen()
        display.set_pen(WHITE_PEN)
        display.text(f"Temp: {corrected_temperature}C", 10, 10, WIDTH, scale=2)
        display.text(f"Humidity: {corrected_humidity}%", 10, 30, WIDTH, scale=2)
        display.text(f"Pressure: {pressure}", 10, 50, WIDTH, scale=2)
        display.text(f"Gas: {gas}", 10, 70, WIDTH, scale=2)
        display.text(f"Light: {lux}", 10, 90, WIDTH, scale=2)
        display.text(f"Sound: {gas}", 10, 110, WIDTH, scale=2)
        display.update()

        # TODO Send to Prometheus remote write endpoint.
    else:
        print("Sensors not ready yet or not reporting.")
        clear_screen()
        display.set_pen(RED_PEN)
        display.text("Sensors not ready.", 10, 80, WIDTH, scale=3)
        display.update()

    print("Sleeping...")
    display.set_pen(WHITE_PEN)
    display.text("Sleeping.", 10, 190, scale=3)
    display.update()
    time.sleep(int(secrets.SAMPLE_INTERVAL))
