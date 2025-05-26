import gc
import machine
import network
import ntptime
import requests
import secrets
import time

from breakout_bme68x import BreakoutBME68X, STATUS_HEATER_STABLE
from machine import Pin, ADC
from picographics import PicoGraphics, DISPLAY_ENVIRO_PLUS
from pimoroni_i2c import PimoroniI2C
from breakout_ltr559 import BreakoutLTR559
from prometheus_remote_write_payload import PrometheusRemoteWritePayload


# Constants for posting data to the Prometheus remote write endpoint.
PROMETHEUS_REQUEST_HEADERS = {
    "Content-Encoding": "snappy",
    "Content-Type": "application/x-protobuf",
    "User-Agent": "MicroPython-Pimoroni-EnviroPlus",
    "X-Prometheus-Remote-Write-Version": "1.0.0"
}
PROMETHEUS_AUTH = (secrets.PROMETHEUS_USER, secrets.PROMETHEUS_PASSWORD)

def clear_screen():
    display.set_pen(BLACK_PEN)
    display.clear()


# Set up the display.
display = PicoGraphics(display=DISPLAY_ENVIRO_PLUS)
display.set_backlight(0.6)
display.set_font("bitmap8")

# Some pens we'll use for drawing.
WHITE_PEN = display.create_pen(255, 255, 255)
BLACK_PEN = display.create_pen(0, 0, 0)
RED_PEN = display.create_pen(255, 0, 0)
GREEN_PEN = display.create_pen(0, 255, 0)

WIDTH, HEIGHT = display.get_bounds()

try:

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

    metrics_last_sent = 0
    num_mic_readings = 0
    total_mic_values = 0

    while True:
        print(f"Next mic reading {mic.read_u16()}") 
        total_mic_values += mic.read_u16()
        num_mic_readings += 1
        print(f"Mic readings taken: {num_mic_readings}, avg {round(total_mic_values / num_mic_readings)}")

        ticks_now = time.ticks_ms()

        # Is it time to send the metrics?
        if time.ticks_diff(ticks_now, metrics_last_sent) > (int(secrets.SAMPLE_INTERVAL) * 1000):
            print("Reading sensors...")

            # Read BME688.
            temperature, pressure, humidity, gas, status, _, _ = bme.read()
            pressure = round(pressure / 100, 2)
            gas = round(gas, 2)
            heater = "Stable" if status & STATUS_HEATER_STABLE else "Unstable"

            # Correct temperature and humidity using an offset due to heat from device and screen.
            corrected_temperature = round(temperature - 5, 1)
            dewpoint = temperature - ((100 - humidity) / 5)
            corrected_humidity = round(100 - (5 * (corrected_temperature - dewpoint)), 1)

            # Read LTR559.
            ltr_reading = ltr.get_reading()
            lux = round(ltr_reading[BreakoutLTR559.LUX], 2)

            # Calculate an average mic reading over the period.
            mic_reading = round(total_mic_values / num_mic_readings)

            if heater == "Stable" and ltr_reading is not None:
                print(f"Temperature: {corrected_temperature}")
                print(f"Humidity: {corrected_humidity}")
                print(f"Pressure: {pressure}")
                print(f"Gas: {gas}")
                print(f"Light: {lux}")
                print(f"Sound: {mic_reading}")

                clear_screen()
                display.set_pen(WHITE_PEN)
                display.text(f"Temp: {corrected_temperature}C", 10, 10, WIDTH, scale=2)
                display.text(f"Humidity: {corrected_humidity}%", 10, 30, WIDTH, scale=2)
                display.text(f"Pressure: {pressure}", 10, 50, WIDTH, scale=2)
                display.text(f"Gas: {gas}", 10, 70, WIDTH, scale=2)
                display.text(f"Light: {lux}", 10, 90, WIDTH, scale=2)
                display.text(f"Sound: {mic_reading}", 10, 110, WIDTH, scale=2)
                display.update()

                # Send data to Prometheus remote write endpoint.
                data_timestamp = time.time() * 1000

                prometheus = PrometheusRemoteWritePayload()
                prometheus.add_data(
                    "temperature", { "instance": secrets.LOCATION }, corrected_temperature, data_timestamp
                )
                prometheus.add_data(
                    "humidity", { "instance": secrets.LOCATION }, humidity, data_timestamp
                )
                prometheus.add_data(
                    "pressure", { "instance": secrets.LOCATION }, pressure, data_timestamp
                )
                prometheus.add_data(
                    "gas", { "instance": secrets.LOCATION }, gas, data_timestamp
                )
                prometheus.add_data(
                    "light", { "instance": secrets.LOCATION }, lux, data_timestamp
                )
                prometheus.add_data(
                    "sound", { "instance": secrets.LOCATION }, mic_reading, data_timestamp
                )
                prometheus.add_data(
                    "memory", { "instance": secrets.LOCATION }, gc.mem_free(), data_timestamp
                )

                # Send data to the Prometheus remote write endpoint.
                response = requests.post(
                    secrets.PROMETHEUS_ENDPOINT,
                    headers = PROMETHEUS_REQUEST_HEADERS,
                    auth = PROMETHEUS_AUTH,
                    data = prometheus.get_payload()
                )

                if response.status_code == 200:
                    print(f"Data sent to remote write endpoint.")
                    display.set_pen(GREEN_PEN)
                    display.text("Data sent!", 10, 135, scale=3)
                else:
                    print(f"Error {response.status_code} sending data to remote write endpoint.")
                    display.set_pen(RED_PEN)
                    display.text(f"Error: {response.status_code}", 10, 135, scale=3)

                display.update()

                metrics_last_sent = time.ticks_ms()

            else:
                print("Sensors not ready yet or not reporting.")
                clear_screen()
                display.set_pen(RED_PEN)
                display.text("Sensors not ready.", 10, 80, WIDTH, scale=3)
                display.update()

            # Reset the microphone averaging process.
            num_mic_readings = 0
            total_mic_values = 0

        print("Sleeping...")
        display.set_pen(WHITE_PEN)
        display.text("Sleeping.", 10, 190, scale=3)
        display.update()
        time.sleep(.25)

except Exception:
    # Just reboot...
    machine.reset()