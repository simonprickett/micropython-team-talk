# Prometheus Metrics Scraping Example

TODO overview...

## Hardware

You'll need either a [Raspberry Pi Pico W](https://shop.pimoroni.com/products/raspberry-pi-pico-w?variant=40059369652307) or the newer [Pico 2 W](https://shop.pimoroni.com/products/raspberry-pi-pico-2-w?variant=54852253024635).  As we're not connecting any other hardware to the microcontroller, you don't need to byu one with the headers attached. However, if you also want to try the [button counter example project](../button-counter/), you should get the "WH" version with the headers pre-soldered.

To get the code onto the device and power it, you'll need a [USB to Micro USB data cable](https://shop.pimoroni.com/products/usb-a-to-microb-cable-black?variant=31241639562) too.

## MicroPython Version 

You'll need to install a MicroPython runtime on the Pico W.  Get the latest `.uf2` image and follow the installation instructions:

* [Image for Raspberry Pi Pico W](https://micropython.org/download/RPI_PICO_W/)
* [Image for Raspberry Pi Pico 2 W](https://micropython.org/download/RPI_PICO2_W/)

We've tested the code using MicroPython 1.25.

## Copy the Source Code to the Pico W

TODO

## Run the Code

TODO

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

## Checking that Promethus is Scraping the Pico W

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