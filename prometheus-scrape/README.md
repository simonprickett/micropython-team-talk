# Prometheus Metrics Scraping Example

This is a simple example showing how to expose metrics in a format that Prometheus can consume by making a HTTP request to a MicroPython script running on the Pico W. It's a sample application that allows you to roll a dice and build up some metrics about how many times each number has been rolled.

This uses a locally installed copy of open source Prometheus.

## Hardware

You'll want either a [Raspberry Pi Pico W](https://shop.pimoroni.com/products/raspberry-pi-pico-w?variant=40059369652307) or the newer [Pico 2 W](https://shop.pimoroni.com/products/raspberry-pi-pico-2-w?variant=54852253024635).  As we're not connecting any other hardware to the microcontroller, you don't need to buy one with the headers attached. However, if you also want to try the [button counter example project](../button-counter/), you should get the "WH" version with the headers pre-soldered.

To get the code onto the device and power it, you'll need a [USB to Micro USB data cable](https://shop.pimoroni.com/products/usb-a-to-microb-cable-black?variant=31241639562) too.

## MicroPython Version 

You'll need to install a MicroPython runtime on the Pico W.  Get the latest `.uf2` image and follow the installation instructions:

* [Image for Raspberry Pi Pico W](https://micropython.org/download/RPI_PICO_W/)
* [Image for Raspberry Pi Pico 2 W](https://micropython.org/download/RPI_PICO2_W/)

We've tested the code using MicroPython 1.25.

## Configure and Install the Code

Now its time to copy the source code to your Pico W and configure the WiFi network credentials.

At your terminal, first change to the correct directory:

```bash
cd prometheus-scrape
```

### Configuring Secrets

Next, create a `secrets.py` file by copying the example provided:

```bash
cp secrets_example.py secrets.py
```

Using a text editor, edit `secrets.py`, replacing the values of `WIFI_SSID` and `WIFI_PASSWORD` with the values for your network. Save your changes.

### Copying Code to the Pico W

We'll copy the source code to the Pico W using the `mpremote` command.  Connect your Pico W to your machine using the USB to Micro USB cable, then enter the following commands:

```bash
mpremote fs cp main.py :main.py
mpremote fs cp secrets.py :secrets.py
mpremote fs cp microdot.py :microdot.py
```

This project uses parts of the [Microdot framework](https://microdot.readthedocs.io/en/latest/index.html) (MIT license) to implement a simple web server. For convenience, the file `microdot.py` from this project has been included in this repository.

Verify that the code was copied correctly:

```bash
mpremote fs ls
```

You should see output similar to this (your file sizes may vary from those shown):

```
ls :
        1848 main.py
       56305 microdot.py
          60 secrets.py
```

## Run the Code

With your Pico W connected to your machine by the USB to MicroUSB cable, run the code like so:

```bash
mpremote run main.py
```

You should see output similar to the following on the MicroPython console:

```
Connecting to wifi...
Connecting to wifi...
Connecting to wifi...
...
Visit http://192.168.5.31:80
```

Once you see a URL on the console, you're ready to generate some metrics!  If the code doesn't connect to the network, check the values for `WIFI_SSID` and `WIFI_PASSWORD` are correct in `secrets.py` and update that file on your device if necessary.

## Roll 'em!

Now the code's up and running, visit the URL that was output to the MicroPython console.  It'll be something like:

```
http://192.168.5.31:80/
```

You'll see a menu of actions.  Click "Roll the dice" a few times, then "View the metrics" to see the page that Prometheus will scrape metrics from.  It'll look something like this:

```
dice_roll{number="1"} 3
dice_roll{number="2"} 5
dice_roll{number="3"} 3
dice_roll{number="4"} 3
dice_roll{number="5"} 4
dice_roll{number="6"} 3
```

You'll need to use your browser's back button to return to a page with the navigation options on it.

If you want to reset the roll counts to 0 at any point, click "Reset the counters".

## Install Prometheus

Install a local copy of Prometheus by following the official [getting started tutorial](https://prometheus.io/docs/prometheus/latest/getting_started/). Make sure that the machine you install it on is on the same wirelss network that you configured the Pico to attach to.

## Example Prometheus Job Configuration

Configure Prometheus to monitor the Pico W by editing `prometheus.yml` and adding the following scrape configuration. You'll need to substitute the IP address that your Pico W connects to your network with.

```yaml
scrape_configs:
  - job_name: 'diceroller'
    scrape_interval: 10s

    static_configs:
      - targets: ['192.168.5.31:80']
```

## Scraping Metrics with Prometheus

With the MicroPython code up and running on your Pico W, go ahead and start Prometheus like so:

```bash
./prometheus --config.file=prometheus.yml
```

Then visit:

```
http://localhost:9090/query
```

and execute the following query expression:

```
dice_roll
```

You should see results similar to these, showing the number of times each number has been rolled:

```
dice_roll{instance="192.168.5.31:80", job="diceroller", number="1"}	  3
dice_roll{instance="192.168.5.31:80", job="diceroller", number="2"}	  5
dice_roll{instance="192.168.5.31:80", job="diceroller", number="3"}	  3
dice_roll{instance="192.168.5.31:80", job="diceroller", number="4"}	  3
dice_roll{instance="192.168.5.31:80", job="diceroller", number="5"}	  4
dice_roll{instance="192.168.5.31:80", job="diceroller", number="6"}	  3
```

From here, you can try more complex queries using PromQL ([check out the official querying Prometheus tutorial](https://prometheus.io/docs/prometheus/latest/querying/basics/)).